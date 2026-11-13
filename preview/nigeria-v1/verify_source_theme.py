import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
base={n:list(bpy.data.objects[n].matrix_local) for n in ['Lid_Hinge','Latch_Pivot']}
base={n:[[float(v) for v in row] for row in m] for n,m in base.items()}
bpy.ops.wm.open_mainfile(filepath=str(R/'nigeria.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in base.items():assert max(abs(bpy.data.objects[n].matrix_local[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
lid=bpy.data.objects['Lid_Hinge'];discs=[o for o in bpy.data.objects if o.name.startswith('Resist / raised indigo disc')];assert len(discs)==3
for o,x in zip(sorted(discs,key=lambda o:o.matrix_world.translation.x),[-1.05,0,1.05]):
 assert o.parent==lid and abs(o.matrix_world.translation.x-x)<1e-6
 assert abs(o.dimensions.x-.64)<1e-5 and abs(o.matrix_world.translation.z-1.994)<1e-5
slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<1e-5 for a,b in zip(slab.dimensions,[3.72,2.38,.30]))
(R/'source-theme-check.json').write_text(json.dumps({'status':'PASS','original_pivot_matrices':base,'three_discs_seated':True,'lid_dimensions':[3.72,2.38,.30],'brief_deviation':'Disc radius .32 rather than stated center radius .25; outer brass radius .29 retained. This broadens the enamel backing.'},indent=2));print('SOURCE_THEME_PASS')
