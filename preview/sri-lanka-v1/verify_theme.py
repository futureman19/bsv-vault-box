import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'sri-lanka.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
orn=[o for o in bpy.data.objects if o.name.startswith('Weave diamond')]
def check_ancestry(objects):
 assert len(objects)==36
 assert all(o.parent==lid for o in objects),'detached ornament'
check_ancestry(orn)
# Deliberate regression control in memory only, saved source remains unchanged.
p=orn[0].parent;orn[0].parent=None
try:check_ancestry(orn)
except AssertionError:negative=True
else:raise AssertionError('Detached ornament not rejected')
orn[0].parent=p;bpy.context.view_layer.update()
v=[o.matrix_world@v.co for o in orn for v in o.data.vertices]
lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
assert lo[0]>=-1.45 and hi[0]<=1.45 and lo[1]>=-.8 and hi[1]<=.8
assert lo[2]<=1.997 and hi[2]-1.978<.20,(lo,hi)
# Gaps remain genuine open space between nested raised threads.
for cx in [-.92,0,.92]:
 hit,loc,n,i,o,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((cx,0,2.3)),Vector((0,0,-1)))
 assert hit and o.name=='Weave / lid panel',(cx,o.name)
panels=[o for o in bpy.data.objects if o.name.startswith('Weave / broad')];assert len(panels)==4
front=next(o for o in panels if o.location.y< -1)
assert front.dimensions.x>=3.2 and front.dimensions.z>=1.19
seams=[o for o in bpy.data.objects if 'seam' in o.name.lower()];assert seams and all(o.dimensions.z<=.12 for o in seams)
# Compare independently evaluated original pivot matrices, not inferred names.
actual={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,rows in actual.items():
 assert max(abs(rows[i][j]-bpy.data.objects[name].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-6
result={'status':'PASS','raised_segments':len(orn),'ornament_bounds':[lo,hi],'three_open_centres':True,'four_large_inset_panels':True,'seam_max_height':.12,'original_pivot_matrices':True,'detached_ornament_negative_control_rejected':negative}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print('THEME PASS',result)
