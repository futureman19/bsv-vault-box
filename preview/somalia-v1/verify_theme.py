import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'somalia.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def check():
 ridges=[o for o in bpy.data.objects if o.name.startswith('Merka dune / ridge')]
 assert len(ridges)==3, 'Exactly three dune ridges required'
 values=[]
 for o in ridges:
  assert o.parent==lid
  vs=[o.matrix_world@v.co for v in o.data.vertices]
  lo=[min(v[i] for v in vs) for i in range(3)];hi=[max(v[i] for v in vs) for i in range(3)]
  assert lo[0]>-1.6 and hi[0]<1.6 and lo[1]>-.9 and hi[1]<.9
  assert 2.15<hi[2]<2.40 and 1.99<lo[2]<2.01
  values.append({'name':o.name,'min':lo,'max':hi})
 assert bpy.data.objects['Ocean / inlay'].parent==lid
 assert bpy.data.objects['Shore / coastal edge'].parent==lid
 assert not any('Cedar' in o.name or 'moss' in o.name.lower() for o in bpy.data.objects)
 return values
values=check();o=bpy.data.objects['Merka dune / ridge 0'];o.name='Negative control missing ridge'
try:check()
except AssertionError as e:negative=str(e)
else:raise AssertionError('Negative control did not fail')
o.name='Merka dune / ridge 0';check()
# Exact baseline pivots captured independently from the included mechanism.
pivots={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,matrix in pivots.items():
 assert max(abs(matrix[i][j]-bpy.data.objects[name].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
out={'status':'PASS','ridge_bounds':values,'all_ornaments_lid_parented':True,'baseline_pivots_equal':True,'negative_control':{'result':'EXPECTED FAIL','message':negative,'restored_result':'PASS'}}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print('THEME PASS',json.dumps(out))
