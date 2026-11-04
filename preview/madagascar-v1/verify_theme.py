"""Independent saved-source theme and exact inherited pivot checks."""
import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
def pivot(n):
 o=bpy.data.objects[n];return {'location':list(o.location),'rotation':list(o.rotation_euler),'parent':o.parent.name if o.parent else None}
expected={n:pivot(n) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'madagascar.blend'),use_scripts=False)
assert expected=={n:pivot(n) for n in expected}
lid=bpy.data.objects['Lid_Hinge'];peaks=[o for o in bpy.data.objects if o.name.startswith('Tsingy / pinnacle')];green=[o for o in bpy.data.objects if o.name.startswith('Forest / gully')]
def contract(ps,gs):
 assert len(ps)>=18 and len(gs)>=6
 assert all(o.parent==lid for o in ps+gs)
 for o in ps:
  z=[(o.matrix_world@v.co).z for v in o.data.vertices];assert min(z)<1.98 and .18<=max(z)-1.98<=.68
contract(peaks,green)
negative=[]
try:contract([],green)
except AssertionError:negative.append('missing pinnacles rejected')
else:raise AssertionError('negative control failed')
old=peaks[0].parent;peaks[0].parent=None
try:contract(peaks,green)
except AssertionError:negative.append('detached pinnacle rejected')
else:raise AssertionError('negative control failed')
peaks[0].parent=old
assert not any('Cedar' in o.name or 'Glacier' in o.name for o in bpy.data.objects)
r={'status':'PASS','pivots':expected,'pinnacles':len(peaks),'green_patches':len(green),'negative_controls':negative,'height_range_above_lid':[min(max((o.matrix_world@v.co).z for v in o.data.vertices)-1.98 for o in peaks),max(max((o.matrix_world@v.co).z for v in o.data.vertices)-1.98 for o in peaks)]}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
