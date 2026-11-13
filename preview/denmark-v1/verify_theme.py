import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'denmark.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
land=[o for o in bpy.data.objects if o.name.startswith(('Landscape /','Baltic /'))]
def owned(items):
 assert items and all(o.parent==lid for o in items),'Landscape lost lid ancestry'
owned(land)
o=land[0];p=o.parent;o.parent=None
try:owned(land)
except AssertionError:negative=True
else:raise AssertionError('Detached ornament was accepted')
o.parent=p;bpy.context.view_layer.update()
cliffs=[o for o in land if o.name.startswith('Landscape / chalk cliff')]
assert len(cliffs)==3
for o in cliffs:
 vs=[o.matrix_world@v.co for v in o.data.vertices]
 assert min(v.z for v in vs)>=2 and 2.6>max(v.z for v in vs)>2.4
 assert len(o.data.materials)==2
assert len([o for o in land if 'flint shore' in o.name])==24
assert len([o for o in bpy.data.objects if o.name.startswith('Chalk body')])==4
assert len([o for o in bpy.data.objects if o.name.startswith('Flint foot')])==4
saved={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
images=[i.name for i in bpy.data.images if i.packed_file];assert len(images)==3
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
err=max(abs(saved[n][i][j]-bpy.data.objects[n].matrix_world[i][j]) for n in saved for i in range(4) for j in range(4));assert err<1e-6
result={'status':'PASS','landscape_lid_owned':len(land),'cliff_sections':3,'flint_shore_stones':24,'packed_maps':images,'original_pivot_error':err,'detached_ornament_negative_control_rejected':negative,'limits':'Abstract plateau crown, not individual trees or geographic reconstruction'}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
