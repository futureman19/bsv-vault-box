import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'china.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];parts=[o for o in bpy.data.objects if o.name.startswith('Peony /')]
def valid_parent():return all(o.parent==lid for o in parts)
assert valid_parent();o=parts[0];o.parent=None;assert not valid_parent();o.parent=lid
petals=[o for o in parts if 'petal' in o.name];leaves=[o for o in parts if 'leaf' in o.name];assert len(petals)==48 and len(leaves)==6
verts=[o.matrix_world@v.co for o in parts for v in o.data.vertices];bounds=[[min(v[i] for v in verts),max(v[i] for v in verts)] for i in range(3)]
assert bounds[0][0]>-1.58 and bounds[0][1]<1.58 and bounds[1][0]>-1 and bounds[1][1]<1 and bounds[2][1]<2.278
# Bottoms of every ornament are seated in or on ground/slab, no hovering pieces.
for o in parts:
 z=min((o.matrix_world@v.co).z for v in o.data.vertices);assert 1.97<=z<=2.001,(o.name,z)
assert abs(lid.location.y-1.32)<1e-6 and abs(lid.location.z-1.668)<1e-6
out=dict(status='PASS',petals=len(petals),leaves=len(leaves),ornament_bounds=bounds,lid_parentage=True,detached_negative_control_rejected=True,seated_ornaments=True)
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
