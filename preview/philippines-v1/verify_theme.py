import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'philippines.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge']
def check():
 tiers=[o for o in bpy.data.objects if o.name.startswith('Terrace / retaining')];fields=[o for o in bpy.data.objects if o.name.startswith('Paddy / field')]
 assert len(tiers)==len(fields)==6
 heights=[];widths=[]
 for k in range(6):
  o=bpy.data.objects['Terrace / retaining '+str(k)];f=bpy.data.objects['Paddy / field '+str(k)]
  assert o.parent==lid and f.parent==lid,'Ornament detached from lid'
  vs=[o.matrix_world@v.co for v in o.data.vertices];fs=[f.matrix_world@v.co for v in f.data.vertices]
  z=max(v.z for v in vs);assert abs(z-(2.08+k*.1))<1e-5
  assert abs(max(v.z for v in fs)-z-.006)<1e-5
  widths.append(max(v.x for v in vs)-min(v.x for v in vs));heights.append(z)
  assert all(-1.5<v.x<1.5 and -.9<v.y<1 for v in vs)
 assert all(a>b for a,b in zip(widths,widths[1:]))
 return dict(tiers=6,fields=6,heights=heights,widths=widths,lid_ancestry=True)
r=check();o=bpy.data.objects['Paddy / field 0'];o.parent=None
try:check()
except AssertionError as e:r['negative_control']={'detached_field_rejected':True,'error':str(e)}
else:raise AssertionError('Negative control failed to reject')
o.parent=lid
r['status']='PASS';(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
