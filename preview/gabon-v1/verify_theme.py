import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'gabon.blend'),use_scripts=False)
bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge']; latch=bpy.data.objects['Latch_Pivot']
def owned(o):
 while o.parent:
  o=o.parent
  if o==lid:return True
 return False
orn=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(('Forest /','Coast /','Lagoon /'))]
assert all(owned(o) for o in orn)
can=[o for o in orn if o.name.startswith('Forest / canopy')];assert len(can)==15
verts=[o.matrix_world@v.co for o in orn for v in o.data.vertices]
assert all(abs(v.x)<=1.98 and abs(v.y)<=1.31 and v.z<=1.978+.85 for v in verts)
water=bpy.data.objects['Lagoon / continuous winding water'];assert len(water.data.polygons)==40
# Shared-edge graph proves one continuous ribbon, not disconnected strips.
seen={0}
while True:
 old=len(seen)
 for poly in water.data.polygons:
  if seen.intersection(poly.vertices):seen.update(poly.vertices)
 if old==len(seen):break
assert len(seen)==len(water.data.vertices)
dep=bpy.context.evaluated_depsgraph_get();hits=[]
for poly in water.data.polygons:
 c=water.matrix_world@poly.center
 hit,loc,n,i,obj,m=bpy.context.scene.ray_cast(dep,Vector((c.x,c.y,4)),Vector((0,0,-1)))
 assert hit and obj==water,(poly.index,obj.name if obj else None)
 hits.append(poly.index)
assert all(abs(o.dimensions.z-.08)<1e-5 for o in bpy.data.objects if o.name.startswith('Mineral seam'))
assert abs(bpy.data.objects['Lid / polished slab'].dimensions.x-3.72)<1e-5
pivots={o.name:list(o.matrix_world.translation) for o in [lid,latch]}
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False);bpy.context.view_layer.update()
for n,p in pivots.items():assert (bpy.data.objects[n].matrix_world.translation-Vector(p)).length<1e-6
out=dict(status='PASS',canopy_meshes=len(can),ornament_meshes=len(orn),lagoon_connected_vertices=len(seen),exposed_lagoon_face_rays=len(hits),pivots_unchanged=True,ornament_bounds=True,seam_height=.08)
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
