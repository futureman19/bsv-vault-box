import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'latvia.blend'),use_scripts=False)
bpy.context.view_layer.update()
def bounds(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();v=[o.matrix_world@x.co for x in m.vertices];ev.to_mesh_clear();return [[min(x[i] for x in v),max(x[i] for x in v)] for i in range(3)]
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot'];assert latch.parent==lid
panel=bpy.data.objects['Linen / raised woven panel'];assert panel.parent==lid
b=bounds(panel);assert abs(b[0][1]-b[0][0]-2.95)<1e-5 and abs(b[1][1]-b[1][0]-1.65)<1e-5
assert abs(b[2][0]-1.981)<1e-5 and abs(b[2][1]-2.011)<1e-5
stones=sorted([o for o in bpy.data.objects if o.name.startswith('Amber / cabochon')],key=lambda o:o.matrix_world.translation.x)
def ornament_gate(objects):
 assert len(objects)==3,'Requires exactly three cabochons'
 for o,x in zip(objects,[-.9,0,.9]):
  assert o.parent==lid and abs(o.matrix_world.translation.x-x)<1e-5
  bb=bounds(o);assert abs(bb[0][1]-bb[0][0]-.36)<1e-5 and bb[2][1]<2.16
ornament_gate(stones)
try:ornament_gate(stones[:-1])
except AssertionError as e:negative={'status':'EXPECTED_FAIL','reason':str(e)}
else:raise AssertionError('Missing ornament negative accepted')
assert not any(o.name.startswith(('Cedar tree','Terrain / moss')) for o in bpy.data.objects)
current={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in current.items():assert max(abs(m[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
out={'status':'PASS','panel_bounds':b,'cabochons':3,'lid_ancestry':True,'same_mechanism_pivots':True,'negative_control':negative,'no_inherited_country_ornament':True}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
