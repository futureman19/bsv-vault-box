"""Independent exported triangle-UV rays across each split star (closed pose)."""
import bpy,math,json,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import barycentric_transform
R=Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.gltf(filepath=str(R/'united-states.glb'));bpy.context.view_layer.update()
meshes=[]
for o in bpy.data.objects:
 if o.type!='MESH' or not o.name.startswith(('Lid / polished slab','Navy seam /','Flag / rim corner','Flag body /')):continue
 m=o.data;m.calc_loop_triangles();ts=list(m.loop_triangles);vs=[o.matrix_world@v.co for v in m.vertices]
 img=next(n.image for n in m.materials[0].node_tree.nodes if n.type=='TEX_IMAGE' and n.image.colorspace_settings.name=='sRGB')
 px=np.array(img.pixels[:]).reshape(img.size[1],img.size[0],4)
 meshes.append((o,m,ts,vs,BVHTree.FromPolygons(vs,[t.vertices for t in ts],all_triangles=True),px))
def sample(face,s,z):
 pos=Vector((-2.2,s,z) if face=='left' else (s,-1.6,z));direction=Vector((1,0,0) if face=='left' else (0,1,0));best=None
 for o,m,ts,vs,tree,px in meshes:
  hit,normal,idx,dist=tree.ray_cast(pos,direction,.6)
  if hit is None or (best and dist>=best[0]):continue
  t=ts[idx];uv=barycentric_transform(hit,*[vs[v] for v in t.vertices],*[Vector((*m.uv_layers.active.data[l].uv,0)) for l in t.loops]);color=px[min(len(px)-1,max(0,int(uv.y*len(px)))),min(px.shape[1]-1,max(0,int(uv.x*px.shape[1]))),:3]
  best=(dist,bool(min(color)>.70),o.name)
 return best
rows=[]
for face,centers in [('left',[-.81,-.27,.27,.81]),('front',[-1.54,-1.27,-1,-.73,-.46])]:
 for center in centers:
  whites=[]
  for s in np.linspace(center-.14,center+.14,101):
   for z in np.linspace(1.59,1.855,121):
    r=sample(face,float(s),float(z))
    if r and r[1]:whites.append((float(s),float(z),r[2]))
  assert whites
  lid=[p for p in whites if p[2].startswith('Lid')];fixed=[p for p in whites if not p[2].startswith('Lid')];assert lid and fixed
  span=max(p[0] for p in whites)-min(p[0] for p in whites);assert .21<span<.26,(face,center,span)
  rows.append(dict(face=face,center=center,width=span,lid_white_samples=len(lid),fixed_white_samples=len(fixed),fixed_objects=sorted({p[2] for p in fixed})))
assert len(rows)==9
lid=next(o for o in bpy.data.objects if o.name.startswith('Lid / polished slab'));z=[(lid.matrix_world@v.co).z for v in lid.data.vertices];assert abs(max(z)-min(z)-.30)<1e-5
out=dict(pass_exported_seam=True,stars=rows,lid_thickness=max(z)-min(z),limitation='Ray samples establish pigment on both independently moving and fixed surfaces; physical .006 closure gap remains. Star tops no longer fold from lid top; 14 top stars are separate original-size glyphs. Rim is the fixed body continuation.')
(R/'seam-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
