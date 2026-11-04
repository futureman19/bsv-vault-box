import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
names=['Lid_Hinge','Latch_Pivot'];base={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in names}
bpy.ops.wm.open_mainfile(filepath=str(R/'russia.blend'),use_scripts=False);bpy.context.view_layer.update()
assert base=={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in names}
slabs=[o for o in bpy.data.objects if o.name.startswith('Ice slab /')]
def check(items):
 assert len(items)==7
 for o in items:
  assert o.parent and o.parent.name=='Lid_Hinge'
  for v in o.data.vertices:
   p=o.matrix_world@v.co;assert abs(p.x)<1.6 and abs(p.y)<.95 and 1.97<p.z<2.55
check(slabs)
old=slabs[0].parent;slabs[0].parent=None
try:
 check(slabs)
except AssertionError: rejected=True
else: rejected=False
slabs[0].parent=old
assert rejected
r={'status':'PASS','slabs':7,'lid_ancestry':True,'bounds':True,'exact_inherited_pivots':True,'detached_negative_control_rejected':rejected}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(r)
