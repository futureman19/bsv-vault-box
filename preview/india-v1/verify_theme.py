import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'india.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def check():
 flowers=[o for o in bpy.data.objects if o.name.startswith('Floral /')]
 assert len([o for o in flowers if 'central petal' in o.name])==8
 assert len([o for o in flowers if 'satellite petal' in o.name])==24
 assert len([o for o in flowers if 'heart' in o.name])==5
 assert len([o for o in flowers if 'leaf' in o.name])==8
 assert all(o.parent==lid for o in flowers)
 bounds=[o.matrix_world@v.co for o in flowers for v in o.data.vertices]
 assert min(v.z for v in bounds)>=1.974 and max(v.z for v in bounds)<=2.04
 assert max(abs(v.x) for v in bounds)<1.6 and max(abs(v.y) for v in bounds)<1
 assert not any(o.name.startswith(('Cedar','Terrain')) for o in bpy.data.objects)
 return {'status':'PASS','ornaments':len(flowers),'petals':32,'hearts':5,'leaves':8,'min_z':min(v.z for v in bounds),'max_z':max(v.z for v in bounds)}
r=check()
o=next(o for o in bpy.data.objects if o.name.startswith('Floral /'));o.parent=None
try:check()
except AssertionError:r['detached_ornament_negative_control']='rejected as required'
else:raise AssertionError('Negative control falsely accepted')
# Independently open original mechanism and compare evaluated pivot matrices.
o.parent=lid;bpy.context.view_layer.update()
actual={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,m in actual.items():
 expected=bpy.data.objects[name].matrix_world
 assert max(abs(m[i][j]-expected[i][j]) for i in range(4) for j in range(4))<1e-6
r['original_pivots']='PASS';(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
