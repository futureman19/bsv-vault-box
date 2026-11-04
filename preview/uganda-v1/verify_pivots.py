import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
def snapshot(file):
 bpy.ops.wm.open_mainfile(filepath=str(R/file),use_scripts=False);bpy.context.view_layer.update()
 return {n:{'parent':bpy.data.objects[n].parent.name if bpy.data.objects[n].parent else None,'matrix':[list(r) for r in bpy.data.objects[n].matrix_world]} for n in ['Lid_Hinge','Latch_Pivot']}
a=snapshot('mechanism.blend');b=snapshot('uganda.blend');assert a==b
(R/'pivot-check.json').write_text(json.dumps({'status':'PASS','exact_inherited_world_matrices':True,'pivots':b},indent=2));print('PIVOT_CHECK PASS')
