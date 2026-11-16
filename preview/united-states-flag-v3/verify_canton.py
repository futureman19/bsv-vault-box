"""Reopened saved-source UV regression and exact v2 geometric preservation."""
import bpy,json,hashlib,struct
import numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import barycentric_transform
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
OLD=R.parent/'united-states-flag-v2'
def snapshot(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False);bpy.context.view_layer.update()
 return {o.name:dict(parent=o.parent.name if o.parent else None,matrix=[list(r) for r in o.matrix_world],vertices=[list(v.co) for v in o.data.vertices] if o.type=='MESH' else [],polygons=[list(p.vertices) for p in o.data.polygons] if o.type=='MESH' else []) for o in bpy.data.objects if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']}
a=snapshot(OLD/'united-states.blend');b=snapshot(R/'united-states.blend');assert a==b
for f in ['mechanism.blend','motion.mjs','viewer.js','viewer.bundle.js','fireworks.js','tests.mjs']:
 assert (OLD/f).read_bytes()==(R/f).read_bytes(),f
# Sample the actual saved wall mesh UVs through triangle barycentrics, not just generator formulas.
def footprint(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),use_scripts=False);bpy.context.view_layer.update()
 data={}
 for o in bpy.data.objects:
  if not o.name.startswith('Flag body'):continue
  m=o.data;m.calc_loop_triangles();vs=[o.matrix_world@v.co for v in m.vertices]
  tris=list(m.loop_triangles);tree=BVHTree.FromPolygons(vs,[list(t.vertices) for t in tris],all_triangles=True)
  mat=o.data.materials[0];im=next(n.image for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and 'wall' in n.image.name)
  pixels=np.asarray(im.pixels[:]).reshape(im.size[1],im.size[0],4)
  data[o.name]=(o,m,vs,tris,tree,pixels)
 mask=[]
 for j in range(40):
  row=[];z=.13+(j+.5)*1.40/40
  for i in range(496):
   s=(i+.5)*12.4/496
   if s<3.72:point=Vector((1.86-s,1.24,z));direction=Vector((0,-1,0));kind='long';side=1
   elif s<6.20:point=Vector((-1.86,1.24-(s-3.72),z));direction=Vector((1,0,0));kind='side';side=-1
   elif s<9.92:point=Vector((s-6.20-1.86,-1.24,z));direction=Vector((0,1,0));kind='long';side=-1
   else:point=Vector((1.86,s-9.92-1.24,z));direction=Vector((-1,0,0));kind='side';side=1
   # Raycast all four walls: front/rear walls cover side-wall butt-joint endpoints.
   hits=[]
   for item in data.values():
    hit,normal,idx,dist=item[4].ray_cast(point-direction*.15,direction,.5)
    if hit is not None:hits.append((dist,item,hit,idx))
   if not hits:row.append(-1);continue
   dist,item,hit,idx=min(hits,key=lambda v:v[0]);o,m,vs,tris,tree,pixels=item
   t=tris[idx];uvs=[Vector((*m.uv_layers.active.data[l].uv,0)) for l in t.loops]
   uv=barycentric_transform(hit,*[vs[v] for v in t.vertices],*uvs)
   # Original uses repeat; successor uses EXTEND. Exactly reproduce sampler semantics.
   if path.parent==OLD:u,v=uv.x%1,uv.y%1
   else:u,v=max(0,min(1,uv.x)),max(0,min(1,uv.y))
   pix=pixels[min(pixels.shape[0]-1,int(v*pixels.shape[0])),min(pixels.shape[1]-1,int(u*pixels.shape[1]))]
   row.append(int(pix[2]>pix[0]*1.5 and pix[0]<.15))
  mask.append(row)
 mask=np.array(mask)
 # Vertical OR closes white star holes, leaving actual navy interval footprint.
 cols=(mask==1).any(axis=0);runs=int(np.sum(cols & ~np.roll(cols,1)))
 lower=int((mask[:16]==1).sum());upper=int((mask[28:]==1).sum())
 # Each sampled upper left face must have navy and no intervening striped face reset.
 return dict(navy_perimeter_runs=runs,lower_navy_samples=lower,upper_navy_samples=upper,navy_columns=int(cols.sum()),grid=[496,40],unsampled_corner_points=int((mask<0).sum()))
old=footprint(OLD/'united-states.blend');new=footprint(R/'united-states.blend')
assert new['navy_perimeter_runs']==1,new
assert new['lower_navy_samples']==0 and new['upper_navy_samples']>1000,new
assert old['navy_perimeter_runs']>1,old
# Export sampler MUST clamp: no outside-domain wrapped star field.
def glb(path):
 raw=path.read_bytes();n=struct.unpack_from('<I',raw,12)[0];return json.loads(raw[20:20+n])
g=glb(R/'united-states.glb');assert all(s.get('wrapS')==33071 and s.get('wrapT')==33071 for s in g['samplers'])
out=dict(PASS=True,negative_control_v2=old,v3=new,all_collectible_geometry_transforms_parentage_exact_v2=True,unchanged_objects=len(a),runtime_bundle_fireworks_motion_byte_identical=True,glb_all_samplers_clamp_to_edge=True,lid='Separate moving surface aligned at x=-0.15; not a second body canton',rear='Unseen reference rear extrapolated as continuation around left end')
(R/'canton-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
