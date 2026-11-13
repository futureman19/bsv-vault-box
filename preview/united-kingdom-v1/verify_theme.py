import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'united-kingdom.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
terrain=[o for o in bpy.data.objects if o.name.startswith('Terrain /')];walls=[o for o in bpy.data.objects if o.name.startswith('Field wall /')]
def contract():
 assert len(terrain)==2 and len(walls)>=90
 assert all(o.parent==lid for o in terrain+walls)
 assert len([o for o in bpy.data.objects if o.name.startswith('Slate / front')])>=36
 assert all(1.97<(o.matrix_world@v.co).z<2.6 for o in terrain+walls for v in o.data.vertices)
contract();victim=walls[0];victim.parent=None
try:contract();raise RuntimeError('negative control accepted')
except AssertionError:negative=True
victim.parent=lid
# Compare independently evaluated inherited pivots.
actual={n:[list(row) for row in bpy.data.objects[n].matrix_local] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,rows in actual.items():assert max(abs(rows[i][j]-bpy.data.objects[n].matrix_local[i][j]) for i in range(4) for j in range(4))<1e-7
out={'status':'PASS','terrain_meshes':len(terrain),'wall_meshes':len(walls),'detached_ornament_rejected':negative,'pivots_match_trimmed_mechanism':True}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(out)
