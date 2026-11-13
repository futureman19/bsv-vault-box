"""Brief-driven Madagascar limestone-forest pilot. Authored mesh and maps; no photogrammetry.
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

limestone=mat('Limestone / weathered chalk',(.4,.42,.36),.78);maptex(limestone,'limestone-color.png','Base Color');maptex(limestone,'limestone-roughness.png','Roughness',True)
granite=mat('Limestone / dark cleft',(.16,.19,.16),.88);maptex(granite,'cleft-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
moss=mat('Forest / sheltered green',(.065,.105,.037),.96)
seam=mat('Mineral seam / shaded green',(.035,.055,.032),.9)
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

for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(granite if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Continuous dark shell with individual fluted limestone outer ribs.
for sy in [-1,1]:
 cube('Limestone / continuous wall',(0,sy*1.135,.83),(3.72,.17,1.46),granite,bevel=.015)
 for i in range(23):
  x=-1.76+i*3.52/22;z=.83+random.uniform(-.025,.025)
  cube('Limestone / vertical flute',(x,sy*1.198,z),(.13+random.random()*.025,.09,1.40+random.uniform(-.05,.05)),limestone,bevel=.025)
for sx in [-1,1]:
 cube('Limestone / side shell',(sx*1.745,0,.83),(.23,2.10,1.46),granite,bevel=.012)
 for i in range(13):
  y=-.99+i*1.98/12
  cube('Limestone / side flute',(sx*1.84,y,.83),(.075,.13+random.random()*.025,1.43+random.uniform(-.04,.04)),limestone,bevel=.025)
cube('Limestone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),limestone,bevel=.025)
for sy in [-1,1]:
 cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Limestone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),limestone,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),limestone,lid,.045)
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
 for sy in [-1,1]:stone('Limestone foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
# Closed irregular tapered prisms, not cone primitives; two skewed shoulder rings.
def pinnacle(n,x,y,h,rx,ry):
 sides=7;verts=[]
 for z,f,ox,oy in [(1.965,1,0,0),(1.98+h*.42,.77,.018,-.012),(1.98+h*.81,.32,-.021,.013)]:
  for j in range(sides):
   a=j*math.tau/sides;r=1+random.uniform(-.2,.2);verts.append((x+ox+math.cos(a)*rx*f*r,y+oy+math.sin(a)*ry*f*r,z+random.uniform(-.012,.012)))
 verts.append((x+rx*.18,y-ry*.17,1.98+h));faces=[tuple(reversed(range(sides)))]
 for k in range(2):
  for j in range(sides):a=k*sides+j;b=k*sides+(j+1)%sides;faces.append((a,b,b+sides,a+sides))
 for j in range(sides):faces.append((14+j,14+(j+1)%sides,21))
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(limestone);uv(o);parent(o)
for row in range(4):
 for col in range(7):
  x=-1.34+col*.43+random.uniform(-.055,.055);y=-.68+row*.43+random.uniform(-.05,.05)
  h=.18+.33*(row/3)+.13*(col/6)+random.uniform(-.015,.015)
  pinnacle('Tsingy / pinnacle %02d'%(row*7+col),x,y,h,.14+random.random()*.045,.11+random.random()*.025)
for i in range(18):
 x=-1.25+(i%6)*.49;y=-.45+(i//6)*.43
 stone('Forest / gully patch %02d'%i,(x,y,1.99),(.18,.08,.025),lid,moss,2)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'madagascar.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'madagascar.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('MADAGASCAR AUTHORED')
