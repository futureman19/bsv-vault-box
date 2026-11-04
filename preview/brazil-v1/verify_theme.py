import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'brazil.blend'),use_scripts=False)
bpy.context.view_layer.update()
def lid_owned(o):
 while o.parent:
  o=o.parent
  if o.name=='Lid_Hinge':return True
 return False
features=[o for o in bpy.data.objects if o.name.startswith(('Forest /','River /'))]
assert len(features)>=33 and all(lid_owned(o) for o in features)
canopy=[o for o in features if 'canopy' in o.name];assert len(canopy)>=12
river=bpy.data.objects['River / continuous channel']
assert lid_owned(river)
old=river.parent;river.parent=None
negative=not lid_owned(river);assert negative
river.parent=old;bpy.context.view_layer.update()
# Direct ray samples independently hit the visible continuous water surface.
dep=bpy.context.evaluated_depsgraph_get();hits=[]
for i in range(61):
 x=-1.50+i*3/60;y=.18*math.sin(x*2.5)+.06*math.sin(x*5)
 hit,loc,n,ix,obj,m=bpy.context.scene.ray_cast(dep,Vector((x,y,4)),Vector((0,0,-1)))
 assert hit and obj.name==river.name,(i,obj.name if hit else None)
 hits.append([x,y,loc.z])
verts=[river.matrix_world@v.co for v in river.data.vertices]
assert max(v.x for v in verts)-min(v.x for v in verts)>=1.8
assert all(abs((verts[i+1]-verts[i]).y)>=.16 for i in range(0,len(verts),2))
assert max((o.matrix_world@v.co).z for o in features for v in o.data.vertices)<2.628
# Original pivot positions/rotations independently reopened, not guessed.
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,rows in pivots.items():assert max(abs(rows[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-6
out={'status':'PASS','forest_river_meshes':len(features),'canopy_clusters':len(canopy),'river_unoccluded_vertical_samples':len(hits),'river_samples':hits,'detached_river_negative_control_rejected':negative,'pivot_matrices_match_mechanism':True,'max_relief_bound':.65}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print('PASS theme, river, ancestry negative control, pivots')
