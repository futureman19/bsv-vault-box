import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
baseline={n:list(bpy.data.objects[n].location) for n in ['Lid_Hinge','Latch_Pivot']}
bpy.ops.wm.open_mainfile(filepath=str(R/'zambia.blend'),use_scripts=False)
for n,v in baseline.items():assert max(abs(a-b) for a,b in zip(v,bpy.data.objects[n].location))<1e-7
lid=bpy.data.objects['Lid_Hinge'];slab=bpy.data.objects['Lid / polished slab']
assert abs(slab.dimensions.x-3.72)<1e-5 and abs(slab.dimensions.y-2.38)<1e-5
ornaments=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(('Gorge /','Falls /','Zambezi /'))]
assert len(ornaments)>=40
for o in ornaments:
 assert o.parent==lid
 for v in o.data.vertices:
  p=o.matrix_world@v.co
  assert abs(p.x)<1.65 and abs(p.y)<.95 and 1.95<p.z<2.628,(o.name,list(p))
for o in bpy.data.objects:
 if o.name.startswith('Mineral seam'):assert o.dimensions.z<=.10001
water=bpy.data.objects['Zambezi / continuous river and falls'];adj={v.index:set() for v in water.data.vertices}
for e in water.data.edges:a,b=e.vertices;adj[a].add(b);adj[b].add(a)
seen=set();todo=[0]
while todo:
 i=todo.pop()
 if i in seen:continue
 seen.add(i);todo.extend(adj[i]-seen)
assert len(seen)==len(adj),'disconnected water surface'
zs=[(water.matrix_world@v.co).z for v in water.data.vertices];assert max(zs)-min(zs)>.35
assert {p.material_index for p in water.data.polygons}=={0,1}
result={'status':'PASS','pivot_locations_identical_to_mechanism':baseline,'lid_dimensions':list(slab.dimensions),'ornament_meshes':len(ornaments),'all_ornament_vertices_inside_declared_envelope':True,'connected_river_vertices':len(seen),'water_drop':max(zs)-min(zs),'seam_height_max':max(o.dimensions.z for o in bpy.data.objects if o.name.startswith('Mineral seam'))}
(R/'geometry-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
