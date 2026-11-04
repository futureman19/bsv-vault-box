import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
pivots={n:[list(r) for r in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'peru.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,rows in pivots.items():assert max(abs(v-bpy.data.objects[n].matrix_world[i][j]) for i,row in enumerate(rows) for j,v in enumerate(row))<1e-6
lid=bpy.data.objects['Lid_Hinge'];orn=[o for o in bpy.data.objects if o.name.startswith(('Terrace /','Ridge /'))]
def owned():return all(o.parent==lid for o in orn)
assert owned();assert len([o for o in orn if o.name.startswith('Terrace / green tread')])==5
pts=[o.matrix_world@v.co for o in orn for v in o.data.vertices]
assert all(abs(v.x)<=1.55 and abs(v.y)<=.9 and 1.97<=v.z<=3.078 for v in pts)
assert len([o for o in bpy.data.objects if o.name.startswith('Masonry /')])>=24
old=orn[0].parent;orn[0].parent=None;negative=not owned();orn[0].parent=old;assert negative
r={'status':'PASS','terrace_treads':5,'ornament_meshes':len(orn),'lid_ownership':True,'bounds_pass':True,'original_pivots':True,'detached_ornament_negative_control_rejected':negative}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(r)
