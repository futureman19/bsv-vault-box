import bpy,json,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'luxembourg.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
outc=[o for o in bpy.data.objects if o.name.startswith('Outcrop /')];ferns=[o for o in bpy.data.objects if o.name.startswith('Fern /')];stream=bpy.data.objects['Ravine / stream']
if '--negative' in sys.argv:outc[0].parent=None
assert len(outc)==8 and len(ferns)==12
assert all(o.parent==lid for o in outc+ferns+[stream]),'Detached ornament rejected'
verts=[o.matrix_world@v.co for o in outc for v in o.data.vertices]
assert max(v.z for v in verts)-1.978<.8
assert max(v.x for v in verts)-min(v.x for v in verts)<2.8
assert max(v.y for v in verts)-min(v.y for v in verts)<1.65
west=[o.matrix_world@v.co for o in outc if 'west' in o.name for v in o.data.vertices];east=[o.matrix_world@v.co for o in outc if 'east' in o.name for v in o.data.vertices]
gap=min(v.x for v in east)-max(v.x for v in west);assert gap>.35
# Compare exact inherited pivot matrices after independently updating each scene.
pivots={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
images=[i.name for i in bpy.data.images if i.packed_file];assert len(images)>=3
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for name,m in pivots.items():assert max(abs(m[i][j]-bpy.data.objects[name].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-7
result=dict(status='PASS',outcrops=len(outc),ferns=len(ferns),ravine_gap=gap,pivots_preserved=True,packed_images=images)
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(result)
