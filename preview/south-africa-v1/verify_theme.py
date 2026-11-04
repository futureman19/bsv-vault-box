import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'south-africa.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot'];mesa=bpy.data.objects['Terrain / Table Mountain mesa']
def attached():
 assert mesa.parent==lid,'Mesa must travel with lid'
attached();mesa.parent=None
try:attached()
except AssertionError:negative=True
else:raise AssertionError('Detached negative control accepted')
mesa.parent=lid;bpy.context.view_layer.update()
v=[mesa.matrix_world@x.co for x in mesa.data.vertices];top=v[-40:]
assert 2.65<min(p.z for p in top)<max(p.z for p in top)<2.75
assert max(p.x for p in v)-min(p.x for p in v)>2
assert max(p.y for p in v)-min(p.y for p in v)>.8
plants=[o for o in bpy.data.objects if o.name.startswith('Fynbos /')];assert len(plants)>=25 and all(o.parent==lid for o in plants)
assert all(i.packed_file for i in bpy.data.images if i.name.endswith('.png'))
pivots={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(m[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-6
out={'status':'PASS','mesa_top_z':[min(p.z for p in top),max(p.z for p in top)],'fynbos_clusters':len(plants),'detached_negative_control_rejected':negative,'original_pivot_matrices_preserved':True}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(out)
