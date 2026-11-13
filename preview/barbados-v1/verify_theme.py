import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'barbados.blend'),use_scripts=False)
bpy.context.view_layer.update()
def check():
 lid=bpy.data.objects['Lid_Hinge']; terraces=[bpy.data.objects['Terrace / '+n] for n in ['lower','middle','upper']]
 assert all(o.parent==lid for o in terraces)
 heights=[max((o.matrix_world@v.co).z for v in o.data.vertices) for o in terraces]
 assert all(abs(a-b)<1e-5 for a,b in zip(heights,[2.16,2.32,2.49]))
 assert bpy.data.objects['Coast / turquoise inlay'].parent==lid
 assert max(heights)-1.978<.65
 assert len([o for o in bpy.data.objects if o.name.startswith('Limestone foot')])==4
 return heights
heights=check();o=bpy.data.objects['Terrace / upper'];parent=o.parent;o.parent=None
try:
 check()
except AssertionError: negative=True
else: raise AssertionError('detached terrace negative control not detected')
o.parent=parent
# Independently open baseline, compare evaluated pivot matrices.
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
error=max(abs(pivots[n][i][j]-bpy.data.objects[n].matrix_world[i][j]) for n in pivots for i in range(4) for j in range(4));assert error<1e-6
r={'status':'PASS','terrace_top_z':heights,'all_terrain_lid_owned':True,'detached_terrace_negative_rejected':negative,'baseline_pivot_max_error':error}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(r)
