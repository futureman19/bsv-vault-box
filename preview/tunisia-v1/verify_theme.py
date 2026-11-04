import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'tunisia.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
dish=bpy.data.objects['Sejnane / shallow dish'];accents=[o for o in bpy.data.objects if o.name.startswith('Sejnane / lip accent')]
def check_ancestry():
 assert dish.parent==lid and len(accents)==12 and all(o.parent==lid for o in accents),'Every dish/mark must travel with lid'
check_ancestry()
dish.parent=None
try:check_ancestry();raise RuntimeError('Negative control accepted!')
except AssertionError as e:negative={'mutation':'detach dish from Lid_Hinge','rejected':True,'error':str(e)}
dish.parent=lid
check_ancestry()
vs=[dish.matrix_world@v.co for v in dish.data.vertices]
assert abs(max(v.x for v in vs)-.73)<1e-5
assert max(v.z for v in vs)<=2.24
assert abs(vs[0].z-2.015)<1e-5 and max(v.z for v in vs)-vs[0].z>=.10
# Top surface winding (first six radial rings) must face upward.
assert all(p.normal.z>0 for p in list(dish.data.polygons)[:96*5])
slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<1e-5 for a,b in zip(slab.dimensions,(3.72,2.38,.30)))
assert not any(o.name.startswith(('Cedar tree','Finger /','Terrain /')) for o in bpy.data.objects)
pivots={o.name:[list(row) for row in o.matrix_world] for o in [lid,latch]}
# Independent base reopen rather than trusting generator constants.
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,m in pivots.items():
 assert max(abs(m[i][j]-bpy.data.objects[n].matrix_world[i][j]) for i in range(4) for j in range(4))<1e-6
result={'status':'PASS','dish_radius':.73,'dish_floor_z':vs[0].z,'dish_rim_z':max(v.z for v in vs),'dish_concavity':max(v.z for v in vs)-vs[0].z,'upward_top_faces':480,'lip_accents':len(accents),'lid_dimensions':[3.72,2.38,.30],'mechanism_pivots_preserved':True,'negative_control':negative}
(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
