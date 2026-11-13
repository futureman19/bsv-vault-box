import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'serbia.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def contract(objects):
 relief=[o for o in objects if o.name.startswith('Pirot relief')]
 assert len(relief)==6,len(relief)
 for o in relief:
  assert o.parent==lid
  vs=[o.matrix_world@v.co for v in o.data.vertices]
  idx=int(o.name[-1]);cx=[-1,0,1][idx]
  assert abs((min(v.x for v in vs)+max(v.x for v in vs))/2-cx)<1e-5
  assert max(v.z for v in vs)<=2.04601 and min(v.z for v in vs)>=2.00299
  assert max(v.x for v in vs)-min(v.x for v in vs)<=.68001
 for key in ['Textile / lid','Lid / polished slab']:assert bpy.data.objects[key].parent==lid
 assert len([o for o in objects if o.name.startswith('Textile /')])==5
 assert not any(any(t in o.name.lower() for t in ['cedar','granite','moss','glacier']) for o in objects)
contract(list(bpy.data.objects));negative=False
try:contract([o for o in bpy.data.objects if o.name!='Pirot relief / ivory 0'])
except AssertionError:negative=True
assert negative
# Compare actual updated original source pivot matrices, not appended unlinked objects.
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<1e-5 for a,b in zip(slab.dimensions,[3.72,2.38,.30]))
for o in bpy.data.objects:
 if o.name.startswith('Dark seam'):assert o.dimensions.z<.12
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
err=max(abs(pivots[n][i][j]-bpy.data.objects[n].matrix_world[i][j]) for n in pivots for i in range(4) for j in range(4));assert err<1e-7
result={'status':'PASS','reliefs':6,'textile_panels':5,'lid_ancestry':True,'slab_dimensions':[3.72,2.38,.30],'pivot_max_error':err,'missing_relief_negative_control_rejected':negative,'seam_under_0_12':True}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
