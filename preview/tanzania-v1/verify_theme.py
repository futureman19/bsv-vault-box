import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'tanzania.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot'];o=bpy.data.objects['Terrain / Kibo crater and shoulder']
if '--negative' in sys.argv:o.parent=None
assert o.parent==lid,'Terrain detached from lid'
v=[o.matrix_world@x.co for x in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
assert hi[0]-lo[0]<2.75 and hi[1]-lo[1]<1.70,(lo,hi)
assert 2.78<hi[2]<2.96 and 1.96<lo[2]<1.98
assert max(p.z for p in v)-v[-1].z>.18,'Missing crater bowl'
assert len(o.data.materials)==3
pivots={x.name:[list(row) for row in x.matrix_world] for x in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(m[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-6
out={'status':'PASS','terrain_bounds':[lo,hi],'crater_depth':hi[2]-v[-1].z,'lid_ancestry':True,'inherited_pivots_exact':True,'three_slope_materials':True}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
