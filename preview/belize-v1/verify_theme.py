import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'belize.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
lid=bpy.data.objects['Lid_Hinge'];terrain=[o for o in bpy.data.objects if o.name.startswith('Terrain /')]
def check_parent():
 assert terrain and all(o.parent==lid for o in terrain),'Detached lid ornament'
check_parent();o=terrain[0];o.parent=None
try:check_parent();raise RuntimeError('Negative control incorrectly accepted')
except AssertionError as e:negative=str(e)
o.parent=lid
floor=bpy.data.objects['Terrain / Blue Hole floor'];reef=bpy.data.objects['Terrain / pale broken reef']
def coords(o):return [o.matrix_world@v.co for v in o.data.vertices]
f=coords(floor);r=coords(reef)
assert max(v.z for v in f)<min(v.z for v in r)
assert .9<max(v.x for v in f)-min(v.x for v in f)<1.3
assert all(abs(v.x)<1.86 and abs(v.y)<1.19 and 1.90<v.z<2.627 for o in terrain for v in coords(o))
assert all(p.normal.z>0 for name in ['Terrain / turquoise shoal','Terrain / pale broken reef'] for p in bpy.data.objects[name].data.polygons)
assert not any(o.name.startswith(('Cedar','Granite')) for o in bpy.data.objects)
result={'status':'PASS','pivot_matrices_preserved':True,'terrain_objects':len(terrain),'all_lid_owned':True,'hole_diameter':max(v.x for v in f)-min(v.x for v in f),'floor_below_reef':True,'negative_control':{'status':'REJECTED','reason':negative},'within_lid_footprint':True}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print('THEME PASS',json.dumps(result))
