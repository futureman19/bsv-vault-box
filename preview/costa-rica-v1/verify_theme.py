import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
bpy.context.view_layer.update()
base={n:[list(row) for row in bpy.data.objects[n].matrix_world] for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'costa-rica.blend'),use_scripts=False)
bpy.context.view_layer.update()
for n,v in base.items():
 assert max(abs(v[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-8
lid=bpy.data.objects['Lid_Hinge'];cone=bpy.data.objects['Arenal / cone']
canopy=[o for o in bpy.data.objects if o.name.startswith('Rainforest / canopy')]
assert len(canopy)==24 and all(o.parent==lid for o in canopy+[cone,bpy.data.objects['Rainforest / island']])
z=[(cone.matrix_world@v.co).z for v in cone.data.vertices];assert 2.87<max(z)<2.90
# Deliberate detached-ornament negative control; never saved to final source.
cone.parent=None
try: assert cone.parent==lid
except AssertionError: rejected=True
else: rejected=False
assert rejected
r={'status':'PASS','canopy_clusters':len(canopy),'cone_z_range':[min(z),max(z)],'inherited_pivots_exact':True,'lid_ancestry':True,'detached_ornament_negative_control_rejected':rejected}
(R/'theme-source-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
