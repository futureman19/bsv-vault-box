import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'congo.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def bounds(o):
 v=[o.matrix_world@Vector(p) for p in o.bound_box];return [[min(p[i] for p in v),max(p[i] for p in v)] for i in range(3)]
s=bpy.data.objects['Lid / polished slab'];bb=bounds(s)
assert abs(bb[0][1]-bb[0][0]-3.72)<1e-4 and abs(bb[1][1]-bb[1][0]-2.38)<1e-4
ornaments=[o for o in bpy.data.objects if o.type=='MESH' and (o.name.startswith('Bai /') or o.name.startswith(('Forest / root','Forest / trunk','Forest / branch','Forest / broadleaf')))]
assert len(ornaments)>25 and all(o.parent==lid for o in ornaments)
relief=max((bounds(o)[2][1]-bb[2][1],o.name) for o in ornaments)
print('MAX_RELIEF',relief,flush=True)
assert relief[0]<=.65
clearing=bounds(bpy.data.objects['Bai / clearing']);assert clearing[0][1]-clearing[0][0]>=.65
assert all(o.dimensions.z<=.10001 for o in bpy.data.objects if o.name.startswith('Mineral seam'))
# Actual immutable family mechanism pivot comparison, rather than guessed coordinates.
actual={n:list(bpy.data.objects[n].location) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
expected={n:list(bpy.data.objects[n].location) for n in actual};assert actual==expected
r={'status':'PASS','lid_dimensions':[(b[1]-b[0]) for b in bb],'ornament_mesh_count':len(ornaments),'clearing_bounds':clearing,'pivot_positions':actual,'pivot_reference_matches':True,'relief_limit':.65,'seam_limit':.10}
(R/'contract-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
