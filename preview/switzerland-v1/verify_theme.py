import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'switzerland.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']; latch=bpy.data.objects['Latch_Pivot']
terrain=[o for o in bpy.data.objects if o.name.startswith('Terrain /')]
assert len(terrain)==4 and all(o.parent==lid for o in terrain)
m=bpy.data.objects['Terrain / Matterhorn'];v=[m.matrix_world@p.co for p in m.data.vertices]
lo=[min(p[i] for p in v) for i in range(3)];hi=[max(p[i] for p in v) for i in range(3)]
assert lo[0]>-1.7 and hi[0]<1.7 and lo[1]>-1 and hi[1]<1
assert .65<hi[2]-1.978<1.15
assert len(set(p.material_index for p in m.data.polygons))==2
assert all(i.packed_file for i in bpy.data.images if i.type=='IMAGE' and i.users)
actual={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,rows in actual.items():
 assert max(abs(rows[i][j]-bpy.data.objects[name].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
out={'status':'PASS','terrain_count':len(terrain),'mountain_bounds':[lo,hi],'rock_and_snow_faces':True,'packed_maps':True,'original_pivots_match':True,'lid_ancestry':True}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(out)
