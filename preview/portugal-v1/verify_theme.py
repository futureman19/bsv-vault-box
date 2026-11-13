import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'portugal.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def validate():
 waves=[o for o in bpy.data.objects if o.name.startswith('Atlantic wave')]
 assert len(waves)==3
 for o in waves:
  assert o.parent==lid
  v=[o.matrix_world@p.co for p in o.data.vertices]
  assert abs(min(p.x for p in v)+1.35)<1e-5 and abs(max(p.x for p in v)-1.35)<1e-5
  assert 1.97<min(p.z for p in v)<1.99 and 2.2<max(p.z for p in v)<2.3
 slab=bpy.data.objects['Lid / polished slab'];assert (slab.dimensions-Vector((3.72,2.38,.30))).length<1e-5
 assert len([i for i in bpy.data.images if i.packed_file])>=3
 assert latch.parent==lid
 return waves
waves=validate();original=waves[0].parent;waves[0].parent=None
try:validate()
except AssertionError:negative=True
else:raise AssertionError('Detached ornament negative control not rejected')
waves[0].parent=original
# Independently compare actual saved baseline pivot matrices.
matrices={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
err=max(abs(matrices[n][i][j]-bpy.data.objects[n].matrix_world[i][j]) for n in matrices for i in range(4) for j in range(4));assert err<1e-7
out={'status':'PASS','three_solid_waves':True,'lid_parentage':True,'dimensions':True,'packed_maps':True,'detached_wave_negative_rejected':negative,'baseline_pivot_max_error':err}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print('THEME PASS',json.dumps(out))
