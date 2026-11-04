import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:list(bpy.data.objects[n].matrix_world) for n in []}
baseline={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'saint-vincent-and-the-grenadines.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']
for n,rows in baseline.items():assert max(abs(rows[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
cays=[o for o in bpy.data.objects if o.name.startswith('Cay /')];assert len(cays)==5
ornaments=cays+[bpy.data.objects[n] for n in ['Sea / inset','Soufriere / crater massif','Reef / horseshoe trace']]
def ancestry():
 for o in ornaments:assert o.parent==lid,('Detached ornament',o.name)
ancestry();cays[0].parent=None
try:ancestry()
except AssertionError:negative=True
else:raise AssertionError('Detached negative control was accepted')
cays[0].parent=lid
# World coordinates captured from delivered saved source, not generation constants.
bpy.ops.wm.open_mainfile(filepath=str(R/'saint-vincent-and-the-grenadines.blend'),use_scripts=False);bpy.context.view_layer.update()
m=bpy.data.objects['Soufriere / crater massif'];vs=[m.matrix_world@v.co for v in m.data.vertices]
zs=[v.z for v in vs];rim=max(zs);center=vs[-1].z
assert .10<rim-center<.5
assert .35<rim-1.982<.65
assert max(v.x for v in vs)-min(v.x for v in vs)<1.35
for o in [o for o in bpy.data.objects if o.name.startswith('Cay /')]:
 pts=[o.matrix_world@v.co for v in o.data.vertices];assert max(v.z for v in pts)-1.991<.16
 assert min(v.z for v in pts)<1.991 and max(v.z for v in pts)>2.04
assert len([i for i in bpy.data.images if i.packed_file])>=3
r={'status':'PASS','same_mechanism_pivots':True,'cay_count':5,'crater_rim_z':rim,'crater_center_z':center,'crater_depth':rim-center,'all_ornaments_lid_children':True,'detached_ornament_negative_control_rejected':negative,'maps_packed':True}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print('THEME PASS',r)
