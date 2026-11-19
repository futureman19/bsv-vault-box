import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'lithuania.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];o=bpy.data.objects['Dune / continuous ridge']
vs=[o.matrix_world@v.co for v in o.data.vertices];assert o.parent==lid
assert abs(min(v.x for v in vs)+1.4)<1e-5 and abs(max(v.x for v in vs)-1.4)<1e-5
assert 2.30<max(v.z for v in vs)<2.48
plants=[o for o in bpy.data.objects if o.name.startswith('Vegetation /')];assert len(plants)==22 and all(o.parent==lid for o in plants)
assert bpy.data.objects['Lagoon / inset'].parent==lid
# Compare inherited pivots against a separately reopened mechanism, not guessed transforms.
names=['Lid_Hinge','Latch_Pivot'];current={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in names}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n in names:assert max(abs(current[n][i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-6
result={'status':'PASS','dune_x':[-1.4,1.4],'dune_max_z':max(v.z for v in vs),'vegetation_meshes':22,'all_ornaments_lid_owned':True,'inherited_pivots_exact':True}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print('THEME PASS',result)
