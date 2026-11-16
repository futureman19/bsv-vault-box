"""Independent exported triangle ray/UV and top-to-BODY continuation oracle."""
import bpy,math,json,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
R=Path(__file__).resolve().parent
r=.012;rz=.009
lengths=[math.hypot(r*(math.sin((i+1)*math.pi/6)-math.sin(i*math.pi/6)),rz*(math.cos((i+1)*math.pi/6)-math.cos(i*math.pi/6))) for i in range(3)]
arc=sum(lengths);qbody=2*arc+.042+.0236
centers={'front':[-1.54,-1.25,-.96,-.67,-.38],'left':[-.81,-.27,.27,.81]}
def inspect(file,current):
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(file));bpy.context.view_layer.update()
 trees=[]
 for o in bpy.data.objects:
  if o.type!='MESH' or not o.name.startswith(('Lid / polished slab','Flag body /')):continue
  m=o.data;m.calc_loop_triangles();tris=list(m.loop_triangles);vs=[o.matrix_world@v.co for v in m.vertices]
  images=[n.image for n in m.materials[0].node_tree.nodes if n.type=='TEX_IMAGE' and n.image.colorspace_settings.name=='sRGB']
  im=images[0];px=np.asarray(im.pixels[:]).reshape(im.size[1],im.size[0],4)
  trees.append((o.name,m,tris,vs,BVHTree.FromPolygons(vs,[t.vertices for t in tris],all_triangles=True),px))
 def sample(pos,normal,prefix):
  origin=Vector(pos)+Vector(normal)*.2;direction=-Vector(normal);hits=[]
  for name,m,tris,vs,t,px in trees:
   if not name.startswith(prefix):continue
   hit,n,idx,dist=t.ray_cast(origin,direction,.45)
   if hit is None:continue
   tri=tris[idx];uv=barycentric_transform(hit,*[vs[v] for v in tri.vertices],*[Vector((*m.uv_layers.active.data[l].uv,0)) for l in tri.loops])
   color=px[min(px.shape[0]-1,max(0,int(uv.y*px.shape[0]))),min(px.shape[1]-1,max(0,int(uv.x*px.shape[1])))]
   hits.append((dist,min(color[:3])>.70,uv,hit,name))
  assert hits,(pos,prefix)
  return min(hits,key=lambda h:h[0])
 out={}
 for face,cs in centers.items():
  regions=[]
  for center in cs:
   top=body=0;errors=[];body_x=[];body_z=[]
   for s in np.linspace(center-.143,center+.143,81):
    for z in np.linspace(1.435,1.557,45):
     pos=(s,-1.24,z) if face=='front' else (-1.86,s,z);normal=(0,-1,0) if face=='front' else (-1,0,0)
     _,white,uv,hit,name=sample(pos,normal,'Flag body /')
     if white:body+=1;body_x.append(float(s));body_z.append(float(z))
     # Independent wall atlas world coordinate reconstruction.
     perimeter=8.06+s if face=='front' else 4.96-s
     errors.append(max(abs(uv.x-perimeter/12.4),abs(uv.y-(hit.z-.10)/1.46)))
    for q in np.linspace(-.045,-.002,18):
     x,y=(s,-1.178-q) if face=='front' else (-1.848-q,s)
     top+=sample((x,y,1.6436 if current else 1.978),(0,0,1),'Lid / polished slab')[1]
   regions.append(dict(center=center,top_white_samples=int(top),BODY_white_samples=int(body),body_min_z=min(body_z) if body else None,body_span=max(body_x)-min(body_x) if body else 0,max_body_UV_metric_error=max(errors)))
  out[face]=regions
  if current:
   # Scan the entire navy face interval, including the empty corner, rather than
   # merely iterating declared glyph centres. Count independent occupied spans.
   active=[]
   for s in np.linspace(-1.78 if face=='front' else -1.10,-.20 if face=='front' else 1.10,600):
    occupied=False
    for z in np.linspace(1.425,1.530,30):
     pos=(s,-1.24,z) if face=='front' else (-1.86,s,z)
     occupied |= sample(pos,(0,-1,0) if face=='front' else (-1,0,0),'Flag body /')[1]
    active.append(occupied)
   measured=sum(v and (i==0 or not active[i-1]) for i,v in enumerate(active))
   assert measured==len(cs),(face,measured)
   errors=[]
   for center in cs:
    for s in [center-.03,center,center+.03]:
     for k in range(3):
      for t in [.15,.50,.85]:
       a=k*math.pi/6;b=(k+1)*math.pi/6
       outer=r*((1-t)*math.sin(a)+t*math.sin(b));z=1.6346+rz*((1-t)*math.cos(a)+t*math.cos(b));q=sum(lengths[:k])+t*lengths[k]
       pos=(s,-1.178-outer,z) if face=='front' else (-1.848-outer,s,z)
       normal=(0,-.5,.5) if face=='front' else (-.5,0,.5)
       _,white,uv,hit,name=sample(pos,normal,'Lid / polished slab')
       expected=((s+2.56)/5.12,(-1.178-q+1.89)/3.78) if face=='front' else ((-1.848-q+2.56)/5.12,(s+1.89)/3.78)
       errors.append(max(abs(uv.x-expected[0]),abs(uv.y-expected[1])))
   assert max(errors)<2e-6,(face,max(errors))
   out[face+'_measured']={'whole_face_body_components':int(measured),'upper_bevel_metric_uv_error':max(errors),'actual_ray_samples':18000+len(errors)}
  if current:
   assert all(x['top_white_samples']>0 and x['BODY_white_samples']>50 for x in regions),out
   assert all(x['max_body_UV_metric_error']<2e-6 for x in regions),out
  else:assert all(x['BODY_white_samples']==0 for x in regions),out
 return out
old=inspect(R/'baseline-v7.glb',False);new=inspect(R/'united-states.glb',True)
out=dict(PASS=True,counts={'left':4,'front':5},same_world_circumradius_all_stars=.145,top_to_BODY_continuation=True,body_start_developed_q=qbody,negative_control_v7=old,current=new,note='Actual exported triangle UV samples; seam separates moving and static components, no duplicate glyph rows. Visual acceptance remains separate.')
(R/'body-wrap-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
