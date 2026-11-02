"""Bounded geometry-only cedar/moss refinement; saved approved source is the base."""
import bpy,bmesh,math,random,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(20261101)
bpy.ops.wm.open_mainfile(filepath=str(R/'baseline.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];bark=bpy.data.materials['Cedar / furrowed bark'];leafm=[bpy.data.materials['Cedar foliage / '+str(i)] for i in range(4)]
def eligible(o):return not (o.name.startswith('Cedar tree / branch') or o.name.startswith('Cedar tree / foliage') or o.name.startswith('Terrain / moss') or o.name.startswith('Studio'))
def fingerprint():
 d={}
 for o in bpy.data.objects:
  if not eligible(o):continue
  rec={'parent':o.parent.name if o.parent else None,'matrix':[list(row) for row in o.matrix_local]}
  if o.type=='MESH':rec.update(vertices=[list(v.co) for v in o.data.vertices],faces=[list(p.vertices) for p in o.data.polygons],materials=[m.name for m in o.data.materials],uv=[list(x.uv) for x in o.data.uv_layers.active.data] if o.data.uv_layers.active else [])
  d[o.name]=hashlib.sha256(json.dumps(rec,sort_keys=True).encode()).hexdigest()
 return d
frozen=fingerprint()
for o in list(bpy.data.objects):
 if o.name.startswith(('Cedar tree / branch','Cedar tree / foliage','Terrain / moss')):bpy.data.objects.remove(o,do_unlink=True)
def mesh(n,vs,fs,m):
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(m)
 for f in me.polygons:f.use_smooth=True
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=lid;o.matrix_world=mw;return o
# Each real tapering branch supports overlapping irregular 3D needle sprays.
vs=[[] for _ in leafm];fs=[[] for _ in leafm]
def needle(q,d,w,length,mi):
 d=d.normalized();side=d.cross(Vector((0,0,1))).normalized()*w;mid=q+d*length*.42;n=len(vs[mi]);vs[mi].extend([q,mid+side,q+d*length,mid-side+Vector((0,0,w*.45))]);fs[mi].extend([(n,n+1,n+2),(n,n+2,n+3)])
for k in range(30):
 tier=k//6;level=tier/4;az=k*2.399+random.uniform(-.30,.30);rad=[.37,.39,.32,.23,.12][tier]*random.uniform(.78,1.15)
 start=Vector((.63+.015*math.sin(k),.78,2.40+tier*.115+random.uniform(-.025,.025)));direction=Vector((math.cos(az),math.sin(az),0));tip=start+direction*rad+Vector((0,0,random.uniform(-.025,.045)));mid=start.lerp(tip,.55)+Vector((0,0,.015));points=[start,mid,tip];vv=[];ff=[]
 for i,c in enumerate(points):
  tangent=(points[min(2,i+1)]-points[max(0,i-1)]).normalized();a=tangent.cross(Vector((0,0,1))).normalized();bb=tangent.cross(a).normalized();radius=[.013*(1-level*.65),.007,.0018][i]
  for j in range(7):vv.append(c+radius*(a*math.cos(j*math.tau/7)+bb*math.sin(j*math.tau/7)))
 for i in range(2):
  for j in range(7):a=i*7+j;b=i*7+(j+1)%7;ff.append((a,b,b+7,a+7))
 ff.extend([tuple(reversed(range(7))),tuple(14+j for j in range(7))]);mesh('Cedar tree / branch '+str(k),vv,ff,bark)
 for j in range(10):
  t=.18+j*.078;c=start.lerp(tip,t)+Vector((0,0,.012*math.sin(t*math.pi)))
  for sign in [-1,1]:
   angle=az+sign*random.uniform(.65,1.05);spraylen=random.uniform(.075,.125)*(1-level*.4)*(1-t*.27);end=c+Vector((math.cos(angle)*spraylen,math.sin(angle)*spraylen,random.uniform(-.025,.035)))
   for h in range(6):
    q=c.lerp(end,h/6);theta=angle+(1 if h%2 else -1)*random.uniform(.55,1.05);d=Vector((math.cos(theta),math.sin(theta),random.uniform(-.25,.65)));needle(q,d,random.uniform(.015,.021)*(1-level*.2),random.uniform(.065,.095)*(1-level*.3),random.choices(range(4),[2,4,4,1])[0])
for i in range(4):mesh('Cedar tree / foliage '+str(i),vs[i],fs[i],leafm[i])
# Continuous low conforming moss with irregular stone windows, not hovering blobs.
rock=bpy.data.objects['Terrain / granite'];bpy.context.view_layer.update();inv=rock.matrix_world.inverted()
def surface(x,y):
 hit,co,no,idx=rock.ray_cast(inv@Vector((x,y,3)),Vector((0,0,-1)))
 return rock.matrix_world@co if hit else None
mats=[]
for i,c in enumerate([(.08,.135,.025),(.12,.19,.035),(.16,.23,.047)]):
 m=bpy.data.materials.new('Moss / textured carpet '+str(i));m.diffuse_color=(*c,1);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*c,1);bs.inputs['Roughness'].default_value=.95;mats.append(m)
vv=[];ff=[];coords={};step=.021
for iy in range(34):
 for ix in range(48):
  x=.12+ix*step;y=.405+iy*step;co=surface(x,y)
  if co is None or co.z<1.995:continue
  # Coverage follows most sheltered mound but reveals irregular granite islands.
  field=math.sin(x*29+y*17)+.65*math.sin(y*41-x*13)+.35*math.cos(x*61+y*37)
  if field<-1.65:continue
  coords[ix,iy]=len(vv);vv.append(co+Vector((0,0,.004+random.random()*.004)))
for (ix,iy),a in coords.items():
 for keys in [[(ix,iy),(ix+1,iy),(ix,iy+1)],[(ix+1,iy),(ix+1,iy+1),(ix,iy+1)]]:
  if all(key in coords for key in keys):ff.append(tuple(coords[key] for key in keys))
o=mesh('Terrain / moss carpet',vv,ff,mats[0]);o.data.materials.append(mats[1]);o.data.materials.append(mats[2])
for f in o.data.polygons:f.material_index=random.choices(range(3),[3,5,2])[0]
# Fine attached awl tufts add rough silhouette and breakup at ordinary viewing scale.
tv=[];tf=[]
for co in vv:
 if random.random()>.48:continue
 for j in range(2):
  angle=random.random()*math.tau;d=Vector((math.cos(angle),math.sin(angle),0));n=len(tv);w=random.uniform(.002,.004);height=random.uniform(.008,.016);tv.extend([co-d*w,co+d*w,co+Vector((0,0,height))+d*.002]);tf.append((n,n+1,n+2))
mesh('Terrain / moss filaments',tv,tf,mats[1])
# glTF exports surfaces, not isolated grid sample points: remove loose source verts.
for obj in bpy.data.objects:
 if obj.type=='MESH' and obj.name.startswith('Terrain / moss'):
  bm=bmesh.new();bm.from_mesh(obj.data);loose=[v for v in bm.verts if not v.link_faces];bmesh.ops.delete(bm,geom=loose,context='VERTS');bm.to_mesh(obj.data);bm.free()
assert fingerprint()==frozen,'Non-tree/moss object drift'
(R/'mechanism-preservation.json').write_text(json.dumps({'unchanged_object_fingerprints':frozen,'exact_raw_mesh_uv_material_names_and_local_matrices':True,'viewer_and_motion':'copied byte-identically from v1'},indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(R/'japan.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'japan.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
bpy.context.scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('REFINED',len(vv),'moss vertices',sum(len(x) for x in fs),'foliage triangles')
