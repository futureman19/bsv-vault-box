import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'chad.blend'),use_scripts=False)
def check_arch(objects):
 arches=[o for o in objects if o.name=='Ennedi / open wind arch'];assert len(arches)==1,'Missing real arch'
 o=arches[0];assert o.parent.name=='Lid_Hinge'
 bpy.context.view_layer.update();v=[o.matrix_world@p.co for p in o.data.vertices]
 tree=BVHTree.FromPolygons(v,[list(p.vertices) for p in o.data.polygons])
 for x in [-.3,0,.3]:
  assert tree.ray_cast(Vector((x,-2,2.20)),Vector((0,1,0)))[0] is None,'Arch opening obstructed'
 assert tree.ray_cast(Vector((0,-2,2.68)),Vector((0,1,0)))[0] is not None,'Arch crown missing'
 assert max(p.x for p in v)-min(p.x for p in v)>2
 assert max(p.z for p in v)>2.8
 return len(v)
verts=check_arch(list(bpy.data.objects))
try:check_arch([o for o in bpy.data.objects if not o.name.startswith('Ennedi')])
except AssertionError as e:negative=str(e)
else:raise AssertionError('Negative control did not fail')
ornaments=[o for o in bpy.data.objects if o.name.startswith('Ennedi')]
assert len(ornaments)==6 and all(o.parent.name=='Lid_Hinge' for o in ornaments)
assert tuple(round(x,3) for x in bpy.data.objects['Lid_Hinge'].location)==(0,1.32,1.668)
images=[i for i in bpy.data.images if i.packed_file];assert len(images)>=3
for i in images:
 assert tuple(i.size)==(512,512)
 samples=list(i.pixels)[::4];assert max(samples)-min(samples)>.05
r={'status':'PASS','arch_vertices':verts,'opening_ray_samples':3,'crown_ray_hit':True,'lid_ornaments':len(ornaments),'maps':len(images),'negative_control':negative,'limits':'Art interpretation, not a named arch scale replica'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
