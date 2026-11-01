import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
changed={'Glacier / crevassed asymmetric ridge','Lid / polished slab','River / depth graded connected channel','River / connected side cascade'}
def records():
 out={}
 for o in bpy.data.objects:
  if o.name in changed:continue
  d={'matrix':[list(row) for row in o.matrix_world],'parent':o.parent.name if o.parent else None}
  if o.type=='MESH':d.update(v=[list(v.co) for v in o.data.vertices],p=[list(p.vertices) for p in o.data.polygons],materials=[m.name for m in o.data.materials])
  out[o.name]=hashlib.sha256(json.dumps(d,sort_keys=True).encode()).hexdigest()
 return out
bpy.ops.wm.open_mainfile(filepath=str(R/'approved-v9.blend'),use_scripts=False);bpy.context.view_layer.update();before=records()
bpy.ops.wm.open_mainfile(filepath=str(R/'iceland.blend'),use_scripts=False);bpy.context.view_layer.update();after=records();assert before==after
ice=bpy.data.objects['Glacier / crevassed asymmetric ridge'];river=bpy.data.objects['River / depth graded connected channel']
def verts(o):return [o.matrix_world@v.co for v in o.data.vertices]
def tree(o):
 ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();t=BVHTree.FromPolygons([o.matrix_world@v.co for v in m.vertices],[list(p.vertices) for p in m.polygons]);ev.to_mesh_clear();return t
iv=verts(ice);bounds=[[min(v[i] for v in iv) for i in range(3)],[max(v[i] for v in iv) for i in range(3)]]
assert bounds[0][0]>.8 and bounds[0][1]>.35 and bounds[1][1]<1.05
assert bpy.data.objects['Latch_Pivot'].matrix_world.translation.y<0 and bpy.data.objects['Lid_Hinge'].matrix_world.translation.y>0
rv=verts(river);end=[sum(v[i] for v in rv[-6:])/6 for i in range(3)];assert end[0]>1.2 and end[1]>.65
# Endpoint below the glacier footprint and ice surface; channel crosses ice boundary.
hit=tree(ice).ray_cast(Vector((end[0],end[1],3)),Vector((0,0,-1)));assert hit[0] is not None
# The source rises into the ice footprint: actual triangle intersections, not projection.
assert tree(ice).overlap(tree(river)), 'River must intersect glacier'
assert bounds[0][2]<end[2]<hit[0].z
slab=tree(bpy.data.objects['Lid / polished slab'])
oldhit=slab.ray_cast(Vector((1.2,-.75,3)),Vector((0,0,-1)))[0]
newhit=slab.ray_cast(Vector((.1,.38,3)),Vector((0,0,-1)))[0]
assert oldhit and oldhit.z>1.977, 'Old channel not filled'
# Direct centerline ray away from glacier verifies the actual new incision.
p=json.loads((R/'authorship.json').read_text())['river_centerline'][40]
newhit=slab.ray_cast(Vector((p[0],p[1],3)),Vector((0,0,-1)))[0]
assert newhit and newhit.z<1.95, 'Missing new channel cut'
clearances={}
for o in bpy.data.objects:
 if o.type=='MESH' and (o.name.startswith('Corner ') or o.name.startswith('Hinge /')):
  assert not tree(ice).overlap(tree(o)),o.name
  clearances[o.name]=min((v-tree(o).find_nearest(v)[0]).length for v in iv)
assert len([o for o in bpy.data.objects if o.name.startswith('River /')])==2
result={'physical_axes':'Blender front -Y (latch), rear +Y (hinge), right +X viewed head-on at latch','glacier_world_bounds':bounds,'upstream_river_endpoint':end,'endpoint_inside_glacier_footprint':True,'glacier_surface_over_endpoint':list(hit[0]),'cap_hinge_no_intersections':True,'sampled_ice_vertex_nearest_hardware_distance':min(clearances.values()),'unchanged_other_object_records':len(before),'unchanged_camera_and_transforms':True,'only_two_connected_river_meshes':True}
(R/'physical-check.json').write_text(json.dumps(result,indent=2));print(result)
scene=bpy.context.scene;camera=scene.camera;camera.location=(0,0,9);camera.rotation_euler=(0,0,0);camera.data.type='ORTHO';camera.data.ortho_scale=5;scene.render.resolution_x=1100;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.filepath=str(R/'top-down-source.png');bpy.ops.render.render(write_still=True)
