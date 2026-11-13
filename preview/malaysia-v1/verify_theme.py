import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'malaysia.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def check_threads():
 threads=[o for o in bpy.data.objects if o.name.startswith('Songket thread /')]
 assert len(threads)==60,len(threads)
 assert all(o.parent==lid for o in threads)
 vs=[o.matrix_world@v.co for o in threads for v in o.data.vertices]
 assert max(abs(v.x) for v in vs)<1.55 and max(abs(v.y) for v in vs)<.85
 assert min(v.z for v in vs)>=1.99 and max(v.z for v in vs)<2.08
 return {'edges':len(threads),'diamonds':len(threads)//4,'min_z':min(v.z for v in vs),'max_z':max(v.z for v in vs)}
r=check_threads();obj=next(o for o in bpy.data.objects if o.name.startswith('Songket thread /'));obj.parent=None
try:check_threads();raise RuntimeError('Negative control incorrectly accepted')
except AssertionError:r['detached_thread_negative_control']='REJECTED'
obj.parent=lid
pivots={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(m[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
r.update(status='PASS',pivots_unchanged=True,negative_control_type='postimplementation regression')
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(r)
