import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'monaco.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
assert (lid.location-Vector((0,1.32,1.668))).length<1e-5,tuple(lid.location)
objects=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(('Riviera /','Old town /','Garden /','Rock /'))]
def check_ancestry():
 assert all(o.parent==lid for o in objects),'Every ornament must belong to lid'
check_ancestry()
negative=objects[0];negative.parent=None
try:
 check_ancestry()
except AssertionError as e:
 negative_result={'status':'EXPECTED_FAIL','mutation':'Detached '+negative.name,'error':str(e)}
else:raise AssertionError('Ancestry negative control failed to reject')
negative.parent=lid;check_ancestry()
(R/'theme-negative-control.json').write_text(json.dumps(negative_result,indent=2))
max_z=max((o.matrix_world@v.co).z for o in objects for v in o.data.vertices)
assert max_z<3.0,max_z
assert len([o for o in objects if o.name.startswith('Old town / roof')])==7
assert len([o for o in objects if o.name.startswith('Garden /')])==6
assert bpy.data.objects['Riviera / sea inset'].dimensions.x>3.1
# Independently reopen inherited mechanism to compare exact pivots.
actual={o.name:{'location':list(o.location),'rotation':list(o.rotation_euler),'scale':list(o.scale)} for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,data in actual.items():
 o=bpy.data.objects[name]
 for key,attr in [('location','location'),('rotation','rotation_euler'),('scale','scale')]:assert max(abs(a-b) for a,b in zip(data[key],getattr(o,attr)))<1e-7
out={'status':'PASS','ornaments':len(objects),'ornament_max_z':max_z,'roofs':7,'gardens':6,'lid_ancestry':True,'original_pivots_preserved':actual,'negative_control_rejected':True}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
