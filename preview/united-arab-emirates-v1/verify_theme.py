from pathlib import Path
import bpy,json
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'uae.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];diamonds=[o for o in bpy.data.objects if o.name.startswith('Loom / diamond')]
assert len(diamonds)==28
assert all(o.parent==lid for o in diamonds)
for o in diamonds:
 coords=[o.matrix_world@v.co for v in o.data.vertices]
 assert all(abs(v.x)<1.3 and abs(v.y)<.34 and 2.02<v.z<2.07 for v in coords)
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(m[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
r={'status':'PASS','diamond_segments':len(diamonds),'diamonds':7,'lid_parentage':True,'relief_bounds':True,'original_pivot_matrices':True}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(r)
