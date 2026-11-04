import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
snap={}
for name in ['mechanism.blend','nauru.blend']:
 bpy.ops.wm.open_mainfile(filepath=str(R/name),use_scripts=False);bpy.context.view_layer.update()
 snap[name]={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
assert snap['mechanism.blend']==snap['nauru.blend']
(R/'pivot-check.json').write_text(json.dumps({'status':'PASS','pivots_identical':True,'matrices':snap},indent=2));print('PASS: original pivot matrices preserved')
