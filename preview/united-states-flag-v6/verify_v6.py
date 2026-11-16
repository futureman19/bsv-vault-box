import bpy,json,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import barycentric_transform
R=Path(__file__).resolve().parent;OLD=R.parent/'united-states-flag-v5'
def components(mask):
 seen=set();sizes=[]
 for y,x in zip(*np.where(mask)):
  if (y,x) in seen:continue
  stack=[(y,x)];seen.add((y,x));size=0
  while stack:
   a,b=stack.pop();size+=1
   for q in [(a-1,b),(a+1,b),(a,b-1),(a,b+1)]:
    if 0<=q[0]<mask.shape[0] and 0<=q[1]<mask.shape[1] and mask[q] and q not in seen:seen.add(q);stack.append(q)
  if size>5:sizes.append(size)
 return sizes

def inspect(root):
 bpy.ops.wm.open_mainfile(filepath=str(root/'united-states.blend'),use_scripts=False);bpy.context.view_layer.update()
 snap={o.name:dict(parent=o.parent.name if o.parent else None,matrix=[list(r) for r in o.matrix_world],vertices=[list(v.co) for v in o.data.vertices] if o.type=='MESH' else [],polygons=[list(p.vertices) for p in o.data.polygons] if o.type=='MESH' else [],uv=[list(x.uv) for x in o.data.uv_layers.active.data] if o.type=='MESH' and o.data.uv_layers.active else []) for o in bpy.data.objects if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']}
 feet=[]
 for o in bpy.data.objects:
  if 'stone foot' not in o.name:continue
  m=o.data.materials[0];bs=m.node_tree.nodes.get('Principled BSDF');color=list(bs.inputs['Base Color'].default_value)
  feet.append(dict(name=o.name,material=m.name,color=color,constant=not bs.inputs['Base Color'].is_linked,all_faces=all(p.material_index==0 for p in o.data.polygons)))
 counts={};rays={};dep=bpy.context.evaluated_depsgraph_get()
 cache={}
 for face in ['front','left']:
  mask=np.zeros((64,420),dtype=bool);miss=0
  for j,z in enumerate(np.linspace(1.382,1.552,64)):
   for i,s in enumerate(np.linspace(-1.69,-.30,420) if face=='front' else np.linspace(-1.02,1.02,420)):
    origin=Vector((s,-2,z)) if face=='front' else Vector((-2,s,z));direction=Vector((0,1,0)) if face=='front' else Vector((1,0,0))
    hit,loc,n,idx,o,mat=bpy.context.scene.ray_cast(dep,origin,direction)
    if not hit:miss+=1;continue
    mesh=o.data
    if o.name not in cache:
     mesh.calc_loop_triangles();m=mesh.materials[0];images=[n.image for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and 'wall' in n.image.name]
     cache[o.name]=np.asarray(images[0].pixels[:]).reshape(images[0].size[1],images[0].size[0],4) if images else None
    pixels=cache[o.name]
    if pixels is None:continue
    triangles=[t for t in mesh.loop_triangles if t.polygon_index==idx]
    for t in triangles:
     uv=barycentric_transform(loc,*[o.matrix_world@mesh.vertices[v].co for v in t.vertices],*[Vector((*mesh.uv_layers.active.data[l].uv,0)) for l in t.loops]);break
    color=pixels[min(pixels.shape[0]-1,max(0,int(uv.y*pixels.shape[0]))),min(pixels.shape[1]-1,max(0,int(uv.x*pixels.shape[1])))]
    mask[j,i]=min(color[:3])>.7
  sizes=components(mask);counts[face]=len(sizes);rays[face]=dict(samples=int(mask.size),misses=miss,white_components=sizes)
  assert miss==0
 return snap,dict(counts=counts,feet=feet,rays=rays)
a,old=inspect(OLD);b,new=inspect(R)
differences={n:[k for k in a[n] if a[n][k]!=b[n][k]] for n in a if a[n]!=b[n]}
print('SOURCE_DIFFERENCES',differences,flush=True)
assert a==b,'Saved geometry / UV / transforms / pivots changed'
def passes(x):return x['counts']==dict(front=5,left=4) and len(x['feet'])==4 and all(f['constant'] and f['all_faces'] and f['color'][0]>.8 and max(f['color'][1:3])<.01 for f in x['feet'])
assert not passes(old) and old['counts']==dict(front=0,left=0)
assert passes(new),new
for name in ['viewer.js','viewer.bundle.js','fireworks.js','motion.mjs','tests.mjs','mechanism.blend','maps/flag-lid.png','maps/lacquer-roughness.png']:
 assert (OLD/name).read_bytes()==(R/name).read_bytes(),name
def pixels(path):
 im=bpy.data.images.load(str(path),check_existing=False);return np.asarray(im.pixels[:]).reshape(im.size[1],im.size[0],4)
wa=pixels(OLD/'maps/flag-wall.png');wb=pixels(R/'maps/flag-wall.png');changed=np.any(wa!=wb,axis=2)
assert changed.any() and np.all(wa[changed,:3]<.3) and np.all(wb[changed,:3]>.7)
navya=(wa[:,:,2]>wa[:,:,0]*1.5)&(wa[:,:,0]<.15);navyb=(wb[:,:,2]>wb[:,:,0]*1.5)&(wb[:,:,0]<.15)
assert np.array_equal(navya,navyb|changed)
out=dict(PASS=True,negative_baseline_rejected=old,current=new,exact_saved_geometry_uv_pivots=True,unchanged_objects=len(a),top_lid_roughness_runtime_motion_fireworks_bytes_identical=True,visual_correction_iterations=0)
(R/'features-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
