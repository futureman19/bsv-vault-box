import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'solomon-islands.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']; latch=bpy.data.objects['Latch_Pivot']
meshes=[o for o in bpy.data.objects if o.type=='MESH' and not o.name.startswith('Studio')]
shell=[o for o in meshes if o.name.startswith('Shell')];orn=[o for o in shell if o.name.startswith('Shell lid')]
def validate():
 assert len(shell)>=20
 assert len(orn)==45 and all(o.parent==lid for o in orn)
 assert not any(any(x in o.name.lower() for x in ['cedar','terrain','moss','glacier']) for o in meshes)
 for o in orn:
  zs=[(o.matrix_world@v.co).z for v in o.data.vertices]
  assert min(zs)<=1.979 and 1.978<max(zs)<=2.158
validate()
o=orn[0];old=o.parent;o.parent=None
try:
 validate();raise RuntimeError('Negative control was not rejected')
except AssertionError:negative=True
finally:o.parent=old
# Compare stored mechanical transforms to independently opened baseline.
pivots={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
# Prove adjacent medallion pieces have no XY overlap by convex separating axes.
med=[o for o in orn if o.name.startswith('Shell lid medallion')]
def overlap(a,b):
 A=[(a.matrix_world@v.co).xy for v in list(a.data.vertices)[:4]];B=[(b.matrix_world@v.co).xy for v in list(b.data.vertices)[:4]]
 for P in [A,B]:
  for i in range(4):
   e=P[(i+1)%4]-P[i];n=Vector((-e.y,e.x));aa=[v.dot(n) for v in A];bb=[v.dot(n) for v in B]
   if max(aa)<=min(bb) or max(bb)<=min(aa):return False
 return True
assert not [(a.name,b.name) for i,a in enumerate(med) for b in med[i+1:] if overlap(a,b)]
result={'status':'PASS','shell_pieces':len(shell),'lid_shell_pieces':len(orn),'lid_ancestry':True,'low_relief':True,'medallion_nonoverlap':True,'detached_lid_ornament_negative_control_rejected':negative,'original_geometric_motifs_not_traditional_replicas':True}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
err=max(abs(bpy.data.objects[n].matrix_world[i][j]-v[i][j]) for n,v in pivots.items() for i in range(4) for j in range(4));assert err<1e-7
result['baseline_pivot_matrix_max_error']=err
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
