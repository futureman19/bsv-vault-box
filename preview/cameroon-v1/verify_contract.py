"""Independent dimensional, landmark, source-material and pivot contract."""
import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
base={n:{'location':list(bpy.data.objects[n].location),'rotation':list(bpy.data.objects[n].rotation_euler)} for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'cameroon.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,v in base.items():
 o=bpy.data.objects[n];assert max(abs(a-b) for a,b in zip(o.location,v['location']))<1e-8;assert max(abs(a-b) for a,b in zip(o.rotation_euler,v['rotation']))<1e-8
lid=bpy.data.objects['Lid_Hinge'];relief=bpy.data.objects['Fako / elongated volcanic massif'];assert relief.parent==lid
slab=bpy.data.objects['Lid / polished slab'];assert abs(slab.dimensions.x-3.72)<.01 and abs(slab.dimensions.y-2.38)<.01
verts=[relief.matrix_world@v.co for v in relief.data.vertices];span=[max(v[i] for v in verts)-min(v[i] for v in verts) for i in range(3)];assert span[0]>=1.7 and .35<span[2]<.85
# Real lower-slope grass material occupies polygons, not an unused palette entry.
grassy=[p for p in relief.data.polygons if p.material_index==1];assert len(grassy)>100
canopies=[o for o in bpy.data.objects if o.name.startswith('Rainforest /')];assert len(canopies)==100 and all(o.parent==lid for o in canopies)
assert max((o.matrix_world@Vector(c)).z for o in canopies for c in o.bound_box)<max(v.z for v in verts)
# Sample the two authored subsidiary shoulders and main crest from actual vertices.
shoulders=[]
for x,y in [(-.62,-.03),(.78,-.15),(.27,.20)]:
 near=[v.z for v in verts if abs(v.x-x)<.12 and abs(v.y-y)<.12];assert near and max(near)>2.12;shoulders.append(max(near))
assert shoulders[2]>max(shoulders[:2])
seams=[o for o in bpy.data.objects if o.name.startswith('Seam /')];assert seams and all(o.dimensions.z<.12 for o in seams)
images=[i for i in bpy.data.images if i.packed_file];assert len(images)==3 and all(max(i.size)<=1024 for i in images)
out={'status':'PASS','same_pivots_as_trimmed_baseline':base,'lid_dimensions':list(slab.dimensions),'relief_span_xyz':span,'green_lower_slope_polygons':len(grassy),'canopies':len(canopies),'shoulder_and_main_heights':shoulders,'packed_maps':[i.name for i in images]}
(R/'source-contract-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
