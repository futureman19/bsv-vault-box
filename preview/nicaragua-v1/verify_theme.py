import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'nicaragua.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge']
def validate():
 for n in ['Lake / inset','Island / connected isthmus','Volcano / Concepcion crater','Volcano / Maderas crater']:
  assert bpy.data.objects[n].parent==lid,n
 for n,x,h in [('Volcano / Concepcion crater',-.65,.65),('Volcano / Maderas crater',.65,.45)]:
  o=bpy.data.objects[n];v=[o.matrix_world@v.co for v in o.data.vertices]
  assert len(v)==256
  rim=sum(p.z for p in v[128:192])/64;floor=sum(p.z for p in v[192:])/64
  assert rim-floor>.12,(rim,floor)
  assert abs(rim-(2.04+h))<.02
validate()
o=bpy.data.objects['Volcano / Maderas crater'];o.parent=None
try:validate();raise RuntimeError('Negative control did not fail')
except AssertionError as e:negative=str(e)
o.parent=lid;validate()
r={'status':'PASS','two_recessed_craters':True,'all_landscape_lid_owned':True,'detached_ornament_negative_control_rejected':negative,'note':'Regression control, not preimplementation TDD; sculptural interpretation not geography.'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(r)
