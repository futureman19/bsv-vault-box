import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'ecuador.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
base={n:tuple(bpy.data.objects[n].matrix_world.translation) for n in ['Lid_Hinge','Latch_Pivot']}
islands=[o for o in bpy.data.objects if o.name.startswith('Islet /')]
assert len(islands)==3
for o in islands:
 assert o.parent==lid
 vs=[o.matrix_world@v.co for v in o.data.vertices]
 assert all(abs(v.x)<1.5 and abs(v.y)<.85 for v in vs)
 assert min(v.z for v in vs)>=2.017 and max(v.z for v in vs)<2.57
cal=bpy.data.objects['Islet / caldera'];vs=[cal.matrix_world@v.co for v in cal.data.vertices]
center=vs[-1];rim=vs[192:256];depth=min(v.z for v in rim)-center.z
assert .20<depth<.35,depth
assert (center-Vector((.53,.23,2.197))).length<1e-5
# Actual deliberate ancestry mutation must be rejected; restore in memory only.
original=cal.parent;cal.parent=None
try:
 assert all(o.parent==lid for o in islands)
except AssertionError:negative=True
else:raise AssertionError('Detached-islet negative control falsely passed')
cal.parent=original
maps=[im for im in bpy.data.images if im.packed_file];assert len(maps)>=4
assert all(max(im.size)<=1024 for im in maps)
# Independently evaluate original mechanism pivots, not hardcoded guessed values.
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,xyz in base.items():assert (bpy.data.objects[n].matrix_world.translation-Vector(xyz)).length<1e-7
r={'status':'PASS','islets':3,'caldera_depression':depth,'all_islets_lid_owned':True,'detached_islet_negative_rejected':negative,'original_mechanism_pivots_equal':True,'packed_maps':len(maps)}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
