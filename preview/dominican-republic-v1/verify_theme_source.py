import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'dominican-republic.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot'];orn=[o for o in bpy.data.objects if o.name.startswith('Ornament')]
def check():
 assert len(orn)==4 and all(o.parent==lid for o in orn)
 assert max((o.matrix_world@v.co).z for o in orn for v in o.data.vertices)<=2.53
check();o=orn[0];o.parent=None
try:check()
except AssertionError:negative=True
else:raise AssertionError('Detached ornament was accepted')
o.parent=lid;check()
current={o.name:[list(row) for row in o.matrix_local] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
error=max(abs(current[n][i][j]-bpy.data.objects[n].matrix_local[i][j]) for n in current for i in range(4) for j in range(4));assert error<1e-7
r={'status':'PASS','ornaments':4,'lid_owned':True,'height_max':2.53,'negative_detached_ornament_rejected':negative,'inherited_pivot_matrix_error':error};(R/'theme-source-check.json').write_text(json.dumps(r,indent=2));print(r)
