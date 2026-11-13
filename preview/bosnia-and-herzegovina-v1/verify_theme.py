import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'bosnia-and-herzegovina.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
petals=[o for o in bpy.data.objects if o.name.startswith('Ornament / petal')]
ornaments=[o for o in bpy.data.objects if o.name.startswith(('Ornament /','Border /'))]
def validate():
 assert len(petals)==8
 assert len([o for o in ornaments if o.name.startswith('Border /')])==76
 assert all(o.parent==lid for o in ornaments)
 for o in ornaments:
  for v in o.data.vertices:
   p=o.matrix_world@v.co
   assert 1.96<p.z<2.12,(o.name,list(p))
validate()
original=petals[0].parent;petals[0].parent=None
try:validate()
except AssertionError:negative=True
else:raise AssertionError('Detached petal not rejected')
finally:petals[0].parent=original
# Independent inherited pivot matrices, freshly evaluated from separate source.
matrices={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
source_images=[i.name for i in bpy.data.images if i.packed_file]
assert all(n in source_images for n in ['copper-color.png','copper-normal.png','copper-roughness.png'])
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
err=max(abs(matrices[n][i][j]-bpy.data.objects[n].matrix_world[i][j]) for n in matrices for i in range(4) for j in range(4));assert err<1e-6
out={'status':'PASS','petals':8,'border_beads':76,'all_ornaments_lid_owned':True,'ornament_z_bounds':[1.96,2.12],'detached_petal_negative_control_rejected':negative,'inherited_pivot_max_error':err,'packed_maps':source_images}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
