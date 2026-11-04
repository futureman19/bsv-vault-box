import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'singapore.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
if '--negative' in sys.argv:bpy.data.objects['Orchid 0 / lobe 0'].parent=None
orn=[o for o in bpy.data.objects if o.name.startswith(('Orchid ','Orchid stem','Orchid leaf'))]
assert len([o for o in orn if '/ lobe ' in o.name])==15
assert len([o for o in orn if '/ lip' in o.name])==3
assert all(o.parent==lid for o in orn), 'Detached ornament rejected'
vs=[o.matrix_world@v.co for o in orn for v in o.data.vertices]
assert min(v.z for v in vs)>1.97 and max(v.z for v in vs)<2.328
for k in range(3):
 for j in range(5):
  o=bpy.data.objects[f'Orchid {k} / lobe {j}'];assert ('pink' if j<3 else 'ivory') in o.data.materials[0].name
 assert 'purple' in bpy.data.objects[f'Orchid {k} / lip'].data.materials[0].name
source_pivots={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
images=[i.name for i in bpy.data.images if i.packed_file];assert len(images)>=3
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in source_pivots.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
r={'status':'PASS','flower_count':3,'petal_count':15,'all_ornaments_on_lid':True,'relief_z':[min(v.z for v in vs),max(v.z for v in vs)],'differentiated_petals':True,'original_pivot_matrices':True,'packed_maps':images}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
