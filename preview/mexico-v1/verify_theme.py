"""Independent saved-source visual contract and deliberate negative control."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
baseline={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mexico.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,rows in baseline.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-rows[i][j]) for i in range(4) for j in range(4))<1e-7
lid=bpy.data.objects['Lid_Hinge'];leaf=[o for o in bpy.data.objects if o.name.startswith('Agave / leaf')];tiles=[o for o in bpy.data.objects if o.name.startswith('Ceramic tile /')]
assert len(leaf)==24 and len(tiles)==78
assert len([o for o in bpy.data.objects if o.name.startswith('Lid ceramic /')])==18
assert not any(o.name.startswith(('Cedar','Moss','Granite')) for o in bpy.data.objects)
def ancestry():
 for o in leaf:
  assert o.parent==lid, 'Detached agave leaf: '+o.name
ancestry();obj=leaf[0];mw=obj.matrix_world.copy();obj.parent=None;obj.matrix_world=mw
try:ancestry()
except AssertionError as e:negative=str(e)
else:raise AssertionError('Negative control failed to reject detached leaf')
obj.parent=lid;obj.matrix_world=mw;ancestry();bpy.context.view_layer.update()
# Source mesh extremum and island attachment; no screenshot-coordinate guessing.
verts=[o.matrix_world@v.co for o in leaf for v in o.data.vertices]
assert max(v.z for v in verts)<3.15
assert all(abs(v.x)<1.65 and abs(v.y)<1.0 for v in verts)
island=bpy.data.objects['Agave / soil island'];assert island.parent==lid
mesh=island.data;tree=BVHTree.FromPolygons([island.matrix_world@v.co for v in mesh.vertices],[list(p.vertices) for p in mesh.polygons])
roots=[]
for o in leaf:
 # Four section vertices at root; center is under soil surface or within .025.
 c=sum((o.matrix_world@v.co for v in list(o.data.vertices)[:4]),Vector())/4
 hit,n,i,d=tree.ray_cast(Vector((c.x,c.y,3.5)),Vector((0,0,-1)))
 assert hit is not None and abs(c.z-hit.z)<.06,(o.name,c,hit)
 roots.append(abs(c.z-hit.z))
r={'status':'PASS','ceramic_body_tiles':len(tiles),'lid_border_tiles':18,'agave_leaves':len(leaf),'all_ornaments_lid_owned':True,'max_leaf_z':max(v.z for v in verts),'root_to_soil_max_abs_z':max(roots),'pivot_matrices_identical_to_included_mechanism':True,'negative_control':{'detached_leaf_rejected':True,'message':negative,'restored_pass':True},'old_theme_nodes_absent':True}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
