import bpy,json,hashlib,struct,io
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parent;OLD=R/'baseline-v6'
def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False);bpy.context.view_layer.update();out={}
 for o in bpy.data.objects:
  if o.name.startswith('Studio') or o.type not in ['MESH','EMPTY']:continue
  out[o.name]=dict(parent=o.parent.name if o.parent else None,matrix=[list(a) for a in o.matrix_world],vertices=[list(v.co) for v in o.data.vertices] if o.type=='MESH' else [],polygons=[list(p.vertices) for p in o.data.polygons] if o.type=='MESH' else [],materials=[m.name for m in o.data.materials] if o.type=='MESH' else [],uv=[list(t.uv) for t in o.data.uv_layers.active.data] if o.type=='MESH' and o.data.uv_layers.active else [])
 return out
a=snapshot(R/'baseline-v6.blend');b=snapshot(R/'united-states.blend');assert a.keys()==b.keys()
changes={n:[k for k in a[n] if a[n][k]!=b[n][k]] for n in a if a[n]!=b[n]};assert changes=={'Lid / polished slab':['uv']},changes
feet=[o for o in bpy.data.objects if 'stone foot' in o.name];assert len(feet)==4
for o in feet:
 p=o.data.materials[0].node_tree.nodes.get('Principled BSDF');c=p.inputs['Base Color'];assert not c.is_linked and c.default_value[0]>.8 and max(c.default_value[1:3])<.01
 assert all(p.material_index==0 for p in o.data.polygons)
for f in ['viewer.js','viewer.bundle.js','fireworks.js','motion.mjs','tests.mjs','template.html','mechanism.blend','maps/lacquer-roughness.png']:assert (OLD/f).read_bytes()==(R/f).read_bytes(),f
# Imported source already proves geometry equality; compare actual glTF triangle corners,
# allowing UV seams to split vertex records but no geometry/normals changes.
def load(p):
 raw=p.read_bytes();n=struct.unpack_from('<I',raw,12)[0];return json.loads(raw[20:20+n]),raw[28+n:]
def acc(g,raw,i):
 ac=g['accessors'][i];v=g['bufferViews'][ac['bufferView']];n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[ac['type']];dt={5126:'<f4',5123:'<u2',5125:'<u4'}[ac['componentType']];sz=np.dtype(dt).itemsize
 return np.ndarray((ac['count'],n),dtype=dt,buffer=raw,offset=v.get('byteOffset',0)+ac.get('byteOffset',0),strides=(v.get('byteStride',n*sz),sz)).copy()
a,ab=load(OLD/'united-states.glb');b,bb=load(R/'united-states.glb');assert a['nodes']==b['nodes'];assert a['materials']==b['materials'];ntri=0
for am,bm in zip(a['meshes'],b['meshes']):
 assert am['name']==bm['name']
 for ap,bp in zip(am['primitives'],bm['primitives']):
  ai=acc(a,ab,ap['indices']).flatten();bi=acc(b,bb,bp['indices']).flatten();assert len(ai)==len(bi);ntri+=len(ai)//3
  for key in ['POSITION','NORMAL']:
   av=acc(a,ab,ap['attributes'][key])[ai];bv=acc(b,bb,bp['attributes'][key])[bi];assert np.array_equal(av,bv),(am['name'],key,float(abs(av-bv).max()))
# Compare decoded authored pixels to actual GLB payloads and preserve non-band wall.
def pixels(path):
 im=bpy.data.images.load(str(path),check_existing=False);return np.asarray(im.pixels[:]).reshape(im.size[1],im.size[0],4)
wa=pixels(OLD/'maps/flag-wall.png');wb=pixels(R/'maps/flag-wall.png');diff=np.any(wa!=wb,axis=2)
assert np.all(wa[diff,:3]>.7) and np.all(wb[diff,0]<.15) and np.all(wb[diff,2]>wb[diff,0]*1.5)
out=dict(PASS=True,exact_saved_geometry_pivots_material_ownership=True,source_objects=len(changes) if False else len(a['nodes']),changed_source_records=changes,exact_exported_triangle_positions_normals=ntri,all_nodes_materials_exact=True,four_constant_red_feet=True,runtime_fireworks_motion_template_roughness_exact=True,body_change_only_removes_v6_white_stars=True)
(R/'identity-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
