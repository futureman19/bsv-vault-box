import bpy,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'palestine.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];stitches=[o for o in bpy.data.objects if o.name.startswith('Stitch / cross')]
if '--negative' in sys.argv:stitches[0].parent=None
assert len(stitches)==96
assert all(o.parent==lid for o in stitches),'detached ornament'
pts=[o.matrix_world@v.co for o in stitches for v in o.data.vertices]
assert all(abs(v.x)<1.45 and abs(v.y)<.85 and 2.030<v.z<2.08 for v in pts)
assert bpy.data.objects['Textile / inset'].parent==lid
r={'status':'PASS','thread_segments':len(stitches),'crosses':len(stitches)//2,'diamonds':3,'z_min':min(v.z for v in pts),'z_max':max(v.z for v in pts),'all_lid_owned':True}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(r)
