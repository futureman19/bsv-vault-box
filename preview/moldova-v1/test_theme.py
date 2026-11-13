import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
base={n:[list(r) for r in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'moldova.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in base.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
flowers=[o for o in bpy.data.objects if o.name.startswith('Flower')];assert len(flowers)==33
assert all(o.parent==bpy.data.objects['Lid_Hinge'] for o in flowers)
assert len([o for o in bpy.data.objects if o.name.startswith('Woven')])==5
for i in range(3):
 petals=[o for o in flowers if o.name.startswith('Flower %d / petal'%i)];assert len(petals)==8
 v=[o.matrix_world@v.co for o in petals for v in o.data.vertices];span=max(p.x for p in v)-min(p.x for p in v);assert .55<span<.85
 assert all(1.99<p.z<2.10 for p in v)
assert not any(any(s in o.name for s in ['Cedar','Granite','Terrain','Moss']) for o in bpy.data.objects)
images=[i.name for i in bpy.data.images if i.packed_file];assert len(images)>=4
# Prove ornament ancestry oracle rejects deliberately detached lid flower.
o=flowers[0];p=o.parent;o.parent=None
try:assert all(o.parent==bpy.data.objects['Lid_Hinge'] for o in flowers)
except AssertionError:negative=True
else:raise AssertionError('Negative control accepted detached flower')
o.parent=p
r={'status':'PASS','flowers':3,'flower_meshes':len(flowers),'woven_panels':5,'pivot_matrices_unchanged':True,'packed_maps':images,'detached_ornament_negative_control_rejected':negative,'palette_and_motif':'invented contemporary interpretation'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
