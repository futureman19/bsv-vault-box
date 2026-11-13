"""Saved-source theme gates, including connected visible tidal channels."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
from collections import deque
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
bpy.context.view_layer.update()
baseline={name:[list(row) for row in bpy.data.objects[name].matrix_local] for name in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'bangladesh.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def under(o,parent):
 while o.parent:
  o=o.parent
  if o==parent:return True
 return False
islands=[o for o in bpy.data.objects if o.name.startswith('Delta / island')]
assert len(islands)==4
ornaments=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(('Delta /','Lid ornament /','Lid border /'))]
assert ornaments and all(under(o,lid) for o in ornaments)
for o in ornaments:
 for v in o.data.vertices:
  p=o.matrix_world@v.co
  assert abs(p.x)<1.87 and abs(p.y)<1.20 and 1.97<p.z<2.24,(o.name,p)
# Exact inherited pivot comparison from the included immutable mechanism source.
pivots={o.name:list(o.matrix_local) for o in [lid,latch]}
for name in ['Lid_Hinge','Latch_Pivot']:
 assert all(abs(pivots[name][i][j]-baseline[name][i][j])<1e-8 for i in range(4) for j in range(4)),name
# Cast down on actual evaluated triangles, not a hand-authored channel annotation.
bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get();nx=101;ny=61;wet=set()
for iy in range(ny):
 for ix in range(nx):
  x=-1.40+2.80*ix/(nx-1);y=-.74+1.48*iy/(ny-1)
  hit,loc,n,idx,o,mat=bpy.context.scene.ray_cast(dep,Vector((x,y,3)),Vector((0,0,-1)))
  assert hit
  if o.name=='Delta / connected tidal water':wet.add((ix,iy))
assert wet
q=deque([next(iter(wet))]);connected=set(q)
while q:
 x,y=q.popleft()
 for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if p in wet and p not in connected:connected.add(p);q.append(p)
edges={edge:any(condition(x,y) for x,y in connected) for edge,condition in [('west',lambda x,y:x==0),('east',lambda x,y:x==nx-1),('south',lambda x,y:y==0),('north',lambda x,y:y==ny-1)]}
assert all(edges.values()),edges
fraction=len(wet)/(nx*ny);assert .08<fraction<.45,fraction
assert len(connected)==len(wet),(len(connected),len(wet))
result={'result':'PASS','islands':len(islands),'lid_ornament_meshes':len(ornaments),'all_lid_parented':True,'unchanged_mechanism_pivots':True,'ray_grid':[nx,ny],'visible_water_samples':len(wet),'connected_water_samples':len(connected),'water_fraction':fraction,'connected_channel_reaches':edges,'limit':'sampled visible water continuity, not geographic fidelity'}
(R/'theme-source-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
