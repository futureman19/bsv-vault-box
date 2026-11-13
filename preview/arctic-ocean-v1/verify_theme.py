import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'arctic.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']
floes=[o for o in bpy.data.objects if o.name.startswith('Floe /')];ponds=[o for o in bpy.data.objects if o.name.startswith('Pond /')];ridges=[o for o in bpy.data.objects if o.name.startswith('Pressure ridge /')]
def owned(o):return o.parent==lid
assert len(floes)==12 and len(ponds)==2 and len(ridges)==9
assert all(owned(o) for o in floes+ponds+ridges)
# Actual negative-control detachment must be rejected.
o=floes[0];p=o.parent;o.parent=None;assert not owned(o);o.parent=p
zs=[(o.matrix_world@v.co).z for o in ridges for v in o.data.vertices];assert max(zs)<2.6
for pond in ponds:
 floe=bpy.data.objects[pond.name.replace('Pond','Floe')]
 poly=[floe.matrix_world@v.co for v in list(floe.data.vertices)[:4]]
 for v in pond.data.vertices:
  q=pond.matrix_world@v.co
  crosses=[(poly[(i+1)%4].x-poly[i].x)*(q.y-poly[i].y)-(poly[(i+1)%4].y-poly[i].y)*(q.x-poly[i].x) for i in range(4)]
  assert min(crosses)>0,('pond outside floe',pond.name)
# Saved matrices of both pivots compared with independently opened baseline.
current={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
error=max(abs(current[n][i][j]-bpy.data.objects[n].matrix_world[i][j]) for n in current for i in range(4) for j in range(4));assert error<1e-7
out=dict(status='PASS',floes=len(floes),ponds=len(ponds),ridge_blocks=len(ridges),ridge_max_z=max(zs),pond_vertex_containment=True,all_ornaments_lid_owned=True,detached_negative_control_rejected=True,pivot_matrix_max_error=error)
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(out)
