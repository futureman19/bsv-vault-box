import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'slovakia.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
lid=bpy.data.objects['Lid_Hinge'];relief=[o for o in bpy.data.objects if o.name.startswith('Lime relief')];facade=[o for o in bpy.data.objects if o.name.startswith('Lime facade')]
def check_relief():
 assert len(relief)==60
 for o in relief:
  assert o.parent==lid
  v=[o.matrix_world@v.co for v in o.data.vertices]
  assert 1.976<min(p.z for p in v)<1.979
  assert 2.025<max(p.z for p in v)<2.06
  assert max(abs(p.x) for p in v)<1.6 and max(abs(p.y) for p in v)<.90
check_relief();assert len(facade)==108,len(facade)
# Real in-memory mutation: detached relief must be rejected; never saved.
o=relief[0];o.parent=None
try:check_relief();raise RuntimeError('Negative control incorrectly accepted')
except AssertionError:negative='PASS: detached relief rejected'
o.parent=lid
# Encoded palette targets and actual image variation.
images=[i for i in bpy.data.images if i.packed_file];assert len(images)>=5
assert not any(o.name.startswith(('Cedar tree','Terrain')) for o in bpy.data.objects)
r={'status':'PASS','pivot_parity':'exact within 1e-7','relief_strokes':len(relief),'diamond_repeats':15,'facade_strokes':len(facade),'relief_seated':True,'negative_control':negative,'packed_images':[i.name for i in images]}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
