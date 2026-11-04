"""Brief-led Lithuania pilot. Authored mesh and maps; no photogrammetry.
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
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z
   if axis=='Y' and abs(p.normal.z)>.7:v=co.x
   layer.data[li].uv=(u/3.72+.5,v/1.7+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
sand=mat('Sand / wind ripple',(.65,.49,.28),.8);maptex(sand,'sand-color.png','Base Color');maptex(sand,'sand-roughness.png','Roughness',True)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Lagoon / dark seam',(.025,.07,.065),.7)
water=mat('Lagoon / teal ceramic',(.035,.24,.25),.24);maptex(water,'lagoon.png','Base Color')
green=mat('Dune / stabilization green',(.08,.15,.065),.9)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(sand if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Sand body / long',(0,sy*1.145,.83),(3.72,.19,1.46),sand,bevel=.025)
for sx in [-1,1]:cube('Sand body / end',(sx*1.745,0,.83),(.23,2.48,1.46),sand,bevel=.025)
cube('Sand / clasp seat',(0,-1.255,1.36),(.56,.075,.47),sand,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / end',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:
  cube('Sand / rim',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),sand,bevel=.004)
  cube('Sand / foot',(sx*1.47,sy*.91,-.08),(.55,.46,.32),sand,bevel=.05)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),sand,lid,.045)
cube('Lagoon / inset',(0,0,1.988),(3.16,1.8,.022),water,lid,.008)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# Closed curved dune volume. Sand ridges are geometry, not painted terrain.
verts=[];faces=[];nx=64;ny=16
for i in range(nx+1):
 x=-1.4+2.8*i/nx;u=i/nx;cy=.15*math.sin(u*math.pi*1.7);width=.24+.07*math.sin(math.pi*u)
 for j in range(ny+1):
  t=-1+2*j/ny;y=cy+t*width
  z=2.035+.40*max(0,math.sin(math.pi*u))**.65*max(0,1-abs(t)**1.4)*(.83+.17*math.sin(u*math.pi*3))
  verts.append((x,y,z))
for i in range(nx):
 for j in range(ny):
  a=i*(ny+1)+j;faces.append((a,a+ny+1,a+ny+2,a+1))
border=list(range(ny+1))+[i*(ny+1)+ny for i in range(1,nx+1)]+[nx*(ny+1)+j for j in range(ny-1,-1,-1)]+[i*(ny+1) for i in range(nx-1,0,-1)]
for k,a in enumerate(border):
 b=border[(k+1)%len(border)];v=len(verts);verts.extend([(verts[a][0],verts[a][1],1.995),(verts[b][0],verts[b][1],1.995)]);faces.append((a,v,v+1,b))
me=bpy.data.meshes.new('Curved dune volume');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Dune / continuous ridge',me);bpy.context.collection.objects.link(o);me.materials.append(sand);uv(o);parent(o)
for f in me.polygons:f.use_smooth=True
# Coherent shoulder planting: low irregular clusters rooted into sand.
for i in range(22):
 u=.13+.74*i/21;x=-1.4+2.8*u;cy=.15*math.sin(u*math.pi*1.7);t=.72;y=cy+t*(.24+.07*math.sin(math.pi*u));z=2.035+.40*math.sin(math.pi*u)**.65*(1-t**1.4)*(.83+.17*math.sin(u*math.pi*3))
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=(x,y,z));o=bpy.context.object;o.name='Vegetation / shoulder';o.scale=(.09,.065,.055);o.data.materials.append(green);parent(o)
# Clean obsolete unreferenced theme resources from source.
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
# Studio rendering is a real render of the exact exported mesh.
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'lithuania.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'lithuania.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('LITHUANIA AUTHORED')
