import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'cuba.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def gate():
 hills=[o for o in bpy.data.objects if o.name.startswith('Mogote /')];assert len(hills)==3
 for o in hills:
  assert o.parent==lid,'mogote detached from lid'
  z=[(o.matrix_world@v.co).z for v in o.data.vertices];assert .45<max(z)-min(z)<.83
  assert abs(min(z)-2.023)<1e-5
  assert {p.material_index for p in o.data.polygons}=={0,1}
 assert bpy.data.objects['Valley / earth plain'].parent==lid
 return [o.name for o in hills]
names=gate();o=bpy.data.objects[names[0]];o.parent=None
try:gate()
except AssertionError as e:negative=str(e)
else:raise AssertionError('negative control did not fail')
o.parent=lid;gate()
# Compare pivot local matrices independently against the included immutable mechanism.
actual={o.name:[list(row) for row in o.matrix_local] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
err=max(abs(actual[n][i][j]-bpy.data.objects[n].matrix_local[i][j]) for n in actual for i in range(4) for j in range(4));assert err<1e-7
report=dict(status='PASS',mogotes=names,root_z=2.023,negative_control={'detached_mogote_rejected':negative},pivot_max_error=err)
(R/'theme-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
