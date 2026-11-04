import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
def capture(file):
 bpy.ops.wm.open_mainfile(filepath=str(R/file),use_scripts=False);bpy.context.view_layer.update()
 return {n:{'matrix':[list(row) for row in bpy.data.objects[n].matrix_world],'parent':bpy.data.objects[n].parent.name if bpy.data.objects[n].parent else None} for n in ['Lid_Hinge','Latch_Pivot']}
a=capture('mechanism.blend');b=capture('myanmar.blend');assert a==b
(R/'pivot-check.json').write_text(json.dumps({'status':'PASS','exact_inherited_pivots':a},indent=2));print('PIVOT PASS')
