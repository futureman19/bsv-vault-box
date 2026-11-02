import bpy,json,math,hashlib,sys
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R));from glb_tools import uv

def simple(v):
 if isinstance(v,(int,float,str,bool)):return v
 try:return list(v)
 except:return str(v)
def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False);objs={};mats={}
 for o in bpy.data.objects:
  d={'type':o.type,'matrix':[list(r) for r in o.matrix_world],'parent':o.parent.name if o.parent else None}
  if o.type=='MESH':
   d.update(vertices=[list(v.co) for v in o.data.vertices],faces=[list(f.vertices) for f in o.data.polygons],modifiers=[(m.name,m.type) for m in o.modifiers])
   if not o.name.startswith('Rose stone'):d.update(uv=[[list(x.uv) for x in layer.data] for layer in o.data.uv_layers],materials=[m.name for m in o.data.materials])
  if o.type=='LIGHT':d.update(energy=o.data.energy,color=list(o.data.color))
  if o.type=='CAMERA':d.update(ortho_scale=o.data.ortho_scale,lens=o.data.lens)
  objs[o.name]=d
 for m in bpy.data.materials:
  if m.name.startswith(('Rose ochre','Sandstone','Saturn','Reference /')):continue
  mats[m.name]={'diffuse':list(m.diffuse_color),'nodes':[(n.name,n.type,[(x.name,simple(x.default_value)) for x in n.inputs if hasattr(x,'default_value')],n.image.name if n.type=='TEX_IMAGE' and n.image else '') for n in m.node_tree.nodes] if m.use_nodes else [],'links':[(l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name) for l in m.node_tree.links] if m.use_nodes else []}
 return objs,mats
old=snapshot(R/'baseline/morocco.blend');new=snapshot(R/'morocco.blend');assert old==new,'Source preservation failed'
errs=[]
for o in bpy.data.objects:
 if not o.name.startswith('Rose stone'):continue
 for loop in o.data.loops:
  v=o.matrix_world@o.data.vertices[loop.vertex_index].co;expected=uv(v.x,v.y,v.z,'rear' in o.name)
  actual=o.data.uv_layers.active.data[loop.index].uv;errs.append(max(abs(actual.x-expected[0]),abs(actual.y-expected[1])))
assert max(errs)<2e-6
for name in ['reference-color.png','reference-normal.png','reference-orm.png']:
 im=bpy.data.images[name];assert hashlib.sha256(im.packed_file.data).digest()==hashlib.sha256((R/'maps'/name).read_bytes()).digest()
result={'exact_source_geometry_all_objects':True,'exact_source_nonbody_materials_and_UVs':True,'exact_transforms_parents_cameras_lights':True,'body_source_uv_error':max(errs),'source_packed_maps_match_finalizer_inputs':True,'source_objects_compared':len(new[0]),'nonbody_materials_compared':len(new[1])};(R/'source-preservation-check.json').write_text(json.dumps(result,indent=2));print(result)
