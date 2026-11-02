import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'jordan.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
assert tuple(round(v,3) for v in lid.location)==(0,1.32,1.668),list(lid.location)
terrain=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('Terrain /')]
assert len(terrain)==5 and all(o.parent==lid for o in terrain)
# Negative control changes real source ancestry, then calls the same assertion.
probe=terrain[0];saved=probe.parent;probe.parent=None
try:
 assert all(o.parent==lid for o in terrain)
except AssertionError:negative=True
else:raise AssertionError('ancestry negative control did not fail')
probe.parent=saved;bpy.context.view_layer.update()
def tree(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();t=BVHTree.FromPolygons([o.matrix_world@v.co for v in m.vertices],[list(p.vertices) for p in m.polygons]);ev.to_mesh_clear();return t
arch=bpy.data.objects['Terrain / open sandstone arch'];t=tree(arch)
# Ray through aperture must miss, while higher ray must hit actual arch crown.
aperture=t.ray_cast(Vector((.92,-1,2.15)),Vector((0,1,0)))[0]
crown=t.ray_cast(Vector((.92,-1,2.36)),Vector((0,1,0)))[0]
assert aperture is None and crown is not None,(aperture,crown)
west=bpy.data.objects['Terrain / west fluted massif'];east=bpy.data.objects['Terrain / east fluted massif']
wmax=max((west.matrix_world@v.co).x for v in west.data.vertices);emin=min((east.matrix_world@v.co).x for v in east.data.vertices)
assert emin-wmax>.15,(wmax,emin)
for o in terrain:
 for v in o.data.vertices:
  p=o.matrix_world@v.co
  assert abs(p.x)<=1.57 and abs(p.y)<=.96 and 1.97<=p.z<=2.89,(o.name,list(p))
assert not tree(arch).overlap(tree(west)) and not tree(arch).overlap(tree(east))
result={'status':'PASS','terrain_meshes':len(terrain),'all_terrain_lid_children':True,'arch_aperture_ray_miss':True,'arch_crown_ray_hit':list(crown),'massif_gap_x':emin-wmax,'terrain_bounds':True,'arch_clear_of_massifs':True,'negative_control_detached_terrain_rejected':negative,'lid_pivot':list(lid.location),'latch_pivot_local':list(latch.location)}
(R/'theme-source-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
