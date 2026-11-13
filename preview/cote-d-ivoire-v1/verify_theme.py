import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'cote-d-ivoire.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
actual_pivots={o.name:list(o.matrix_world.translation) for o in [lid,latch]}
strips=[o for o in bpy.data.objects if o.name.startswith('Textile lid strip')]
joins=[o for o in bpy.data.objects if o.name.startswith('Textile raised join')]
def valid_ownership():return all(o.parent==lid for o in strips+joins)
assert len(strips)==9 and len(joins)==8 and valid_ownership()
strips[0].parent=None
assert not valid_ownership(),'negative control did not reject detached ornament'
strips[0].parent=lid
heights=[(o.matrix_world@v.co).z for o in strips+joins for v in o.data.vertices]
assert min(heights)>=1.978 and max(heights)<2.178
assert not any('Cedar tree' in o.name or 'Terrain' in o.name for o in bpy.data.objects)
assert len([o for o in bpy.data.objects if o.name.startswith('Textile body panel')])==18
# Local source image pixel variation, not image names alone.
images={}
for image in bpy.data.images:
 if image.name in ['indigo.png','cream.png','ochre.png','weave-roughness.png']:
  pixels=list(image.pixels);r=pixels[::4];images[image.name]={'range':max(r)-min(r),'width':image.size[0]};assert max(r)>min(r)
assert len(images)==4
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,xyz in actual_pivots.items():assert max(abs(a-b) for a,b in zip(xyz,bpy.data.objects[name].matrix_world.translation))<1e-7
out={'status':'PASS','strips':9,'joins':8,'height_range': [min(heights),max(heights)],'lid_ownership':True,'detached_negative_control_rejected':True,'exact_inherited_pivots':actual_pivots,'images':images}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));print('THEME PASS')
