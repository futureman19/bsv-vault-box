import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'suriname.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];dome=bpy.data.objects['Inselberg / bare granite dome'];river=bpy.data.objects['River / connected inlay'];forest=[o for o in bpy.data.objects if o.name.startswith('Forest /')]
def validate():
 for o in [dome,river,*forest,bpy.data.objects['Terrain / island']]:assert o.parent==lid,o.name
 assert len(forest)==27
 dv=[dome.matrix_world@v.co for v in dome.data.vertices];top=max(v.z for v in dv);assert 2.63<top<2.93
 assert all(max((o.matrix_world@v.co).z for v in o.data.vertices)<top-.3 for o in forest)
 assert len(river.data.vertices)==98 and len(river.data.polygons)==48
 # Actual evaluated visibility at each face center; no exact boundary rays.
 for i in range(48):
  points=[river.matrix_world@river.data.vertices[j].co for j in [2*i,2*i+1,2*i+2,2*i+3]]
  x=sum(v.x for v in points)/4;y=sum(v.y for v in points)/4
  hit,loc,n,idx,o,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,4)),Vector((0,0,-1)))
  assert hit and o==river,(i,o.name if o else None)
 return top
height=validate();river.parent=None
try:validate()
except AssertionError:negative=True
else:negative=False
river.parent=lid;assert negative
# Same pivots independently reopened from included mechanism baseline.
actual={n:list(bpy.data.objects[n].location) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
expected={n:list(bpy.data.objects[n].location) for n in actual};assert actual==expected
r=dict(status='PASS',forest_clusters=27,dome_top=height,river_visible_samples=48,all_relief_lid_owned=True,detached_river_negative_control_rejected=negative,pivots_match=actual)
(R/'theme-source-check.json').write_text(json.dumps(r,indent=2));print('THEME SOURCE PASS',r)
