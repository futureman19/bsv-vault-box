"""Morocco / Atlas & Tile. Generated geometry/maps, not scans. Included mechanism only."""
import bpy,math,random,json,os
PASS=int(os.environ.get('MOROCCO_PASS','3'))
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(604)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
# Increase depth by 0.4 without stretching bearings or changing choreography.
lid.location.y+=.2;latch.location.y-=.4;bpy.data.objects['Latch / pin'].location.y-=.4
for o in bpy.data.objects:
 if o.parent or o.name.startswith('Studio') or o==lid:continue
 if o.name.startswith('Interior'):
  if o.name=='Interior floor' or 'end' in o.name:o.dimensions.y+=.4
  else:o.location.y+=.2 if o.location.y>0 else -.2
 elif o.type=='MESH':o.location.y+=.2 if o.location.y>0 else -.2

def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o

def parent(o,p=lid):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o

def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m

def tex(m,f,socket,non=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/f),check_existing=True)
 if non:t.image.colorspace_settings.name='Non-Color'
 t.image.pack();m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[socket])
wood=mat('Cedar / dark polished longitudinal grain',(.1,.035,.016),.28);tex(wood,'cedar-color.png','Base Color');tex(wood,'cedar-roughness.png','Roughness',True)
stone=mat('Rose ochre / irregular mineral strata',(.55,.25,.14),.43);tex(stone,'rose-stone.png','Base Color')
tex(stone,'stone-roughness.png','Roughness',True)
nt=stone.node_tree;im=nt.nodes.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(R/'maps/stone-normal.png'));im.image.colorspace_settings.name='Non-Color';im.image.pack();nm=nt.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.22;nt.links.new(im.outputs['Color'],nm.inputs['Color']);nt.links.new(nm.outputs['Normal'],nt.nodes.get('Principled BSDF').inputs['Normal'])
rock=mat('Atlas / eroded reddish rock',(.45,.19,.13),.78);tex(rock,'atlas-rock.png','Base Color')
gold=mat('Brass / restrained aged gold',(.43,.28,.095),.32,.82)
grout=mat('Ceramic / warm ivory joints',(.33,.29,.21),.9)
green=mat('Ceramic / deep green glaze',(.006,.085,.036),.42)
ivory=mat('Ceramic / ivory glaze',(.75,.71,.55),.29)
dark=mat('Ceramic / near black green accents',(.012,.035,.025),.26)

def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Shared mapped surface')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   if o.name.startswith('Rose stone'):co=co+o.location
   if abs(p.normal.z)>.7:a,b=co.x/3.72+.5,co.y/2.88+.5
   elif abs(p.normal.y)>.7:a,b=co.x/3.72+.5,co.z/1.6+.5
   else:a,b=(co.y+1.44+3.72)/3.72+.5,co.z/1.6+.5
   layer.data[li].uv=(a,b)

