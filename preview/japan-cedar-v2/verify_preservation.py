import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent
def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False);out={}
 for o in bpy.data.objects:
  if o.name.startswith(('Cedar tree / branch','Cedar tree / foliage','Terrain / moss','Studio')):continue
  d={'parent':o.parent.name if o.parent else None,'matrix':[list(row) for row in o.matrix_local]}
  if o.type=='MESH':
   d.update(vertices=[list(v.co) for v in o.data.vertices],polygons=[list(p.vertices) for p in o.data.polygons],uv=[list(x.uv) for x in o.data.uv_layers.active.data] if o.data.uv_layers.active else [],modifiers=[(m.name,m.type) for m in o.modifiers],materials=[])
   for m in o.data.materials:
    nodes=[]
    for n in m.node_tree.nodes:
     vals={}
     for s in n.inputs:
      if hasattr(s,'default_value'):
       v=s.default_value
       try:v=list(v)
       except TypeError:pass
       if isinstance(v,(str,int,float,bool,list)):vals[s.name]=v
     image=n.image if n.type=='TEX_IMAGE' else None
     nodes.append({'name':n.name,'type':n.type,'inputs':vals,'image_sha256':hashlib.sha256(image.packed_file.data).hexdigest() if image and image.packed_file else None})
    d['materials'].append({'name':m.name,'nodes':nodes,'links':[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links]})
  out[o.name]=hashlib.sha256(json.dumps(d,sort_keys=True).encode()).hexdigest()
 return out
a=snapshot(R/'baseline.blend');b=snapshot(R/'japan.blend');assert a==b,[k for k in a if a[k]!=b.get(k)]
base=R.parent/'japan-cedar-v1';runtime={n:(R/n).read_bytes()==(base/n).read_bytes() for n in ['viewer.js','motion.mjs','viewer.bundle.js']};assert all(runtime.values())
report={'independently_reopened_sources':True,'unchanged_object_count':len(a),'unchanged_raw_geometry_uv_matrices_parents_material_nodes_links_packed_maps':True,'runtime_byte_identical':runtime,'object_hashes':a}
(R/'preservation-source-check.json').write_text(json.dumps(report,indent=2));print('PRESERVED',len(a),'objects; runtime',runtime)
