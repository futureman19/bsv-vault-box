"""Independent saved-source theme checks; no author module import."""
import bpy,math,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
baseline={n:list(bpy.data.objects[n].location) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'equatorial-guinea.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
for n,loc in baseline.items():assert all(abs(a-b)<1e-7 for a,b in zip(bpy.data.objects[n].location,loc)),n
slab=bpy.data.objects['Lid / polished slab'];assert all(abs(a-b)<1e-5 for a,b in zip(slab.dimensions,(3.72,2.38,.30)))
canopies=[o for o in bpy.data.objects if o.name.startswith('Canopy / crown')];terrain=bpy.data.objects['Terrain / shield and caldera']
assert len(canopies)==72 and all(o.parent==lid for o in canopies+[terrain])
def bvh(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();t=BVHTree.FromPolygons([o.matrix_world@v.co for v in m.vertices],[list(p.vertices) for p in m.polygons]);ev.to_mesh_clear();return t
t=bvh(terrain)
def height(x,y):
 hit=t.ray_cast(Vector((x,y,4)),Vector((0,0,-1)))[0];assert hit is not None;return hit.z
center=height(-.35,.10);rim=[height(-.35+.47*math.cos(a),.1+.38*math.sin(a)) for a in [0,math.pi/2,math.pi,math.pi*1.5]]
assert min(rim)-center>.15,(center,rim)
verts=[terrain.matrix_world@v.co for v in terrain.data.vertices];assert max(v.z for v in verts)-1.978<.65
assert max(abs(v.x) for v in verts)<1.65 and max(abs(v.y) for v in verts)<1.0
contacts=[o.name for o in canopies if bvh(o).overlap(t)];missing=[o.name for o in canopies if o.name not in contacts]
images={i.name:len(i.packed_file.data) for i in bpy.data.images if i.packed_file};assert set(images)=={'basalt-color.png','basalt-normal.png','basalt-roughness.png'}
r={'status':'PASS' if not missing else 'FAIL','pivots_match_trimmed_baseline':baseline,'lid_dimensions':list(slab.dimensions),'canopy_meshes':len(canopies),'caldera_center_z':center,'rim_z':rim,'minimum_depression':min(rim)-center,'canopy_surface_contacts':len(contacts),'unseated_canopies':missing,'packed_images':images,'lid_parentage':True}
(R/'theme-source-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r));assert not missing,missing
