import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'rwanda.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge']; latch=bpy.data.objects['Latch_Pivot']
slab=bpy.data.objects['Lid / polished slab']
assert all(abs(a-b)<1e-5 for a,b in zip(slab.dimensions,(3.72,2.38,.30)))
assert all(abs(a-b)<1e-5 for a,b in zip(lid.location,(0,1.32,1.668)))
orn=[o for o in bpy.data.objects if o.name.startswith('Lid relief')]
body=[o for o in bpy.data.objects if o.name.startswith('Body relief')]
assert len(orn)==9 and len(body)>=12
assert all(o.parent==lid for o in orn)
assert all(1.978< (o.matrix_world@v.co).z <2.138 for o in orn for v in o.data.vertices)
assert not any(any(s in o.name.lower() for s in ['cedar','moss','glacier']) for o in bpy.data.objects)
result=dict(status='PASS',lid_dimensions=list(slab.dimensions),lid_pivot=list(lid.location),lid_reliefs=len(orn),body_reliefs=len(body),max_relief_z=max((o.matrix_world@v.co).z for o in orn for v in o.data.vertices))
(R/'contract-check.json').write_text(json.dumps(result,indent=2));print('CONTRACT PASS',result)
