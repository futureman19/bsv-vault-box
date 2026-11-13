import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
baseline={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'argentina.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in baseline.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
ridge=bpy.data.objects['Terrain / Quebrada folded ridge'];lid=bpy.data.objects['Lid_Hinge']
def ownership():assert ridge.parent==lid,'Relief detached from lid'
ownership();ridge.parent=None
try:ownership();raise RuntimeError('Negative control was not rejected')
except AssertionError as e:negative=str(e)
ridge.parent=lid;bpy.context.view_layer.update()
v=[ridge.matrix_world@p.co for p in ridge.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
assert abs(lo[2]-1.978)<1e-5 and 2.4<hi[2]<2.80
assert abs(lo[0]+1.4)<1e-5 and abs(hi[0]-1.4)<1e-5
assert len(set(p.material_index for p in ridge.data.polygons))==6
r={'status':'PASS','pivot_parity':True,'relief_lid_owned':True,'ridge_bounds':[lo,hi],'mineral_bands':6,'detached_negative_control':negative,'reference':'written brief, regional interpretation not topographic replica'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
