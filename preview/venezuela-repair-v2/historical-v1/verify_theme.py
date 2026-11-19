import bpy,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'venezuela.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,rows in pivots.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-rows[i][j]) for i in range(4) for j in range(4))<1e-7
lid=bpy.data.objects['Lid_Hinge'];names=['Tepui / sandstone massif','Tepui / summit vegetation','Tepui / continuous cascade','Tepui / basin']
def owned(o):return o.parent==lid
assert all(owned(bpy.data.objects[n]) for n in names)
o=bpy.data.objects[names[0]];p=o.parent;o.parent=None
assert not owned(o),'detached negative control must fail';o.parent=p
verts=[o.matrix_world@v.co for v in o.data.vertices];bounds=[[min(v[i] for v in verts),max(v[i] for v in verts)] for i in range(3)]
assert .80<bounds[2][1]-bounds[2][0]<.95
assert 1.7<bounds[0][1]-bounds[0][0]<2.2
summit=bpy.data.objects[names[1]];sv=[summit.matrix_world@v.co for v in summit.data.vertices];assert max(v.z for v in sv)-min(v.z for v in sv)<1e-6
water=bpy.data.objects[names[2]];wv=[water.matrix_world@v.co for v in water.data.vertices]
assert min(v.z for v in wv)<2.02 and max(v.z for v in wv)>2.83
# Mesh graph flood-fill proves the actual strip is one connected surface.
adj={v.index:set() for v in water.data.vertices}
for e in water.data.edges:a,b=e.vertices;adj[a].add(b);adj[b].add(a)
seen=set();todo=[0]
while todo:
 i=todo.pop()
 if i in seen:continue
 seen.add(i);todo.extend(adj[i]-seen)
assert len(seen)==len(wv)
# Perspective-independent front rays prove exposed falling ribbon at three heights.
dep=bpy.context.evaluated_depsgraph_get();rays=[]
for z in [2.25,2.5,2.7]:
 hit,loc,normal,index,obj,matrix=bpy.context.scene.ray_cast(dep,Vector((-.12,-3,z)),Vector((0,1,0)))
 assert hit and obj==water,(z,obj.name if obj else None)
 rays.append({'z':z,'first_hit':obj.name})
result={'status':'PASS','pivot_matrices_unchanged':True,'lid_owned_features':names,'tepui_bounds':bounds,'summit_flat':True,'cascade_connected_vertices':len(seen),'exposed_front_rays':rays,'detached_parent_negative_control_rejected':True}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
