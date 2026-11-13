"""Independent saved-source contract checks with a detached-peak negative control."""
import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
baseline={n:[list(r) for r in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'saint-lucia.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in baseline.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
names=['Terrain / Gros Piton','Terrain / Petit Piton','Terrain / Piton Mitan inspired ridge']
def contract():
 for n in names:assert bpy.data.objects[n].parent==bpy.data.objects['Lid_Hinge'],n+' detached'
contract();peak=bpy.data.objects[names[0]];p=peak.parent;peak.parent=None
try:contract();raise RuntimeError('Negative control escaped')
except AssertionError as e:negative=str(e)
finally:peak.parent=p
contract();bpy.context.view_layer.update()
bounds={}
for n in names:
 o=bpy.data.objects[n];v=[o.matrix_world@v.co for v in o.data.vertices];lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)];bounds[n]={'min':lo,'max':hi}
 assert lo[0]>=-1.5 and hi[0]<=1.5 and lo[1]>=-.95 and hi[1]<=.95
assert 2.78<bounds[names[0]]['max'][2]<2.98
assert 2.68<bounds[names[1]]['max'][2]<2.93
assert bounds[names[0]]['max'][0]<bounds[names[1]]['min'][0]
assert len([i for i in bpy.data.images if i.packed_file])>=3
out={'status':'PASS','pivots_match_mechanism':True,'landscape_bounds':bounds,'all_terrain_lid_owned':True,'detached_peak_negative_control':'REJECTED: '+negative,'scope':'Stylized two-peak miniature, not surveyed geography'}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
