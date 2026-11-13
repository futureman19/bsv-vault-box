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
ocean=mat('Ocean enamel / abyssal blue',(.025,.12,.18),.3,.15);maptex(ocean,'ocean-color.png','Base Color');maptex(ocean,'ocean-roughness.png','Roughness',True)
granite=mat('Basalt / volcanic substrate',(.035,.045,.052),.85);maptex(granite,'basalt.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
sand=mat('Coral sand / pale limestone',(.72,.63,.43),.82)
water=mat('Lagoon / turquoise enamel',(.015,.44,.47),.19,.12)
seam=mat('Deep teal / gasket',(.015,.06,.065),.8)
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Planar ocean mapping')
 for p in o.data.polygons:
  ax=max(range(3),key=lambda k:abs(p.normal[k]));axes=[k for k in range(3) if k!=ax]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]/2+.5,co[axes[1]]/2+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(ocean if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Ocean / front' if sy<0 else 'Ocean / rear',(0,sy*1.145,.83),(3.72,.19,1.46),ocean,bevel=.025)
for sx in [-1,1]:cube('Ocean / side',(sx*1.745,0,.83),(.23,2.10,1.46),ocean,bevel=.025)
cube('Ocean / clasp seat',(0,-1.255,1.36),(.56,.075,.47),ocean,bevel=.025)
for sy in [-1,1]:cube('Deep seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Deep seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Ocean / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),ocean,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),ocean,lid,.045)
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
# Continuous annular mesh: a real aperture, not a painted circle.
N=96;verts=[];faces=[]
for band in range(4):
 for i in range(N):
  t=i*math.tau/N;w=1+.045*math.sin(5*t)+.028*math.cos(9*t)
  rx,ry=[(.91,.68),(.86,.63),(.66,.45),(.64,.43)][band]
  z=[1.98,2.10+.025*math.sin(3*t),2.09+.02*math.cos(4*t),1.98][band]
  verts.append((-.30+rx*w*math.cos(t),ry*w*math.sin(t),z))
for band in range(3):
 for i in range(N):
  j=(i+1)%N;faces.append((band*N+i,band*N+j,(band+1)*N+j,(band+1)*N+i))
for i in range(N):
 j=(i+1)%N;faces.append((i,3*N+i,3*N+j,j))
me=bpy.data.meshes.new('Atoll annulus');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Atoll / coral sand ring',me);bpy.context.collection.objects.link(o);me.materials.append(sand);parent(o)
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=1,depth=.025,location=(-.30,0,2.0025));o=bpy.context.object;o.name='Atoll / lagoon';o.scale=(.57,.37,1);select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(water);parent(o)
# Irregular crater cone is separate from the atoll, intentionally not a map.
v=[];f=[];N=48
for band in range(3):
 for i in range(N):
  t=i*math.tau/N;k=1+.08*math.sin(t*7)
  rx,ry,z=[(.31,.24,1.98),(.12,.10,2.38),(.065,.05,2.29)][band]
  v.append((1.05+rx*k*math.cos(t),.47+ry*k*math.sin(t),z+(.025*math.sin(5*t) if band else 0)))
for band in range(2):
 for i in range(N):j=(i+1)%N;f.append((band*N+i,band*N+j,(band+1)*N+j,(band+1)*N+i))
f.append(tuple(range(2*N,3*N)));f.append(tuple(reversed(range(N))))
me=bpy.data.meshes.new('Crater mesh');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new('Seamount / basalt crater',me);bpy.context.collection.objects.link(o);me.materials.append(granite);uv(o);parent(o)
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
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'pacific-ocean.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'pacific-ocean.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('PACIFIC AUTHORED')
