import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'jamaica.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];terrain=bpy.data.objects['Terrain / Blue and John Crow relief']
def check_parent(o):assert o.parent==lid,('Missing moving lid parent',o.name)
items=[o for o in bpy.data.objects if o.name.startswith('Terrain /')]
for o in items:check_parent(o)
terrain.parent=None
try:check_parent(terrain)
except AssertionError:negative=True
else:raise AssertionError('Detached ornament negative not rejected')
terrain.parent=lid;bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(v-m[i][j]) for i,row in enumerate(bpy.data.objects[n].matrix_world) for j,v in enumerate(row))<1e-7
v=[terrain.matrix_world@v.co for v in terrain.data.vertices];lo=[min(c[i] for c in v) for i in range(3)];hi=[max(c[i] for c in v) for i in range(3)]
assert -1.5<lo[0]<-1.3 and 1.3<hi[0]<1.5 and lo[2]>1.96 and hi[2]<2.85
# Connected topology, independent of the object's name.
adj={i:set() for i in range(len(v))}
for e in terrain.data.edges:a,b=e.vertices;adj[a].add(b);adj[b].add(a)
seen={0};todo=[0]
while todo:
 for j in adj[todo.pop()]-seen:seen.add(j);todo.append(j)
assert len(seen)==len(v)
# Count three prominent maxima along an actual surface section in world space.
tree=BVHTree.FromPolygons(v,[list(p.vertices) for p in terrain.data.polygons]);heights=[]
for i in range(121):
 x=-1.2+i*.02;hit=tree.ray_cast(Vector((x,.10,4)),Vector((0,0,-1)))[0];assert hit is not None;heights.append(hit.z)
peaks=[i for i in range(1,120) if heights[i]>heights[i-1] and heights[i]>heights[i+1] and heights[i]>2.30]
assert len(peaks)>=3,peaks
canopies=[o for o in items if 'canopy' in o.name];assert len(canopies)>=50
for c in canopies:
 p=c.matrix_world.translation;h=tree.ray_cast(Vector((p.x,p.y,4)),Vector((0,0,-1)))[0];assert h and abs(h.z-p.z)<1e-5
assert not any('Cedar' in o.name for o in bpy.data.objects)
result={'status':'PASS','relief_bounds':[lo,hi],'connected_vertices':len(seen),'section_peak_count':len(peaks),'lid_owned_terrain_meshes':len(items),'seated_canopies':len(canopies),'original_pivot_matrices_match':True,'detached_ornament_negative_rejected':negative,'limitations':'Section sampling and canopy-centre seating, not botanical or geographic fidelity.'}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
