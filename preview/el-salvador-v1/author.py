"""Procedurally authored El Salvador landscape collectible; not a scale replica."""
import bpy,math,random
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
indigo=mat('Anil / indigo resist',(.025,.07,.16),.58);maptex(indigo,'indigo-color.png','Base Color');maptex(indigo,'indigo-roughness.png','Roughness',True)
stone=mat('Volcanic / charcoal granular',(.07,.08,.09),.72);maptex(stone,'volcanic.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / dark indigo',(.012,.025,.045),.8)
water=mat('Lagoon / mineral turquoise',(.025,.38,.32),.19,.15)
rim=mat('Crater / weathered ash',(.10,.12,.10),.88)
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Physical projection')
 for p in o.data.polygons:
  axes=(0,1) if abs(p.normal.z)>.7 else ((1,2) if abs(p.normal.x)>.7 else (0,2))
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co+o.location
   layer.data[li].uv=(co[axes[0]]/2.5+.5,co[axes[1]]/2.5+.5)
def cube(n,loc,dim,material,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o)
 if bevel:
  m=o.modifiers.new('Soft edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(indigo if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Indigo / front' if sy<0 else 'Indigo / rear',(0,sy*1.145,.83),(3.72,.19,1.46),indigo,bevel=.024)
for sx in [-1,1]:cube('Indigo / side',(sx*1.745,0,.83),(.23,2.10,1.46),indigo,bevel=.018)
cube('Indigo / clasp seat',(0,-1.255,1.36),(.56,.075,.47),indigo,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Indigo / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),indigo,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=(sx*1.47,sy*.91,-.10));o=bpy.context.object;o.name='Volcanic foot'
  for v in o.data.vertices:
   k=1+random.uniform(-.1,.1);v.co=Vector((v.co.x*.32*k,v.co.y*.27*k,v.co.z*.19*k))
  o.data.materials.append(stone);uv(o)
# Watertight crater: irregular concentric cross-sections, continuous inner walls.
N=80;verts=[];faces=[]
for j,(rx,ry,z) in enumerate([(1.30,.83,1.974),(1.05,.66,2.20),(.77,.51,2.55),(.56,.37,2.32),(.435,.29,2.07)]):
 for i in range(N):
  a=i*math.tau/N;k=1+.035*math.sin(5*a)+.025*math.cos(9*a)
  h=(.075*math.sin(3*a)+.045*math.sin(7*a)) if j in (1,2,3) else 0
  if j in (2,3):h-=.22*max(0,-math.sin(a))
  verts.append((rx*math.cos(a)*k,.12+ry*math.sin(a)*k,z+h))
for j in range(4):
 for i in range(N):
  a=j*N+i;b=j*N+(i+1)%N;faces.append((a,b,b+N,a+N))
faces.append(tuple(reversed(range(N))))
faces.append(tuple(4*N+i for i in range(N)))
me=bpy.data.meshes.new('Crater continuous shell');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / volcanic crater',me);bpy.context.collection.objects.link(o);me.materials.append(stone);me.materials.append(rim)
for poly in me.polygons:
 if N*2<=poly.index<N*3:poly.material_index=1
uv(o);parent(o)
# Flat lagoon nested inside inner crater, with enough visible area at hero angle.
verts=[(0,.12,2.105)]+[(.43*math.cos(i*math.tau/N),.12+.285*math.sin(i*math.tau/N),2.105) for i in range(N)]
faces=[(0,1+i,1+(i+1)%N) for i in range(N)]
me=bpy.data.meshes.new('Lagoon inset');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / turquoise lagoon',me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o)
def disk(n,loc,r,depth,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold);m=o.modifiers.new('Rounded brass','BEVEL');m.width=.005;m.segments=3;select(o);bpy.ops.object.modifier_apply(modifier=m.name)
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035)
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,7.3));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=1000;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.use_nodes=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'el-salvador.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'el-salvador.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('EL SALVADOR AUTHORED')
