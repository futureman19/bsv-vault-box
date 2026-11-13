import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
states=[]
for name in ['mechanism.blend','indonesia.blend']:
 bpy.ops.wm.open_mainfile(filepath=str(R/name),use_scripts=False);bpy.context.view_layer.update()
 states.append({n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']})
assert states[0]==states[1]
r={'status':'PASS','exact_baseline_pivot_matrices':True,'matrices':states[1]};(R/'pivot-check.json').write_text(json.dumps(r,indent=2));print(r)
