"""Brief-led Panama pilot. Authored mesh and maps; no photogrammetry.
Run maps.py first. Reproduction uses only the included trimmed mechanism.blend.
"""
import bpy,bmesh,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(521)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p=lid):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def maptex(m,file,input,noncolor=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file),check_existing=True)
 if noncolor:t.image.colorspace_settings.name='Non-Color'
 t.image.pack();m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[input])
wood=mat('Jade / mottled mineral',(.4,.18,.08),.4);maptex(wood,'jade-color.png','Base Color');maptex(wood,'jade-roughness.png','Roughness',True)
end=mat('Sediment / dark matrix',(.21,.075,.028),.47);maptex(end,'sediment.png','Base Color')
# Actual end-grain differs in UV frequency and tint via a separate compact map.
granite=mat('Granite / salt and pepper',(.24,.25,.25),.85);maptex(granite,'granite.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
bark=mat('Mangrove / brown bark',(.19,.075,.031),.85)
moss=mat('Moss / muted cushions',(.095,.16,.035),.95)
seam=mat('Mineral seam / moss green',(.035,.07,.032),.9)
leafm=[mat('Mangrove canopy / '+str(i),c,.92) for i,c in enumerate([(.045,.10,.024),(.07,.14,.035),(.10,.18,.047),(.13,.21,.06)])]
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Physical mineral projection')
 for p in o.data.polygons:
  n=p.normal;major=max(range(3),key=lambda k:abs(n[k]));axes=[k for k in range(3) if k!=major]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co+o.location
   layer.data[li].uv=(co[axes[0]]*.6,co[axes[1]]*.6)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o,'Y' if 'end' in o.name else 'X')
# Continuous mineral skins around the inherited hollow liner.
for sy in [-1,1]:cube('Jade / front' if sy<0 else 'Jade / rear',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.025)
for sx in [-1,1]:cube('Jade / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.025)
# Small collar fills the central clasp mounting behind its retained position.
cube('Jade / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:
 cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Jade / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
# Restrained brass corner protectors replace the Iceland wraps entirely.
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def stone(n,loc,scale,p=None,material=granite,sub=2):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  k=1+random.uniform(-.11,.11);v.co=Vector((v.co.x*scale[0]*k,v.co.y*scale[1]*k,v.co.z*scale[2]*k))
 o.data.materials.append(material);uv(o)
 for face in o.data.polygons:face.use_smooth=True
 if p:parent(o,p)
 return o
for sx in [-1,1]:
 for sy in [-1,1]:stone('Granite foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)
def tube(n,points,radii,material,p=lid,sides=9):
 verts=[];faces=[]
 for i,c in enumerate(points):
  c=Vector(c);t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);t.normalize();a=t.cross(Vector((0,1,0)))
  if a.length<.01:a=t.cross(Vector((1,0,0)))
  a.normalize();b=t.cross(a).normalized()
  for j in range(sides):verts.append(c+radii[i]*(a*math.cos(j*math.tau/sides)+b*math.sin(j*math.tau/sides)))
 for i in range(len(points)-1):
  for j in range(sides):a=i*sides+j;bb=i*sides+(j+1)%sides;faces.append((a,bb,bb+sides,a+sides))
 faces.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))]);me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material)
 for f in me.polygons:f.use_smooth=True
 if p:parent(o,p)
 return o
# A continuous sinuous tidal inlet and two contiguous sediment banks.
water=mat('Tidal water / turquoise',(.025,.24,.23),.18,.12)
sand=mat('Sediment / warm silt',(.23,.18,.105),.86);maptex(sand,'sediment.png','Base Color')
def ribbon(n,side,material):
 verts=[];faces=[];N=40
 for i in range(N+1):
  x=-1.40+2.8*i/N;c=.22*math.sin(2.2*x)
  ys=(c-.14,c+.14) if side==0 else ((c+.14,.85) if side==1 else (-.85,c-.14))
  z=2.018 if side==0 else 2.042
  for y in ys:verts.append((x,y,z))
 for i in range(N):faces.append((2*i,2*i+2,2*i+3,2*i+1))
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o)
 return o
ribbon('Tide / continuous inlet',0,water)
ribbon('Bank / north',1,sand);ribbon('Bank / south',-1,sand)
# Three spreading stilt-root mangroves; leaf diamonds batched by palette.
vs=[[] for _ in leafm];fs=[[] for _ in leafm]
for ti,(x,y) in enumerate([(-.85,.57),(.10,-.55),(.95,.55)]):
 trunk=[(x,y,2.045),(x+.025,y,2.25),(x-.025,y+.015,2.49),(x+.015,y,2.67)]
 tube('Mangrove / trunk '+str(ti),trunk,[.046,.043,.029,.008],bark)
 for j in range(5):
  a=j*math.tau/5;rx=x+math.cos(a)*.18;ry=y+math.sin(a)*.15
  tube('Mangrove / stilt root '+str(ti)+' '+str(j),[(rx,ry,2.042),(x+math.cos(a)*.11,y+math.sin(a)*.09,2.18),trunk[1]],[.013,.018,.022],bark,sides=7)
 for j in range(10):
  az=j*2.399;rad=.23+random.random()*.12;start=Vector((x,y,2.40+j*.019));tip=start+Vector((math.cos(az)*rad,math.sin(az)*rad,.11))
  tube('Mangrove / branch',[start,start.lerp(tip,.5)+Vector((0,0,.05)),tip],[.014,.009,.002],bark,sides=7)
  for k in range(24):
   a=random.uniform(0,math.tau);r=random.random()**.5*.17;q=tip+Vector((math.cos(a)*r,math.sin(a)*r,random.uniform(-.04,.045)))
   ang=random.uniform(0,math.tau);d=Vector((math.cos(ang),math.sin(ang),.12));w=Vector((-math.sin(ang),math.cos(ang),0))*.033
   length=.085+random.random()*.035;mi=random.randrange(4);n=len(vs[mi]);mid=q+d*length*.5
   vs[mi].extend([q,mid+w,q+d*length,mid-w,mid+Vector((0,0,.008))]);fs[mi].extend([(n,n+1,n+4),(n+1,n+2,n+4),(n+2,n+3,n+4),(n+3,n,n+4)])
for i in range(4):
 me=bpy.data.meshes.new('Broadleaf canopy');me.from_pydata(vs[i],[],fs[i]);me.update();o=bpy.data.objects.new('Mangrove / foliage '+str(i),me);bpy.context.collection.objects.link(o);me.materials.append(leafm[i]);parent(o)
 for f in me.polygons:f.use_smooth=True
# Medallion is solid, never an unexplained front opening.
def disk(n,loc,r,depth,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold);m=o.modifiers.new('Rounded brass','BEVEL');m.width=.005;m.segments=3;select(o);bpy.ops.object.modifier_apply(modifier=m.name);return o
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035)
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(0,-1.282,.87),major_radius=.107,minor_radius=.008,rotation=(math.pi/2,0,0));bpy.context.object.name='Medallion / raised rim';bpy.context.object.data.materials.append(gold)
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
# Clean obsolete unreferenced theme resources from source.
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
# Studio rendering is a real render of the exact exported mesh.
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,4.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'panama.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'panama.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('PANAMA AUTHORED')