def cube(n,loc,dim,m,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if bevel:
  mod=o.modifiers.new('Soft dressed edge','BEVEL');mod.width=min(bevel,min(dim)*.35);mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Rose stone / front' if sy<0 else 'Rose stone / rear',(0,sy*1.345,.84),(3.72,.19,1.60),stone,bevel=.025)
for sx in [-1,1]:cube('Rose stone / side',(sx*1.755,0,.84),(.21,2.55,1.60),stone,bevel=.025)
cube('Rose stone / clasp seat',(0,-1.455,1.36),(.56,.075,.47),stone,bevel=.02)
# Rear rim is kept away from the original hinge leaf sweep.
for sy in [-1,1]:cube('Rim / long',(0,sy*(1.34 if sy<0 else 1.30),1.618),(3.28,.16 if sy<0 else .08,.108),wood,bevel=.009)
for sx in [-1,1]:cube('Rim / end',(sx*1.74,0,1.618),(.16,2.45,.108),wood,bevel=.009)
slab=cube('Lid / polished slab',(0,0,1.918),(3.72,2.78,.48),wood,lid,.035)
# Four real mosaic beds, flush tesserae and a slim aged brass perimeter.
for sy in [-1,1]:cube('Tile bed / long',(0,sy*1.15,2.16),(3.57,.36,.022),grout,lid,.006)
for sx in [-1,1]:cube('Tile bed / return',(sx*1.605,0,2.16),(.36,1.94,.022),grout,lid,.006)
for sy in [-1,1]:cube('Brass / crown long',(0,sy*1.375,2.161),(3.72,.038,.038),gold,lid,.008)
for sx in [-1,1]:cube('Brass / crown side',(sx*1.843,0,2.161),(.038,2.72,.038),gold,lid,.008)

def tessera(poly,m):
 # Individual closed ceramic prism; inset vertices provide visible fine grout.
 cx=sum(p[0] for p in poly)/len(poly);cy=sum(p[1] for p in poly)/len(poly)
 poly=[(cx+(x-cx)*.94,cy+(y-cy)*.94) for x,y in poly];n=len(poly)
 vs=[(x,y,z) for z in [2.166,2.185] for x,y in poly]
 fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new('Cut geometric ceramic');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Ceramic tessera / '+m.name.split('/')[1].strip(),me);bpy.context.collection.objects.link(o);me.materials.append(m);parent(o)
 if PASS>=2 and len(poly)>4:
   be=o.modifiers.new('Ceramic softened arris','BEVEL');be.width=.0008;be.segments=1
# Square-octagon tessellation: cut-corner emerald octagons, ivory corner diamonds,
# divided ivory/black radial triangles. Repeats are coherent, never random pixels.
def module(cx,cy,size=.35):
 a=size/2;b=a*.41421356
 poly=[(-b,-a),(b,-a),(a,-b),(a,b),(b,a),(-b,a),(-a,b),(-a,-b)]
 tessera([(cx+x,cy+y) for x,y in poly],green)
 # Ivory inset four-point star on each emerald octagon is itself cut into kites.
 # Geometry replaces top central octagon region using higher relief fine inlay.
 for sx in [-1,1]:
  for sy in [-1,1]:
   tessera([(cx+sx*a,cy+sy*a),(cx+sx*b,cy+sy*a),(cx+sx*a,cy+sy*b)],ivory)
 # diamond-shaped ceramic is separated from green by a thin brass-free joint.
 # small raised star at .003 offset prevents coplanar faces.
 for k in range(4):
  ang=k*math.pi/2;pts=[(0,0),(.12,0),(.035,.035),(0,.12)]
  pts=[(cx+x*math.cos(ang)-y*math.sin(ang),cy+x*math.sin(ang)+y*math.cos(ang)) for x,y in pts]
  before=set(bpy.data.objects);tessera(pts,ivory if k%2==0 else dark)
  for o in set(bpy.data.objects)-before:o.location.z+=.022
if PASS<2:
 for sy in [-1,1]:
  for i in range(10):module(-1.575+i*.35,sy*1.15)
 for sx in [-1,1]:
  for i in range(5):module(sx*1.605,-.70+i*.35)
else:
 # Dense non-overlapping eight-point stars with complementary interstitial kites.
 def rosette(cx,cy,a=.0875):
  pts=[]
  for k in range(16):
   t=k*math.pi/8;rad=a*(1 if k%2==0 else .48)
   pts.append((cx+rad*math.cos(t),cy+rad*math.sin(t)))
  tessera(pts,green)
  for k in range(8):
   t=k*math.pi/4;tn=t+math.pi/4;tm=t+math.pi/8
   tessera([(cx+a*math.cos(t),cy+a*math.sin(t)),(cx+a*1.075*math.cos(tm),cy+a*1.075*math.sin(tm)),(cx+a*math.cos(tn),cy+a*math.sin(tn)),(cx+a*.48*math.cos(tm),cy+a*.48*math.sin(tm))],ivory if k%2 else dark)
 for sy in [-1,1]:
  for j in range(2):
   for i in range(20):rosette(-1.6625+i*.175,sy*1.15+(j-.5)*.175)
 for sx in [-1,1]:
  for j in range(10):
   for i in range(2):rosette(sx*1.605+(i-.5)*.175,-.7875+j*.175)
# Low corner wraps, not feet.
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner brass / front wrap',(sx*1.70,sy*1.449,.17),(.32,.023,.24),gold,bevel=.025)
  cube('Corner brass / side wrap',(sx*1.868,sy*1.29,.17),(.023,.30,.24),gold,bevel=.025)
# Continuous irregular ridged mountain surface at rear centre, rooted in lid.
verts=[];faces=[];nx,ny=(65,39) if PASS>=3 else (45,29)
for j in range(ny):
 v=-1+2*j/(ny-1)
 for i in range(nx):
  u=-1+2*i/(nx-1);edge=max(0,1-u*u)*max(0,1-v*v)
  if PASS<3:
   peaks=.48*math.exp(-((u+.10)/.34)**2)+.30*math.exp(-((u+.58)/.25)**2)+.25*math.exp(-((u-.52)/.30)**2)
   ridge=peaks*math.exp(-((v-.15*math.sin(u*7))/.50)**2)
   gullies=(.025*math.sin(u*53+v*9)+.018*math.sin(u*87-v*17))*(1-abs(v))
   z=2.17+edge*(.07+ridge+gullies)
   verts.append((.10+u*.50*math.sqrt(1-v*v*.50),1.04+v*.27*math.sqrt(1-u*u*.50),z))
  else:
   peaks=[(-.48,-.16,.43,.30,.48),(-.13,.17,.74,.32,.56),(.23,-.12,.46,.27,.48),(.54,.23,.35,.31,.53)]
   z=max(h*max(0,1-math.sqrt(((u-px)/wx)**2+((v-py)/wy)**2))**.72 for px,py,h,wx,wy in peaks)
   z+=.10*edge
   drainage=(.027*math.sin(u*71+v*14)+.016*math.sin(u*113-v*21))*min(1,z*5)
   verts.append((.04+u*.68,1.015+v*.30,2.17+max(0,z+drainage)))

for j in range(ny-1):
 for i in range(nx-1):
  a=j*nx+i;faces.extend([(a,a+1,a+nx+1),(a,a+nx+1,a+nx)])
me=bpy.data.meshes.new('Atlas eroded ridge topology');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Atlas ridge / rear centre eroded massif',me);bpy.context.collection.objects.link(o);me.materials.append(rock);uv(o);parent(o)
for f in me.polygons:f.use_smooth=True
# Fixed medallion and low side ring.
def disk(n,loc,r,depth,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=r,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold);m=o.modifiers.new('Brass roundover','BEVEL');m.width=.004;m.segments=3;select(o);bpy.ops.object.modifier_apply(modifier=m.name);return o
disk('Medallion / uninscribed solid brass',(0,-1.455,.82),.19,.028)
disk('Side ring / mount',(-1.88,-.78,.43),.065,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=10,location=(-1.91,-.78,.30),major_radius=.13,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
if PASS>=3:
 # Front ring retains original size but now lies in the front-face plane.
 mount=bpy.data.objects['Side ring / mount'];mount.location=(-1.25,-1.46,.43);mount.rotation_euler=(math.pi/2,0,0)
 ring=bpy.data.objects['Side ring / hanging brass'];ring.location=(-1.25,-1.50,.30);ring.rotation_euler=(math.pi/2,0,0)
 # Shorten the released hasp around its unchanged bearing anchor, preserving contact.
 for ob in list(bpy.data.objects):
  if ob.parent==latch and ob.type=='MESH' and not any(k in ob.name for k in ['knuckle','bridge']):
   for ve in ob.data.vertices:ve.co.z*=.53
   ob.location.z*=.53
 for ob in list(bpy.data.objects):
  if ob.name.startswith('Corner brass'):
   for ve in ob.data.vertices:
    # Scalloped shoulder with retained wrap seating.
    axis=ve.co.x if 'front' in ob.name else ve.co.y
    if ve.co.z>0:ve.co.z*=.55+.45*math.cos(axis*10)**2
 # Small rounded studs are on the static clasp seat, clear of release path.
 for xx in [-.205,.205]:
  for zz in [1.24,1.47]:disk('Clasp / seated fastener',(xx,-1.502,zz),.022,.013)
if PASS>=3:
 bpy.data.objects['Latch / keeper'].location.z+=.27
 seat=bpy.data.objects['Rose stone / clasp seat'];seat.location.z+=.13;seat.scale.z=.65
 # Organic footprint: remove flat rectangular terrain perimeter, retaining lid-root contact.
 ob=bpy.data.objects['Atlas ridge / rear centre eroded massif'];me=ob.data
 vs=[tuple(v.co) for v in me.vertices];fs=[tuple(f.vertices) for f in me.polygons if max(me.vertices[i].co.z for i in f.vertices)>2.181]
 used=sorted(set(i for f in fs for i in f));remap={v:i for i,v in enumerate(used)}
 nm=bpy.data.meshes.new('Organic eroded footprint');nm.from_pydata([vs[i] for i in used],[],[tuple(remap[i] for i in f) for f in fs]);nm.materials.append(rock);nm.update();ob.data=nm;uv(ob)
 for f in nm.polygons:f.use_smooth=True
# Material batches retain individual disconnected ceramic prisms, reducing GLB node overhead.
if PASS>=2:
 for material in [green,ivory,dark]:
  items=[o for o in bpy.data.objects if o.name.startswith('Ceramic tessera') and o.data.materials[0]==material]
  for ob in items:
   select(ob)
   for modifier in list(ob.modifiers):bpy.ops.object.modifier_apply(modifier=modifier.name)
  bpy.ops.object.select_all(action='DESELECT')
  for ob in items:ob.select_set(True)
  bpy.context.view_layer.objects.active=items[0];count=len(items);bpy.ops.object.join();ob=bpy.context.object;ob['individual_tessera_count']=count
  for face in ob.data.polygons:face.use_smooth=True
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
bpy.ops.object.camera_add(location=(-5.6,-7.8,4.8));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.25))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'morocco.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'morocco.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('MOROCCO AUTHORED PASS',PASS)
