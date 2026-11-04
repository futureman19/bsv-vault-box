import bpy,json,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'albania.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
if '--negative' in sys.argv:bpy.data.objects['House 0 / walls'].parent=None
houses=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('House ')]
assert len(houses)==27,len(houses)
assert all(o.parent==lid for o in houses),'Detached architecture'
roots=[]
for i in range(3):
 o=bpy.data.objects[f'House {i} / walls'];pts=[o.matrix_world@Vector(p) for p in o.bound_box];bottom=min(p.z for p in pts)
 assert abs(bottom-1.978)<1e-5,bottom
 roots.append(bottom)
roofs=[o for o in houses if '/ roof' in o.name]
assert len(roofs)==9
assert all(p.normal.z>0 for o in roofs for p in o.data.polygons if p.index>0),'Inverted roof face'
assert max((o.matrix_world@v.co).z for o in houses for v in o.data.vertices)<2.90
assert all(len(i.packed_file.data)>0 for i in bpy.data.images if i.users and i.name.endswith('.png'))
assert tuple(round(v,3) for v in lid.location)==(0,1.32,1.668),tuple(lid.location)
r={'status':'PASS','house_meshes':len(houses),'roof_meshes':len(roofs),'roots_z':roots,'all_architecture_lid_owned':True,'roof_top_normals_positive':True,'lid_pivot':list(lid.location),'latch_parent':latch.parent.name}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
