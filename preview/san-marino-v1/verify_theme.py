import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'san-marino.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def contract(objects):
 towers=[o for o in objects if o.name.startswith('Tower ') and o.name.endswith('/ keep')]
 assert len(towers)==3, 'Exactly three tower keeps required'
 for o in objects:
  if o.name.startswith(('Tower ','Titano ridge','Battlement','Window ','Fortification','Scrub')):assert o.parent==lid,('Lid ownership',o.name)
 return towers
towers=contract(list(bpy.data.objects));negative=False
try:contract([o for o in bpy.data.objects if o!=towers[0]])
except AssertionError:negative=True
assert negative
# Verify roots intersect the top of the corresponding real evaluated crag.
roots=[]
for i,o in enumerate(towers):
 crag=bpy.data.objects['Titano ridge / crag '+str(i)];bottom=min((o.matrix_world@Vector(v)).z for v in o.bound_box)
 origin=crag.matrix_world.inverted()@Vector((o.matrix_world.translation.x,o.matrix_world.translation.y,4));hit,point,normal,index=crag.ray_cast(origin,Vector((0,0,-1)))
 assert hit;surface=(crag.matrix_world@point).z;assert bottom<=surface and surface-bottom<.3,(o.name,bottom,surface)
 roots.append({'tower':o.name,'bottom':bottom,'surface':surface})
# Compare independently reopened baseline pivot transforms.
current={o.name:[list(row) for row in o.matrix_local] for o in [lid,latch]}
assert len([o for o in bpy.data.objects if o.name.startswith('Battlement')])==12
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,matrix in current.items():assert max(abs(matrix[i][j]-bpy.data.objects[name].matrix_local[i][j]) for i in range(4) for j in range(4))<1e-7
r={'status':'PASS','three_towers':True,'all_ornaments_lid_owned':True,'missing_tower_negative_control_rejected':negative,'tower_root_surface_checks':roots,'baseline_pivots_unchanged':True,'battlements':12}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
