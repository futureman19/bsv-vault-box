"""Exact original source records and resolved GLB payload verification."""
from pathlib import Path
import bpy,json,struct,hashlib
R=Path(__file__).resolve().parent;S=R.parent/'iceland-polished-v6'
sha=lambda b:hashlib.sha256(b).hexdigest()
def val(x):
 if isinstance(x,(str,int,float,bool)) or x is None:return x
 try:return [val(t) for t in x]
 except:return str(x)
def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False);bpy.context.view_layer.update();objects={}
 for o in bpy.data.objects:
  rec={'type':o.type,'parent':o.parent.name if o.parent else None,'world':val(o.matrix_world),'local':val(o.matrix_local)}
  if o.type=='MESH':
   m=o.data
   modifiers=[]
   for mod in o.modifiers:
    props={}
    for prop in mod.bl_rna.properties:
     if prop.identifier in ['rna_type','execution_time','persistent_uid']:continue
     if prop.type in ['BOOLEAN','INT','FLOAT','STRING','ENUM']:props[prop.identifier]=val(getattr(mod,prop.identifier))
    modifiers.append(props)
   rec.update(vertices=[val(v.co) for v in m.vertices],polygons=[list(p.vertices) for p in m.polygons],material_indices=[p.material_index for p in m.polygons],materials=[m.name for m in o.data.materials],uvs={uv.name:[val(x.uv) for x in uv.data] for uv in m.uv_layers},modifiers=modifiers)
  if o.type=='LIGHT':rec['light']=[o.data.type,o.data.energy,val(o.data.color),getattr(o.data,'size',None)]
  if o.type=='CAMERA':rec['camera']=[o.data.type,o.data.lens,o.data.ortho_scale]
  objects[o.name]=sha(json.dumps(rec,sort_keys=True).encode())
 mats={}
 for m in bpy.data.materials:
  if not m.use_nodes:continue
  nodes=[]
  for n in m.node_tree.nodes:
   nodes.append({'name':n.name,'type':n.bl_idname,'inputs':[(i.name,val(i.default_value)) for i in n.inputs if hasattr(i,'default_value')],'image':n.image.name if hasattr(n,'image') and n.image else None})
  links=[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links]
  mats[m.name]=sha(json.dumps([nodes,links],sort_keys=True).encode())
 images={i.name:sha(bytes(i.packed_file.data)) for i in bpy.data.images if i.packed_file}
 return {'objects':objects,'materials':mats,'images':images}
a=snapshot(S/'iceland.blend');b=snapshot(R/'iceland.blend')
for kind,records in a.items():
 assert all(b[kind].get(n)==v for n,v in records.items()),[kind,[n for n,v in records.items() if b[kind].get(n)!=v]]
assert all(n.startswith('Sheltered moss v7') for n in b['objects'].keys()-a['objects'].keys())
def glb(path):
 data=path.read_bytes();ln=struct.unpack_from('<I',data,12)[0];j=json.loads(data[20:20+ln]);binary=data[28+ln:]
 def accessor(i):
  a=dict(j['accessors'][i]);v=j['bufferViews'][a.pop('bufferView')];offset=v.get('byteOffset',0)+a.pop('byteOffset',0)
  components={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}[a['type']];size={5120:1,5121:1,5122:2,5123:2,5125:4,5126:4}[a['componentType']]*components;stride=v.get('byteStride',size)
  content=b''.join(binary[offset+k*stride:offset+k*stride+size] for k in range(a['count']))
  return [a,sha(content)]
 meshes={}
 for m in j['meshes']:
  prim=[]
  for p in m['primitives']:
   p=dict(p);p['attributes']={k:accessor(i) for k,i in p['attributes'].items()}
   if 'indices' in p:p['indices']=accessor(p['indices'])
   if 'material' in p:p['material']=j['materials'][p['material']]['name']
   prim.append(p)
  meshes[m['name']]=prim
 nodes={}
 for n in j['nodes']:
  p=dict(n)
  if 'mesh' in p:p['mesh']=j['meshes'][p['mesh']]['name']
  if 'children' in p:p['children']=[j['nodes'][i]['name'] for i in p['children']]
  nodes[n['name']]=p
 # Resolve texture references to exact image bytes so shifted indices are harmless.
 def resolve(x,key=''):
  if isinstance(x,dict):
   if 'index' in x and ('Texture' in key):
    x=dict(x);t=j['textures'][x.pop('index')];im=j['images'][t['source']];v=j['bufferViews'][im['bufferView']];x['image_sha256']=sha(binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']]);x['sampler']=j.get('samplers',[])[t['sampler']] if 'sampler' in t else None
   return {k:resolve(v,k) for k,v in x.items()}
  if isinstance(x,list):return [resolve(v,key) for v in x]
  return x
 return {'meshes':meshes,'nodes':nodes,'materials':{m['name']:resolve(m) for m in j['materials']},'animations':j.get('animations',[])}
g=glb(S/'iceland.glb');h=glb(R/'iceland.glb')
for kind in ['meshes','nodes','materials']:
 bad=[n for n,v in g[kind].items() if h[kind].get(n)!=v];assert not bad,(kind,bad)
assert g['animations']==h['animations']==[]
for name in ['viewer.js','motion.mjs','template.html','viewer.bundle.js']:assert (S/name).read_bytes()==(R/name).read_bytes(),name
result={'source_original_object_records_exact':len(a['objects']),'source_original_material_records_exact':len(a['materials']),'source_original_packed_images_exact':len(a['images']),'glb_original_mesh_accessor_bytes_exact':len(g['meshes']),'glb_original_node_records_exact':len(g['nodes']),'glb_original_material_records_exact':len(g['materials']),'new_moss_objects':len(b['objects'])-len(a['objects']),'viewer_lighting_camera_motion_bundle_byte_identical':True,'all_original_records_including_old_moss_unchanged':True}
(R/'nonmoss-preservation-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
