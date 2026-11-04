import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
names=['Lid_Hinge','Latch_Pivot']
def sample(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False);bpy.context.view_layer.update()
 return {n:{'matrix':[float(x) for row in bpy.data.objects[n].matrix_world for x in row],'parent':bpy.data.objects[n].parent.name if bpy.data.objects[n].parent else None} for n in names}
a=sample(R/'mechanism.blend');b=sample(R/'new-zealand.blend');assert a==b,(a,b)
(R/'pivot-check.json').write_text(json.dumps({'status':'PASS','exact_inherited_pivots':b},indent=2));print('PIVOT PASS: exact inherited matrices and parents')
