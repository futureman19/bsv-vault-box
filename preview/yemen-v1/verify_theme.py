import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'yemen.blend'),use_scripts=False);bpy.context.view_layer.update()
assert all(max(abs(v-pivots[n][i][j]) for i,row in enumerate(bpy.data.objects[n].matrix_world) for j,v in enumerate(row))<1e-7 for n in pivots)
assert len([o for o in bpy.data.objects if o.name.startswith('Gypsum / side diamond')])==32
lid=bpy.data.objects['Lid_Hinge']; towers=[o for o in bpy.data.objects if o.name.startswith('Tower / house')];ornaments=[o for o in bpy.data.objects if o.name.startswith('Tower /')]
def validate():
 assert len(towers)==3
 assert all(o.parent==lid for o in ornaments)
 for o in towers:
  vs=[o.matrix_world@Vector(v) for v in o.bound_box]
  assert min(v.z for v in vs)>1.97 and max(v.z for v in vs)<3.02
  assert .45<o.dimensions.x<.59
validate();old=towers[0].parent;towers[0].parent=None
try:validate()
except AssertionError:negative=True
else:raise AssertionError('Negative control was not rejected')
towers[0].parent=old
assert len([o for o in bpy.data.objects if o.name.startswith('Gypsum / diamond')])==24
assert len([o for o in bpy.data.objects if o.name.startswith('Gypsum / facade band')])==6
r={'status':'PASS','tower_count':3,'all_tower_parts_on_lid':True,'detached_tower_negative_control_rejected':negative,'diamond_segments':24,'material_maps_packed':len([i for i in bpy.data.images if i.packed_file])}
assert r['material_maps_packed']>=3
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(r)
