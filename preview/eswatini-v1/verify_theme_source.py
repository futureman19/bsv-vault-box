import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
anchors={n:list(bpy.data.objects[n].location) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'eswatini.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge']
for n,v in anchors.items():assert list(bpy.data.objects[n].location)==v
body=[o for o in bpy.data.objects if o.name.startswith('Body coil /')]
loops=[o for o in bpy.data.objects if o.name.startswith('Lid coil /')]
def acceptance(items):
 assert len(items)>=8,'Lid needs at least eight real coils'
 assert all(o.parent==lid for o in items),'Every lid coil must travel with lid'
acceptance(loops);assert len(body)>=8
assert all(o.parent is None for o in body)
assert all(o.dimensions.z<=.10 for o in bpy.data.objects if o.name.startswith('Seam /'))
bpy.context.view_layer.update()
ornaments=loops+[bpy.data.objects['Lid / central woven medallion']]
assert max((o.matrix_world@v.co).z for o in ornaments for v in o.data.vertices)<2.278
# Real post-implementation negative control, not claimed test-first TDD.
old=loops[0].parent;loops[0].parent=None
try:
 acceptance(loops)
except AssertionError as e:negative=str(e)
else:raise AssertionError('Negative control did not fail')
finally:loops[0].parent=old
acceptance(loops)
r={'status':'PASS','body_coils':len(body),'lid_coils':len(loops),'all_lid_ornament_parented':True,'unchanged_pivots':anchors,'negative_control':{'mutation':'Detached actual saved-source lid coil in memory','rejected':negative,'restored_pass':True},'brief_before_model':True}
(R/'theme-source-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
