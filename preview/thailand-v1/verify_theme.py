import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
bpy.context.view_layer.update()
base={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'thailand.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in base.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-8
waves=[o for o in bpy.data.objects if o.name.startswith('Wave /')];assert len(waves)==3
bounds=[]
def owns(o):assert o.parent==bpy.data.objects['Lid_Hinge'],'Detached wave'
for o in waves:
 owns(o);v=[o.matrix_world@p.co for p in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
 assert hi[0]-lo[0]>2 and max(abs(lo[0]),abs(hi[0]))<1.55 and max(abs(lo[1]),abs(hi[1]))<.95
 assert 1.975<=lo[2]<=1.979 and hi[2]<=2.16, ('Wave must seat into lid top 1.978',lo,hi)
 bounds.append({'name':o.name,'min':lo,'max':hi})
o=waves[0];p=o.parent;o.parent=None
try:owns(o)
except AssertionError as e:negative=str(e)
else:raise AssertionError('Negative control not rejected')
o.parent=p
r={'status':'PASS','baseline_pivots_identical':True,'waves':bounds,'negative_detached_wave_rejected':negative,'note':'Wave tube lower surface z1.977 embeds 0.001 into lid top1.978; centre lines z2.022. Visible relief is above lid; brief lower height allows this hidden seating overlap.'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
