import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'panama.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
pivots={o.name:[list(r) for r in o.matrix_world] for o in [lid,latch]}
def owns(o):
 assert o.parent==lid,o.name
ornaments=[o for o in bpy.data.objects if o.name.startswith(('Mangrove /','Bank /','Tide /'))]
assert len(ornaments)==55,len(ornaments)
for o in ornaments:owns(o)
probe=ornaments[0];probe.parent=None
try:
 owns(probe)
except AssertionError: negative=True
else: raise AssertionError('Detached ornament accepted')
probe.parent=lid
water=bpy.data.objects['Tide / continuous inlet']
v=[water.matrix_world@p.co for p in water.data.vertices]
assert len(v)==82 and len(water.data.polygons)==40
assert abs(min(p.x for p in v)+1.4)<1e-5 and abs(max(p.x for p in v)-1.4)<1e-5
assert max(p.y for p in v)-min(p.y for p in v)>.65
# Consecutive quads must share exactly a full edge, not isolated water islands.
for a,b in zip(water.data.polygons, list(water.data.polygons)[1:]):assert len(set(a.vertices)&set(b.vertices))==2
banks=[o for o in ornaments if o.name.startswith('Bank /')]
bvhs=[BVHTree.FromPolygons([o.matrix_world@p.co for p in o.data.vertices],[list(p.vertices) for p in o.data.polygons]) for o in banks]
roots=[]
for o in ornaments:
 if not o.name.startswith('Mangrove / stilt root'):continue
 # First seven vertices are the first tube ring; its center is the foot anchor.
 p=sum((o.matrix_world@v.co for v in list(o.data.vertices)[:7]),Vector())/7
 hits=[t.ray_cast(p+Vector((0,0,.1)),Vector((0,0,-1)),.2)[0] for t in bvhs]
 assert any(h is not None and abs(h.z-p.z)<1e-5 for h in hits),(o.name,list(p))
 roots.append({'name':o.name,'foot':list(p)})
assert len(roots)==15
assert max((o.matrix_world@v.co).z for o in ornaments for v in o.data.vertices)<3.05
# Independent saved baseline opening establishes inherited pivot matrices.
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
error=max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for n,m in pivots.items() for i in range(4) for j in range(4))
assert error<1e-6,error
out={'status':'PASS','ornaments':len(ornaments),'water_quads_connected':40,'root_anchor_rays':roots,'detached_ornament_negative_rejected':negative,'pivot_matrix_max_error':error,'notes':'Root ring centers checked against sediment; sampled source geometry, not botanical accuracy.'}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print('THEME PASS',json.dumps(out))
