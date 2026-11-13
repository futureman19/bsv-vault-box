import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'iran.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():assert max(abs(bpy.data.objects[n].matrix_world[i][j]-m[i][j]) for i in range(4) for j in range(4))<1e-7
lid=bpy.data.objects['Lid_Hinge'];ornaments=[o for o in bpy.data.objects if o.name.startswith('Mosaic /')]
def check(objects):
 assert len(objects)==38
 assert all(o.parent==lid for o in objects)
 for prefix,count in [('Mosaic / eight point star',15),('Mosaic / turquoise jewel',15),('Mosaic / diamond',8)]:assert sum(o.name.startswith(prefix) for o in objects)==count
 verts=[o.matrix_world@v.co for o in objects for v in o.data.vertices]
 assert min(v.z for v in verts)>=1.9779 and max(v.z for v in verts)<=2.10
 assert max(abs(v.x) for v in verts)<1.6 and max(abs(v.y) for v in verts)<.9
 return [min(v.z for v in verts),max(v.z for v in verts)]
bounds=check(ornaments)
o=ornaments[0];o.parent=None
try:check(ornaments)
except AssertionError:negative=True
else:raise AssertionError('detached ornament incorrectly accepted')
o.parent=lid
r={'status':'PASS','ornaments':38,'stars':15,'jewels':15,'diamonds':8,'z_bounds':bounds,'inherited_pivots_exact':True,'detached_ornament_negative_control_rejected':negative,'negative_control_type':'post-implementation regression probe, not TDD'}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
