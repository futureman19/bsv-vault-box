import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'north-macedonia.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];lake=bpy.data.objects['Lake / continuous blue inset'];shore=bpy.data.objects['Shore / irregular limestone'];ridge=[o for o in bpy.data.objects if o.name.startswith('Ridge /')]
def check():
 assert lake.parent==lid and shore.parent==lid and len(ridge)==3 and all(o.parent==lid for o in ridge)
 assert 2.4<lake.dimensions.x<2.9 and 1.2<lake.dimensions.y<1.6
 assert all(max((o.matrix_world@v.co).z for v in o.data.vertices)<2.55 for o in ridge)
 assert not any(o.name.startswith('Cedar tree') for o in bpy.data.objects)
check();lake.parent=None
try:check()
except AssertionError:negative=True
else:raise AssertionError('Detached lake accepted')
lake.parent=lid;check()
r={'status':'PASS','lake_and_shore_lid_parented':True,'ridge_parts':len(ridge),'detached_lake_negative_control_rejected':negative,'interpretation':'stylized lake, not geographic survey'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS')
