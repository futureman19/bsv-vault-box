import bpy,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'zimbabwe.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def check():
 blocks=[o for o in bpy.data.objects if o.name.startswith('Masonry /')];assert len(blocks)>=160
 rocks=[o for o in bpy.data.objects if o.name.startswith('Kopje /')];assert len(rocks)==4
 for o in rocks+[bpy.data.objects['Terrain / ochre plinth']]:assert o.parent==lid,o.name
 bounds=[o.matrix_world@v.co for o in rocks for v in o.data.vertices];assert max(v.z for v in bounds)<3.10
 assert abs(bpy.data.objects['Lid / polished slab'].dimensions.x-3.72)<1e-5
 def tree(n):
  o=bpy.data.objects[n];return BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[list(f.vertices) for f in o.data.polygons])
 pairs=[('Kopje / crown boulder','Kopje / middle boulder'),('Kopje / middle boulder','Kopje / basal boulder'),('Kopje / basal boulder','Terrain / ochre plinth'),('Kopje / companion','Terrain / ochre plinth'),('Terrain / ochre plinth','Lid / polished slab')]
 for a,b in pairs:assert tree(a).overlap(tree(b)),(a,b)
 return {'blocks':len(blocks),'kopje_boulders':len(rocks),'maximum_rock_z':max(v.z for v in bounds),'contact_pairs':pairs,'lid_ancestry':True}
out=check();o=bpy.data.objects['Kopje / crown boulder'];o.parent=None
try:check();raise RuntimeError('Negative control incorrectly accepted')
except AssertionError:out['detached_ornament_negative_control']='REJECTED'
o.parent=lid
# Compare inherited pivot local transforms from independently opened baseline.
current={o.name:[list(o.location),list(o.rotation_euler),list(o.scale)] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
original={n:[list(bpy.data.objects[n].location),list(bpy.data.objects[n].rotation_euler),list(bpy.data.objects[n].scale)] for n in current};assert original==current
out['pivots_match_mechanism']=True;out['status']='PASS';(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
