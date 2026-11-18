import bpy,sys,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];slug=sys.argv[sys.argv.index('--')+1];root=R/'preview'/f'{slug}-repair-v2'
def snap(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False);bpy.context.view_layer.update();out={}
 for o in bpy.data.objects:
  if o.type not in ['MESH','EMPTY'] or o.name.startswith('Studio'):continue
  d={'parent':o.parent.name if o.parent else None,'matrix':[list(row) for row in o.matrix_world]}
  if o.type=='MESH':
   d.update(vertices=[list(v.co) for v in o.data.vertices],faces=[list(p.vertices) for p in o.data.polygons],uv=[list(x.uv) for x in o.data.uv_layers.active.data] if o.data.uv_layers.active else [],materials=[m.name for m in o.data.materials])
  if o.type=='MESH':
   d['polygon_material_indices']=[p.material_index for p in o.data.polygons]
   d['modifiers']=[(m.name,m.type,[(p.identifier,str(getattr(m,p.identifier))) for p in m.bl_rna.properties if p.type in ['BOOLEAN','INT','FLOAT','STRING','ENUM'] and p.identifier!='rna_type']) for m in o.modifiers]
  out[o.name]=d
 mats={}
 for m in bpy.data.materials:
  if not m.use_nodes:continue
  mats[m.name]=[(n.name,n.type,[(i.name,str(i.default_value[:]) if hasattr(i.default_value,'__len__') else str(i.default_value)) for i in n.inputs if hasattr(i,'default_value')]) for n in m.node_tree.nodes]
  mats[m.name].append(('links',sorted((l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links)))
 images={i.name:hashlib.sha256(bytes(i.packed_file.data)).hexdigest() for i in bpy.data.images if i.packed_file}
 return out,mats,images
old,om,oi=snap(root/'historical-v1'/f'{slug}.blend');new,nm,ni=snap(root/f'{slug}.blend')
assert om==nm and oi==ni,'material/image drift';assert old.keys()==new.keys()
changed=[n for n in old if old[n]!=new[n]]
expected=['Dark seam / long'] if slug=='ghana' else ['Mineral seam / side','Mineral seam / side.001']
assert sorted(changed)==sorted(expected),changed
for name in changed:
 for k in old[name]:
  if k!='vertices':assert old[name][k]==new[name][k],(name,k)
 axis=2 if slug=='ghana' else 1
 for a,b in zip(old[name]['vertices'],new[name]['vertices']):
  assert all(a[i]==b[i] for i in range(3) if i!=axis)
report={'status':'PASS','changed_meshes':changed,'unchanged_object_records':len(old)-len(changed),'all_material_node_inputs_exact':True,'packed_images_exact':True,'changed_mesh_uv_topology_material_parent_transform_exact':True,'changed_coordinate_axis':axis}
(root/'preservation-check.json').write_text(json.dumps(report,indent=2));print(report)
