import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
names=['Lid_Hinge','Latch_Pivot'];base={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in names}
bpy.ops.wm.open_mainfile(filepath=str(R/'niger.blend'),use_scripts=False);bpy.context.view_layer.update()
for n in names:assert max(abs(v-base[n][i][j]) for i,row in enumerate(bpy.data.objects[n].matrix_world) for j,v in enumerate(row))<1e-7
terrain=[o for o in bpy.data.objects if o.name.startswith('Terrain /')];assert len(terrain)==4
assert all(o.parent==bpy.data.objects['Lid_Hinge'] for o in terrain)
zs=[(o.matrix_world@v.co).z for o in terrain for v in o.data.vertices];assert max(zs)<1.978+.65
rocks=[o for o in terrain if 'outcrop' in o.name];assert all(o.matrix_world.translation.x>0 and o.matrix_world.translation.y>0 for o in rocks)
dunes=bpy.data.objects['Terrain / Tenere dunes'];assert len(dunes.data.vertices)>1000
assert max(v.co.z for v in dunes.data.vertices)-min(v.co.z for v in dunes.data.vertices)>.15
# Deliberate detached ornament negative control, restored without saving.
o=rocks[0];p=o.parent;o.parent=None
try:assert all(o.parent==bpy.data.objects['Lid_Hinge'] for o in terrain)
except AssertionError:negative=True
else:negative=False
o.parent=p;assert negative
r={'status':'PASS','pivots_match_mechanism':True,'terrain_count':len(terrain),'relief_max_above_lid':max(zs)-1.978,'rear_right_outcrops':len(rocks),'detached_ornament_negative_rejected':negative}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(r)
