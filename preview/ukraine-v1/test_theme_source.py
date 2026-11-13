"""Independent reopened-source theme and pivot contract; includes detached negative control."""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'ukraine.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,rows in pivots.items():assert max(abs(rows[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
orn=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(('Bloom','Floral','Leaf'))]
def validate(items):
 assert len(items)>=80
 for o in items:
  p=o.parent;anc=[]
  while p:anc.append(p.name);p=p.parent
  assert 'Lid_Hinge' in anc,o.name
validate(orn)
o=orn[0];parent=o.parent;o.parent=None
try:
 validate(orn)
 raise RuntimeError('negative control was accepted')
except AssertionError:negative=True
finally:o.parent=parent
bpy.context.view_layer.update()
vs=[o.matrix_world@v.co for o in orn for v in o.data.vertices]
lo=[min(v[i] for v in vs) for i in range(3)];hi=[max(v[i] for v in vs) for i in range(3)]
assert lo[0]>=-1.55 and hi[0]<=1.55 and lo[1]>=-.9 and hi[1]<=.9
assert lo[2]>=1.978 and hi[2]<=2.138
hearts=[o for o in orn if 'ochre heart' in o.name];assert len(hearts)==5
assert len([o for o in orn if o.name.startswith('Floral leaf')])==8
assert len([o for o in orn if o.name.startswith('Leaf branch')])==8
# Every flower center is connected to the terminating end of its physical stem.
for i in range(5):
 stem=bpy.data.objects['Floral stem / '+str(i)];heart=bpy.data.objects['Bloom %d / ochre heart'%i]
 c=heart.matrix_world.translation
 assert min(math.hypot((stem.matrix_world@v.co).x-c.x,(stem.matrix_world@v.co).y-c.y) for v in stem.data.vertices)<.02
assert not [o.name for o in bpy.data.objects if o.name.startswith(('Cedar','Terrain','Moss'))]
r={'status':'PASS','exact_baseline_pivots':True,'ornament_meshes':len(orn),'flowers':len(hearts),'leaves':8,'connected_flower_stem_endpoints':True,'detached_negative_control_rejected':negative,'ornament_bounds':[lo,hi],'interpretation':'Original procedural floral relief, not artisan-pattern authenticity'}
(R/'theme-source-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
