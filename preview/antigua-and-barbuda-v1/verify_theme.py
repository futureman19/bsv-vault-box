import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'antigua-and-barbuda.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge']
orn=[o for o in bpy.data.objects if o.name.startswith(('Coast /','Bridge /'))]
def owned(objects):
 assert len(objects)==5
 assert all(o.parent==lid for o in objects),'Detached lid ornament'
owned(orn)
# Real negative control, restored without saving source.
o=orn[0];p=o.parent;o.parent=None
try:
 owned(orn)
except AssertionError:negative=True
else:raise AssertionError('Detached ornament negative control not rejected')
o.parent=p;bpy.context.view_layer.update()
arch=bpy.data.objects['Bridge / open limestone arch'];ev=arch.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();tree=BVHTree.FromPolygons([arch.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons]);ev.to_mesh_clear()
# At center x .75, horizontal rays pass through opening, then hit crown.
for z in [2.08,2.16,2.24,2.32,2.40]:assert tree.ray_cast(Vector((.75,-1,z)),Vector((0,1,0)),3)[0] is None
assert tree.ray_cast(Vector((.75,-1,2.50)),Vector((0,1,0)),3)[0] is not None
current={n:list(bpy.data.objects[n].matrix_world) for n in []}
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(m[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
out=dict(status='PASS',ornaments=len(orn),all_lid_owned=True,detached_negative_rejected=negative,arch_aperture_ray_heights=[2.08,2.16,2.24,2.32,2.40],crown_ray_z=2.50,pivots_match_mechanism=True)
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(out)
