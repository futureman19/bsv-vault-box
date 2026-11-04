import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
baseline={n:list(bpy.data.objects[n].location) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'angola.blend'),use_scripts=False)
for n,p in baseline.items():assert list(bpy.data.objects[n].location)==p
cliffs=[o for o in bpy.data.objects if o.name.startswith('Cliff /')];assert len(cliffs)==3
for o in cliffs:assert o.parent.name=='Lid_Hinge' and .15<o.dimensions.z<.65
seams=[o for o in bpy.data.objects if o.name.startswith('Earth seam')];assert len(seams)==4 and all(o.dimensions.z<=.10 for o in seams)
slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<.001 and abs(slab.dimensions.y-2.38)<.001
# Negative control exercises this exact feature validator, not fabricated output.
def validate(items):assert len(items)==3 and all(o.parent and o.parent.name=='Lid_Hinge' for o in items)
validate(cliffs)
try:validate(cliffs[:2])
except AssertionError:negative=True
else:raise AssertionError('missing-cliff negative control not rejected')
r={'status':'PASS','exact_baseline_pivots':baseline,'cliffs':len(cliffs),'seam_height_max':max(o.dimensions.z for o in seams),'missing_cliff_negative_rejected':negative}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
