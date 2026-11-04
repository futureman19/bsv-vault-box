import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'liechtenstein.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];peaks=[o for o in bpy.data.objects if o.name.startswith('Three Sisters / peak')]
if '--negative' in sys.argv:peaks[0].parent=None
bpy.context.view_layer.update()
def check():
 assert len(peaks)==3
 bounds=[]
 for o in peaks:
  assert o.parent==lid, 'Peak detached from lid'
  vs=[o.matrix_world@v.co for v in o.data.vertices];mn=[min(v[i] for v in vs) for i in range(3)];mx=[max(v[i] for v in vs) for i in range(3)]
  assert 1.99<mn[2]<2.06 and 2.60<mx[2]<3.0
  bounds.append({'name':o.name,'min':mn,'max':mx})
 assert all(peaks[i].matrix_world!=None for i in range(3))
 # Exact inherited mechanical pivots, not guessed origins.
 matrices={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
 bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
 for n,m in matrices.items():
  assert max(abs(m[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
 return {'status':'PASS','three_peaks':bounds,'all_lid_parented':True,'inherited_pivots_unchanged':True}
r=check();(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
