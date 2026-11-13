import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'libya.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot'];arch=bpy.data.objects['Terrain / Acacus open arch'];dune=bpy.data.objects['Terrain / two dune crests']
assert arch.parent==lid and dune.parent==lid and latch.parent==lid
assert abs(lid.location.y-1.32)<1e-5 and abs(lid.location.z-1.668)<1e-5
bpy.context.view_layer.update();v=[arch.matrix_world@x.co for x in arch.data.vertices];tree=BVHTree.FromPolygons(v,[list(p.vertices) for p in arch.data.polygons])
assert tree.ray_cast(Vector((.3,-2,2.35)),Vector((0,1,0)))[0] is None,'Arch aperture blocked'
assert tree.ray_cast(Vector((.3,-2,2.70)),Vector((0,1,0)))[0] is not None,'Missing arch crown'
assert 1.1<max(p.x for p in v)-min(p.x for p in v)<1.6
assert .55<max(p.z for p in v)-1.978<.95
slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<.001 for a,b in zip(slab.dimensions,(3.72,2.38,.30)))
# Fail-capability: filling the opening with actual triangles must fail the same aperture predicate.
blocked=BVHTree.FromPolygons([(-.1,.48,2.2),(.7,.48,2.2),(.7,.48,2.5),(-.1,.48,2.5)],[(0,1,2,3)])
assert blocked.ray_cast(Vector((.3,-2,2.35)),Vector((0,1,0)))[0] is not None
out={'status':'PASS','arch_aperture_clear':True,'arch_crown_hit':True,'negative_control_filled_aperture_rejected':True,'terrain_lid_parentage':True,'lid_dimensions':list(slab.dimensions),'lid_pivot':list(lid.location),'arch_height_above_lid':max(p.z for p in v)-1.978}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
