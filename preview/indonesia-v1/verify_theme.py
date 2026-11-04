import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'indonesia.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']
ornaments=[o for o in bpy.data.objects if o.name.startswith('Copper rosette')]
def gate(objects):
 assert len(objects)==20
 for o in objects:
  assert o.parent==lid,('missing lid ownership',o.name)
  co=[o.matrix_world@v.co for v in o.data.vertices]
  assert min(v.z for v in co)>2.01 and max(v.z for v in co)<2.04
  assert max(abs(v.y) for v in co)<.25
  assert max(abs(v.x) for v in co)<1.37
 assert not any(o.name.startswith('Cedar tree') for o in bpy.data.objects)
gate(ornaments)
# Intentional detached-parent regression must be rejected, then restored in memory.
o=ornaments[0];o.parent=None
try:gate(ornaments)
except AssertionError as e:negative=str(e)
else:raise AssertionError('Detached ornament accepted')
o.parent=lid
# Read actual packed base image pixels.
im=bpy.data.images['batik-color.png'];pixels=list(im.pixels);red=pixels[0::4]
assert max(red)-min(red)>.65
# Downward ornament-gap ray reaches solid lid, not an opaque ornament plate.
dep=bpy.context.evaluated_depsgraph_get();gap=bpy.context.scene.ray_cast(dep,Vector((.28,0,2.15)),Vector((0,0,-1)))
assert gap[0] and gap[4].name=='Lid / polished slab',gap[4].name
report={'status':'PASS','rosette_petals':len(ornaments),'lid_owned':True,'bounds_checked':True,'gap_hit':gap[4].name,'palette_red_range':max(red)-min(red),'negative_control':{'detached_parent':'REJECTED','assertion':negative},'interpretation':'original invented motif, not an authenticated traditional pattern'}
(R/'theme-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
