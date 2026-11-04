import bpy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'saudi-arabia.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge']
rocks=[o for o in bpy.data.objects if o.name.startswith('AlUla / outcrop')]
if '--negative' in sys.argv:rocks[0].parent=None
try:
 assert len(rocks)==3
 result=[]
 for o in rocks:
  assert o.parent==lid,'Outcrop must travel with lid'
  v=[o.matrix_world@v.co for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
  assert abs(lo[2]-1.97)<1e-5 and 2.45<hi[2]<3.05
  result.append({'name':o.name,'min':lo,'max':hi})
 for a,b in zip(sorted(result,key=lambda a:a['min'][0]),sorted(result,key=lambda a:a['min'][0])[1:]):assert a['max'][0]<b['min'][0], 'Outcrops must be separated'
 assert not any(o.name.startswith(('Cedar','Finger','Terrain / moss')) for o in bpy.data.objects)
 assert len([i for i in bpy.data.images if i.packed_file])>=3
 # Compare evaluated mechanism pivot transforms with the included frozen base.
 pivots={n:list(bpy.data.objects[n].matrix_world.translation) for n in ['Lid_Hinge','Latch_Pivot']}
 bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
 for n,xyz in pivots.items():assert max(abs(a-b) for a,b in zip(xyz,bpy.data.objects[n].matrix_world.translation))<1e-6
 assert '--negative' not in sys.argv,'Negative control failed to reject detached rock'
 report={'status':'PASS','outcrops':result,'pivots_preserved':pivots,'source_maps_packed':True}
 (R/'theme-check.json').write_text(json.dumps(report,indent=2));print('THEME PASS')
except AssertionError as e:
 if '--negative' not in sys.argv:raise
 assert str(e)=='Outcrop must travel with lid',str(e)
 (R/'negative-control.json').write_text(json.dumps({'status':'PASS','mutant':'detached lid outcrop','rejected_by':str(e)},indent=2));print('NEGATIVE CONTROL PASS: detached outcrop rejected')
