import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'bulgaria.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']
def check():
 petals=[o for o in bpy.data.objects if o.name.startswith('Rose petal')]
 centers=[o for o in bpy.data.objects if o.name.startswith('Rose center')]
 leaves=[o for o in bpy.data.objects if o.name.startswith('Rose leaf')]
 assert len(petals)==36 and len(centers)==3 and len(leaves)==12
 for o in petals+centers+leaves:
  assert o.parent==lid, 'ornament detached from lid'
  points=[o.matrix_world@v.co for v in o.data.vertices]
  assert max(v.z for v in points)<2.4
 slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<.001
 assert abs(lid.location.y-1.32)<.001
 return dict(petals=len(petals),centers=len(centers),leaves=len(leaves),all_lid_owned=True,height_below_2_4=True)
r=check();o=bpy.data.objects['Rose center 0'];o.parent=None
try:check()
except AssertionError as e:negative=str(e)
else:raise AssertionError('negative control did not fail')
o.parent=lid
r.update(status='PASS',detached_ornament_negative_control=negative)
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(r)
