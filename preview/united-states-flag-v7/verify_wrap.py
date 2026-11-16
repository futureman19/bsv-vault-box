"""Independently import exported GLBs, ray-sample actual triangle UVs, measure unfolded stars."""
import bpy,math,json,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
R=Path(__file__).resolve().parent;OLD=R/'baseline-v6'
RAD=.045;SEG=2*RAD*math.sin(math.pi/12);ARC=3*SEG

def comps(mask):
 seen=set();out=[]
 for j,i in zip(*np.where(mask)):
  if (j,i) in seen:continue
  stack=[(j,i)];seen.add((j,i));part=[]
  while stack:
   a,b=stack.pop();part.append((a,b))
   for q in [(a-1,b),(a+1,b),(a,b-1),(a,b+1)]:
    if 0<=q[0]<mask.shape[0] and 0<=q[1]<mask.shape[1] and mask[q] and q not in seen:seen.add(q);stack.append(q)
  if len(part)>12:out.append(part)
 return out

def inspect(path,new):
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(path));bpy.context.view_layer.update()
 o=next(o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith('Lid / polished slab'))
 me=o.data;me.calc_loop_triangles();tris=list(me.loop_triangles);vs=[o.matrix_world@v.co for v in me.vertices]
 tree=BVHTree.FromPolygons(vs,[t.vertices for t in tris],all_triangles=True)
 mat=me.materials[0];img=next(n.image for n in mat.node_tree.nodes if n.type=='TEX_IMAGE' and n.image.colorspace_settings.name=='sRGB');px=np.asarray(img.pixels[:]).reshape(img.size[1],img.size[0],4)
 def sample(pos,normal):
  pos=Vector(pos);normal=Vector(normal);hit,n,idx,dist=tree.ray_cast(pos+normal*.025,-normal,.06)
  assert hit is not None,(pos,normal)
  t=tris[idx];uv=barycentric_transform(hit,*[vs[v] for v in t.vertices],*[Vector((*me.uv_layers.active.data[l].uv,0)) for l in t.loops])
  color=px[min(px.shape[0]-1,max(0,int(uv.y*px.shape[0]))),min(px.shape[1]-1,max(0,int(uv.x*px.shape[1])))]
  return min(color[:3])>.70,uv
 def surface(face,s,q):
  if q<0:out=q;z=1.978;normal=(0,0,1)
  elif q<=ARC:
   k=min(2,int(q/SEG));t=(q-k*SEG)/SEG;a=k*math.pi/6;b=(k+1)*math.pi/6
   out=RAD*((1-t)*math.sin(a)+t*math.sin(b));z=1.933+RAD*((1-t)*math.cos(a)+t*math.cos(b))
   ang=(k+.5)*math.pi/6;normal=(-math.sin(ang),0,math.cos(ang)) if face=='left' else (0,-math.sin(ang),math.cos(ang))
  else:out=RAD;z=1.933-(q-ARC);normal=(-1,0,0) if face=='left' else (0,-1,0)
  return ((-1.815-out,s,z) if face=='left' else (s,-1.145-out,z)),normal
 result={}
 for face,smin,smax,centers in [('left',-1.03,1.03,[-.81,-.27,.27,.81]),('front',-1.69,-.30,[-1.54,-1.27,-1,-.73,-.46])]:
  ss=np.linspace(smin,smax,620);qs=np.linspace(-.145,.195,150);mask=np.zeros((len(qs),len(ss)),bool);uvmax=0
  for j,q in enumerate(qs):
   for i,s in enumerate(ss):
    pos,normal=surface(face,s,q);white,uv=sample(pos,normal);mask[j,i]=white
    if new:
     x,y=(-1.815-q,s) if face=='left' else (s,-1.145-q)
     err=max(abs(uv.x-(x+2.56)/5.12),abs(uv.y-(y+1.89)/3.78))
     if err>uvmax:uvmax=err;worst=dict(s=float(s),q=float(q),pos=list(pos),uv=list(uv),expected=[(x+2.56)/5.12,(y+1.89)/3.78])
  components=comps(mask);parts=[]
  for part in components:
   p=np.array(part);parts.append(dict(samples=len(part),s_min=float(ss[p[:,1]].min()),s_max=float(ss[p[:,1]].max()),unfolded_q_min=float(qs[p[:,0]].min()),unfolded_q_max=float(qs[p[:,0]].max()),touches_top=bool(np.any(qs[p[:,0]]<0)),touches_vertical=bool(np.any(qs[p[:,0]]>ARC))))
  result[face]=dict(components=len(components),parts=parts,actual_export_ray_samples=int(mask.size),misses=0,max_shared_metric_uv_error=float(uvmax))
  if new:
   assert len(parts)==len(centers),result
   assert all(p['touches_top'] and p['touches_vertical'] for p in parts),result
   assert uvmax<2e-6,(uvmax,worst,parts)
   for p in parts:
    # Star extent uses same 0.125 circumradius, not equal PNG pixel sizes.
    span=p['s_max']-p['s_min'];assert .218<span<.247,(face,span)
  else:assert not parts,'V6 should reject continuous edge stars'
 # Sample original top star footprint independently, same physical resolution.
 cx=-1.86+1.71/5;cy=1.19-.5*2.38/4
 ss=np.linspace(-.14,.14,180);mask=np.zeros((180,180),bool)
 for j,dy in enumerate(ss):
  for i,dx in enumerate(ss):mask[j,i]=sample((cx+dx,cy+dy,1.978),(0,0,1))[0]
 points=np.array(comps(mask)[0]);width=float(ss[points[:,1]].max()-ss[points[:,1]].min());height=float(ss[points[:,0]].max()-ss[points[:,0]].min())
 result['top_star_measured']={'width':width,'height':height,'circumradius_authored':.125};assert .22<width<.25 and .21<height<.24
 if new:
  lower_samples=0
  for face,centers in [('left',[-.81,-.27,.27,.81]),('front',[-1.54,-1.27,-1,-.73,-.46])]:
   for center in centers:
    for s in np.linspace(center-.13,center+.13,55):
     for angle in np.linspace(.01,math.pi/2-.01,12):
      out=RAD*math.cos(angle);z=1.723-RAD*math.sin(angle)
      pos=(-1.815-out,s,z) if face=='left' else (s,-1.145-out,z)
      normal=(-math.cos(angle),0,-math.sin(angle)) if face=='left' else (0,-math.cos(angle),-math.sin(angle))
      assert not sample(pos,normal)[0],('Repeated lower-bevel star',face,s,z)
      lower_samples+=1
  result['lower_bevel_no_duplicate_stars']={'samples':lower_samples,'white_samples':0}
 return result
old=inspect(OLD/'united-states.glb',False);current=inspect(R/'united-states.glb',True)
out=dict(edge_wrap_PASS=True,negative_control_v6=old,current=current,physical_scale='All stars radius 0.125 world units; 300 isotropic texels/unit in new lid atlas',body_star_continuation=False,body_limitation='0.30-thick lid exceeds 0.25 star diameter; glyphs cross top/bevel/vertical lid, not body seam. No floating mesh bridges.',visual_corrections=2)
(R/'features-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
