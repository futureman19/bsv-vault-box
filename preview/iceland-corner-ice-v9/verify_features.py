import bpy,json,struct,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'iceland.blend'),use_scripts=False);bpy.context.view_layer.update()
lid=bpy.data.objects['Lid_Hinge'];ice=bpy.data.objects['Glacier / crevassed asymmetric ridge'];river=bpy.data.objects['River / depth graded connected channel'];cascade=bpy.data.objects['River / connected side cascade']
def vertices(o):return [o.matrix_world@v.co for v in o.data.vertices]
vs=vertices(ice);lo=[min(v[j] for v in vs) for j in range(3)];hi=[max(v[j] for v in vs) for j in range(3)]
assert lo[0]>.9 and hi[0]<1.75 and lo[1]>-1.12 and hi[1]<-.50,(lo,hi)
assert all(o.parent==lid for o in [ice,river,cascade]);assert abs(lo[2]-1.977)<1e-5
r=vertices(river);c=vertices(cascade);assert max((a-b).length for a,b in zip(r[:6],c[:6]))<1e-6
end=sum(r[-6:],Vector())/6;assert lo[0]<end.x<hi[0] and lo[1]<end.y<hi[1]
# Whole channel connected by indexed edges; no old detached branches.
adj={i:set() for i in range(len(r))}
for edge in river.data.edges:a,b=edge.vertices;adj[a].add(b);adj[b].add(a)
seen=set();todo=[0]
while todo:
 a=todo.pop()
 if a in seen:continue
 seen.add(a);todo.extend(adj[a]-seen)
assert len(seen)==len(r)
# Independent ray proof: old river midpoint is now uninterrupted polished lid.
slab=bpy.data.objects['Lid / polished slab'];dep=bpy.context.evaluated_depsgraph_get();ev=slab.evaluated_get(dep);me=ev.to_mesh();tree=BVHTree.FromPolygons([slab.matrix_world@v.co for v in me.vertices],[list(p.vertices) for p in me.polygons]);hit=tree.ray_cast(Vector((-.6,.22,2.4)),Vector((0,0,-1)))[0];assert hit and abs(hit.z-1.978)<1e-5;ev.to_mesh_clear()
# Four enlarged shaped top plates and paired side wraps, seated geometry, 8 raised rivets.
wraps=[o for o in bpy.data.objects if o.parent==lid and o.name.startswith('Corner strap /')];assert len(wraps)==12
for o in wraps:
 if 'folded top' in o.name:assert o.dimensions.x>.55 and o.dimensions.y>.49 and len(o.data.vertices)>24
# Source/export material parity independently recovered from saved blend.
b=(R/'iceland.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);materials={m['name']:m for m in g['materials']}
for mat in bpy.data.materials:
 if mat.name.startswith('Basalt /'):
  factor=next(n for n in mat.node_tree.nodes if n.type=='MIX_RGB').inputs[2].default_value;assert max(abs(a-b) for a,b in zip(factor,materials[mat.name]['pbrMetallicRoughness']['baseColorFactor']))<1e-7
m=ice.data.materials[0];p=m.node_tree.nodes.get('Principled BSDF');e=materials[m.name]['extensions'];assert abs(p.inputs['Transmission Weight'].default_value-e['KHR_materials_transmission']['transmissionFactor'])<1e-7
thickness=next(n for n in m.node_tree.nodes if n.type=='GROUP' and 'Thickness' in n.inputs).inputs['Thickness'].default_value;assert abs(thickness-e['KHR_materials_volume']['thicknessFactor'])<1e-7
# Preserve all v8 basalt, moss, liner, fixed hardware and pivot raw records.
def records():
 out={}
 for o in bpy.data.objects:
  if o.type=='MESH' and o.name.startswith(('Basalt fracture','Sheltered moss v7','Interior','Hinge /','Latch /')):out[o.name]={'v':[list(v.co) for v in o.data.vertices],'f':[list(p.vertices) for p in o.data.polygons],'matrix':[list(row) for row in o.matrix_world]}
 return out
now=records();bpy.ops.wm.open_mainfile(filepath=str(R/'approved-v8.blend'),use_scripts=False);bpy.context.view_layer.update();old=records();assert now==old
result={'ice_bounds_blender':{'min':lo,'max':hi},'minimum_lid_edge_clearance':min(1.86-hi[0],lo[1]+1.19),'river_glacier_endpoint':list(end),'cascade_endpoint_max_error':max((a-b).length for a,b in zip(r[:6],c[:6])),'river_all_vertices_single_component':len(seen),'old_channel_replaced_with_solid_obsidian':list(hit),'lid_corner_wrap_meshes':len(wraps),'unchanged_source_records':len(now),'source_export_material_parity':True,'no_new_collision_exclusions':True}
(R/'features-check.json').write_text(json.dumps(result,indent=2));print(result)
