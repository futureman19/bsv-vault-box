import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'south-korea.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];flowers=[o for o in bpy.data.objects if o.name.startswith('Pearl / lid chrysanthemum')]
def check():
 assert len(flowers)==5
 assert all(o.parent==lid for o in flowers)
 for o in flowers:
  vs=[o.matrix_world@v.co for v in o.data.vertices]
  assert min(v.z for v in vs)>=1.979 and max(v.z for v in vs)<2.08
  assert len(o.data.polygons)==72
check();flowers[0].parent=None
try:check();raise RuntimeError('negative control incorrectly passed')
except AssertionError:negative=True
flowers[0].parent=lid
r={'status':'PASS','lid_flowers':5,'petals_each':12,'body_flowers':len([o for o in bpy.data.objects if o.name.startswith(('Pearl / body flower','Pearl / side flower'))]),'detached_ornament_rejected':negative,'scope':'original simplified craft-inspired relief, not authentic artisan inlay'}
assert r['body_flowers']==12
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(r)
