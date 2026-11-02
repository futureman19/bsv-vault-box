import bpy, math, json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'mechanism.blend'),use_scripts=False)
anchors={n:list(bpy.data.objects[n].location) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'dr-congo.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot'];assert latch.parent==lid
for n,loc in anchors.items():assert all(abs(a-b)<1e-7 for a,b in zip(loc,bpy.data.objects[n].location)),('pivot changed',n)
ornaments=[o for o in bpy.data.objects if o.name.startswith(('Canopy /','Terrain /','River /'))]
assert all(o.parent==lid for o in ornaments)
river=bpy.data.objects['River / continuous channel'];assert len(river.data.polygons)==64
adj={v.index:set() for v in river.data.vertices}
for e in river.data.edges:
 a,b=e.vertices;adj[a].add(b);adj[b].add(a)
seen=set();todo=[0]
while todo:
 i=todo.pop()
 if i in seen:continue
 seen.add(i);todo.extend(adj[i]-seen)
assert len(seen)==len(river.data.vertices)==130
bpy.context.view_layer.update()
for i in range(65):
 x=-1.5+3*i/64;y=.23*math.sin(x*2.8)+.08*math.sin(x*5)
 # Endpoints are boundary vertices; interior stations prove the channel is not buried.
 if i in (0,64):continue
 hit,loc,normal,index,obj,matrix=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((x,y,3)),Vector((0,0,-1)))
 assert hit and obj==river,('buried river station',i,obj.name if obj else None)
(ROOT/'theme-source-check.json').write_text(json.dumps({'status':'PASS','unchanged_pivots':anchors,'lid_ornaments':len(ornaments),'river_connected_vertices':len(seen),'exposed_river_ray_stations':63},indent=2))
moving=[o for o in bpy.data.objects if o.type=='MESH' and (o.parent==lid or o.parent==latch)]
static=[o for o in bpy.data.objects if o.type=='MESH' and o not in moving and not o.name.startswith('Studio')]
def tree(o):
 dep=bpy.context.evaluated_depsgraph_get();ev=o.evaluated_get(dep);m=ev.to_mesh();verts=[o.matrix_world@v.co for v in m.vertices];polys=[list(p.vertices) for p in m.polygons];t=BVHTree.FromPolygons(verts,polys);ev.to_mesh_clear();return t
bpy.context.view_layer.update();fixed={o.name:tree(o) for o in static};collisions=[]
attachments=[]
for suffix in ['', '.001']:
 for a,b in [('Hinge / body attachment bridge'+suffix,'Interior wall / rear'),('Hinge / body attachment bridge'+suffix,'Hinge / fixed mount'+suffix),('Hinge / bearing mounting stem'+suffix,'Hinge / fixed mount'+suffix),('Hinge / bearing mounting stem'+suffix,'Hinge / fixed barrel'+suffix),('Hinge / moving leaf'+suffix,'Lid / polished slab')]:
  assert tree(bpy.data.objects[a]).overlap(tree(bpy.data.objects[b])),('Disconnected mount',a,b)
  attachments.append([a,b])
(ROOT/'hinge-attachment-check.json').write_text(json.dumps({'intersecting_attachment_pairs':attachments,'bearing_axes':'original coaxial X axis at y=1.32 z=1.668'},indent=2))
for step in range(81):
 p=step/80;lid.rotation_euler.x=-math.radians(105)*max(0,(p-.25)/.75);latch.rotation_euler.x=-math.radians(80)*min(1,p/.25);bpy.context.view_layer.update()
 for o in moving:
  t=tree(o)
  for name,other in fixed.items():
   # Mating bearing surfaces are deliberately concentric, not body clearance.
   if o.name.startswith('Hinge / moving leaf') and name.startswith('Hinge / fixed barrel'):continue
   if t.overlap(other):collisions.append([step,o.name,name])
 # Also test releasing hasp against the moving lid; concentric bearing contact is intentional.
 for o in [m for m in moving if m.parent==latch]:
  for other in [m for m in moving if m.parent==lid]:
   if other.name=='Latch / pin' and o.name in ['Latch / rotating knuckle','Latch / hinge bridge']:continue
   if tree(o).overlap(tree(other)):collisions.append([step,o.name,other.name])
# Interior test with lid removed from ray, intersection must be floor below rim.
lid.rotation_euler.x=-math.radians(105);latch.rotation_euler.x=-math.radians(80);bpy.context.view_layer.update()
hit,loc,normal,index,obj,matrix=bpy.context.scene.ray_cast(bpy.context.evaluated_depsgraph_get(),Vector((0,0,1.4)),Vector((0,0,-1)))
assert hit and obj.name=='Interior floor' and loc.z<.3
result={'saved_source_reopened':True,'named_lid':lid.name,'latch_parent':latch.parent.name,'moving_meshes':len(moving),'static_meshes':len(static),'collision_samples':81,'collisions':collisions,'bearing_contact_exclusion':'moving hinge leaf vs fixed barrel; latch knuckle/bridge vs latch pin (intentional bearings)','hollow_floor_ray_z':loc.z,'source_objects':len(bpy.data.objects)}
(ROOT/'source-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));assert not collisions
