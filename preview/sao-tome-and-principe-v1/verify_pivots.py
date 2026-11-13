import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
names=['Lid_Hinge','Latch_Pivot']
def records(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False);bpy.context.view_layer.update()
 return {n:{'parent':bpy.data.objects[n].parent.name if bpy.data.objects[n].parent else None,'matrix':[float(v) for row in bpy.data.objects[n].matrix_world for v in row]} for n in names}
a=records(R/'mechanism.blend');b=records(R/'sao-tome-and-principe.blend')
assert a==b,(a,b)
r={'status':'PASS','same_baseline_pivots':True,'pivots':b};(R/'pivot-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
