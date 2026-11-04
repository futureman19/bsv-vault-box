import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'qatar.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def contract():
 dunes=[o for o in bpy.data.objects if o.name.startswith('Dune /')];assert len(dunes)==3
 water=bpy.data.objects['Tidal inlet / continuous blue ribbon'];assert water.parent==lid
 for o in dunes:
  assert o.parent==lid
  vs=[o.matrix_world@v.co for v in o.data.vertices];h=max(v.z for v in vs)-2.02
  assert .15<=h<=.40,h
  assert all(p.normal.z>.0 for p in o.data.polygons[:48*16])
 assert len(water.data.polygons)==64
 assert len([i for i in bpy.data.images if i.packed_file])>=3
 return {'dunes':len(dunes),'tidal_faces':64,'lid_ancestry':True,'dune_relief':True,'upward_top_normals':True}
result=contract()
water=bpy.data.objects['Tidal inlet / continuous blue ribbon'];water.parent=None
try:contract()
except AssertionError:result['detached_inlay_negative_control']='REJECTED as required'
else:raise AssertionError('Negative control did not fail')
water.parent=lid
# Compare pivot local matrices against independently reopened mechanical base.
current={o.name:list(v for row in o.matrix_local for v in row) for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,values in current.items():
 baseline=[v for row in bpy.data.objects[name].matrix_local for v in row];assert max(abs(a-b) for a,b in zip(values,baseline))<1e-6
result['original_pivots_preserved']=True;result['status']='PASS'
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
