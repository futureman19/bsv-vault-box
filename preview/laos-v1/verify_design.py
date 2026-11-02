import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'laos.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
assert abs(lid.location.y-1.32)<1e-5 and abs(lid.location.z-1.668)<1e-5
# Included base is the mechanical authority, independently compare exact pivots.
pivots={o.name:{'location':list(o.location),'rotation':list(o.rotation_euler)} for o in [lid,latch]}
peaks=[o for o in bpy.data.objects if o.name.startswith('Karst / peak')];assert len(peaks)==3
bounds=[]
for o in peaks:
 assert o.parent==lid
 v=[o.matrix_world@Vector(c) for c in o.bound_box];mn=[min(q[i] for q in v) for i in range(3)];mx=[max(q[i] for q in v) for i in range(3)]
 assert mn[1]>0 and mx[1]<1.15 and mn[0]>-1.5 and mx[0]<1.5
 assert .3<mx[2]-1.978<.85 and abs(mn[2]-1.97)<1e-5
 bounds.append({'name':o.name,'min':mn,'max':mx})
assert len({round(b['max'][2],2) for b in bounds})==3
for o in bpy.data.objects:
 if o.name.startswith(('River /','Vegetation /')):assert o.parent==lid
 if o.name.startswith('Mineral seam'):assert o.dimensions.z<=.100001
slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<1e-4 for a,b in zip(slab.dimensions,(3.72,2.38,.30)))
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
for name,p in pivots.items():
 o=bpy.data.objects[name];assert max(abs(a-b) for a,b in zip(o.location,p['location']))<1e-7;assert max(abs(a-b) for a,b in zip(o.rotation_euler,p['rotation']))<1e-7
result={'status':'PASS','same_base_pivots':pivots,'three_asymmetric_rear_lid_peaks':bounds,'seam_max_height':.10,'lid_dimensions':[3.72,2.38,.30]}
(R/'design-check.json').write_text(json.dumps(result,indent=2));print('DESIGN PASS',json.dumps(result))
