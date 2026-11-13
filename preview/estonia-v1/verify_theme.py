import bpy,json,sys,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'estonia.blend'),use_scripts=False);bpy.context.view_layer.update()
if '--negative' in sys.argv:
 o=bpy.data.objects['Bog / water 0'];m=o.matrix_world.copy();o.parent=None;o.matrix_world=m
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
assert tuple(round(v,4) for v in lid.location)==(0,1.32,1.668),tuple(lid.location)
orn=[o for o in bpy.data.objects if o.name.startswith(('Bog /','Boardwalk /'))]
assert all(o.parent==lid for o in orn),'Detached ornament rejected'
assert len([o for o in orn if o.name.startswith('Bog / water')])==3
assert len([o for o in orn if o.name.startswith('Bog / rim')])==3
assert len([o for o in orn if o.name.startswith('Boardwalk / plank')])==18
verts=[o.matrix_world@v.co for o in orn for v in o.data.vertices]
assert min(v.z for v in verts)>=1.97 and max(v.z for v in verts)<=2.28
rays=[]
for k,(x,y) in enumerate([(-.85,.25),(.05,.36),(.88,.18)]):
 hit,loc,n,i,obj,m=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3)),Vector((0,0,-1)))
 assert hit and obj.name=='Bog / water '+str(k),(k,obj.name)
 rays.append({'pool':k,'first_hit':obj.name,'height':loc.z})
# Annular top surfaces wind upward and have genuine lower interior water.
for o in [o for o in orn if o.name.startswith('Bog / rim')]:
 assert all(p.normal.z>.9 for p in list(o.data.polygons)[:64])
# Source materials and packed portable images.
assert len([i for i in bpy.data.images if i.packed_file])>=3
r={'status':'PASS','lid_origin':list(lid.location),'ornament_meshes':len(orn),'pool_count':3,'plank_count':18,'ornament_z':[min(v.z for v in verts),max(v.z for v in verts)],'pool_center_rays':rays,'upward_rim_normals':True}
(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
