import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'sao-tome-and-principe.blend'),use_scripts=False)
bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge']
def world(o):return [o.matrix_world@v.co for v in o.data.vertices]
def validate():
 terrain=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('Terrain /')]
 assert len(terrain)>35
 assert all(o.parent==lid for o in terrain),'Detached lid terrain'
 needle=bpy.data.objects['Terrain / Pico Cao Grande inspired needle'];pts=world(needle)
 mn=[min(p[i] for p in pts) for i in range(3)];mx=[max(p[i] for p in pts) for i in range(3)]
 assert 3.0<=mx[2]<=3.25 and mx[0]-mn[0]<.8 and mx[1]-mn[1]<.75
 assert mx[2]-mn[2]>.95
 bed=bpy.data.objects['Terrain / rainforest bed'];pts2=world(bed)
 assert 1.970<=min(p.z for p in pts2)<=1.978 and max(p.z for p in pts2)<2.30
 assert all(abs(p.x)<1.55 and abs(p.y)<.9 for p in pts2)
 # Exact parented canopy bottoms overlap the terrain surface rather than hover.
 tree=BVHTree.FromPolygons(pts2,[list(p.vertices) for p in bed.data.polygons])
 contacts=[]
 for o in terrain:
  if not o.name.startswith('Terrain / forest canopy'):continue
  p=o.matrix_world.translation;hit=tree.ray_cast(Vector((p.x,p.y,4)),Vector((0,0,-1)))
  assert hit[0] is not None,o.name
  bottom=min(v.z for v in world(o));top=max(v.z for v in world(o))
  assert bottom<=hit[0].z<=top,(o.name,bottom,hit[0].z,top)
  contacts.append(o.name)
 assert len(contacts)>30
 assert len([i for i in bpy.data.images if i.packed_file])>=3
 assert abs(bpy.data.objects['Latch_Pivot'].rotation_euler.x)<1e-8
 return dict(terrain_meshes=len(terrain),canopy_roots_tested=len(contacts),needle_min=mn,needle_max=mx,terrain_seated=True,lid_ownership=True)
r=validate()
# Deliberate post-authoring negative control: detach the defining needle.
needle=bpy.data.objects['Terrain / Pico Cao Grande inspired needle'];needle.parent=None
try:validate()
except AssertionError as e:r['negative_control']={'detached_needle_rejected':True,'failure':str(e)}
else:raise AssertionError('Negative control was not rejected')
needle.parent=lid
r['status']='PASS';(R/'theme-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
