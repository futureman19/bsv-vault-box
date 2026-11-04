"""Independent saved-source visual-contract and negative-control checks."""
import bpy,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'canada.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
ornaments=[o for o in bpy.data.objects if o.name.startswith(('Pine /','Shield shore /','Shield lake /'))]
def ownership():
 assert ornaments and all(o.parent==lid for o in ornaments),'Ornament detached from lid'
ownership()
victim=next(o for o in ornaments if o.name=='Pine / trunk');victim.parent=None
try:
 ownership()
except AssertionError as e: negative=str(e)
else: raise AssertionError('Detached ornament negative control not rejected')
victim.parent=lid;ownership();bpy.context.view_layer.update()
def bounds(o):
 vv=[o.matrix_world@Vector(v) for v in o.bound_box]
 return [[min(v[i] for v in vv) for i in range(3)],[max(v[i] for v in vv) for i in range(3)]]
slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<1e-5 for a,b in zip(slab.dimensions,[3.72,2.38,.30]))
water=bpy.data.objects['Shield lake / inlay'];assert all(abs(a-b)<1e-5 for a,b in zip(water.dimensions,[2.86,1.62,.026]))
pines=[o for o in ornaments if o.name.startswith('Pine /')];assert max(bounds(o)[1][2] for o in pines)<3.05
assert len([o for o in pines if 'branch' in o.name])==20
assert len([o for o in pines if 'foliage' in o.name])==4
shores=[o for o in ornaments if o.name.startswith('Shield shore /')];assert len(shores)==3 and max(bounds(o)[1][2] for o in shores)<2.378
# Real evaluated surface overlap at root/trunk to granite, not bbox coincidence.
def tree(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();t=BVHTree.FromPolygons([o.matrix_world@v.co for v in m.vertices],[list(p.vertices) for p in m.polygons]);ev.to_mesh_clear();return t
rock=tree(bpy.data.objects['Shield shore / rear right'])
root_contact=[o.name for o in pines if ('root' in o.name or 'trunk' in o.name) and tree(o).overlap(rock)]
assert root_contact,'Pine floats above rock'
pine_max_z=max(bounds(o)[1][2] for o in pines)
current={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,m in current.items():
 assert max(abs(m[i][j]-bpy.data.objects[name].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
result=dict(status='PASS',ornament_count=len(ornaments),negative_control_rejected=negative,pine_root_surface_contacts=root_contact,lid_dimensions=[3.72,2.38,.30],pine_max_z=pine_max_z,same_pivot_matrices=current)
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print('THEME PASS',json.dumps(result))
