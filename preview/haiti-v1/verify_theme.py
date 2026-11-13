import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'haiti.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
garden=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('Garden /')];leaves=[o for o in garden if o.name.startswith('Garden / leaf')]
def ancestry():
 assert len(leaves)==12
 assert all(o.parent==lid for o in garden),'Detached garden ornament'
ancestry();leaf=leaves[0];leaf.parent=None
try:ancestry()
except AssertionError:negative=True
else:raise AssertionError('Detached leaf negative control did not fail')
leaf.parent=lid;ancestry()
verts=[o.matrix_world@v.co for o in garden for v in o.data.vertices]
assert max(v.z for v in verts)<2.2 and min(v.z for v in verts)>=1.978
assert 2.6<max(v.x for v in verts)-min(v.x for v in verts)<2.8
# Downward rays distinguish real leaf steel from the open spaces down to lid.
dep=bpy.context.evaluated_depsgraph_get();hits={}
for label,xy in [('gap',(.0,.7)),('stem',(.0,.04))]:
 hit,loc,n,idx,obj,m=bpy.context.scene.ray_cast(dep,Vector((*xy,3)),Vector((0,0,-1)))
 assert hit;hits[label]=obj.name
assert hits['gap']=='Lid / polished slab' and hits['stem'].startswith('Garden /'),hits
pivot={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
error=max(abs(pivot[name][i][j]-bpy.data.objects[name].matrix_world[i][j]) for name in pivot for i in range(4) for j in range(4));assert error<1e-8
out={'status':'PASS','garden_meshes':len(garden),'leaves':len(leaves),'lid_ancestry':True,'detached_leaf_negative_control_rejected':negative,'openwork_rays':hits,'max_ornament_z':max(v.z for v in verts),'inherited_pivot_max_error':error}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
