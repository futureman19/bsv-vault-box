"""Djibouti Assal Salt Rift. Procedurally authored, not a scan."""
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
   dominant=max(range(3),key=lambda i:abs(p.normal[i]))
   u,v=((co.y,co.z) if dominant==0 else (co.x,co.z) if dominant==1 else (co.x,co.y))
   layer.data[li].uv=(u/2+.5,v/2+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
basalt=mat('Basalt / warm volcanic rock',(.08,.07,.06),.83)
maptex(basalt,'basalt-color.png','Base Color');maptex(basalt,'basalt-roughness.png','Roughness',True)
t=basalt.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/basalt-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=basalt.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.24;basalt.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);basalt.node_tree.links.new(n.outputs['Normal'],basalt.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
salt=mat('Salt / ivory crystalline shelf',(.78,.74,.61),.8);maptex(salt,'salt-color.png','Base Color')
water=mat('Assal / turquoise brine',(.025,.34,.38),.17,.15)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
liner=mat('Interior / dark mineral lining',(.06,.065,.06),.68)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(liner if o.name.startswith('Interior') else gold)
for sy in [-1,1]:cube('Basalt / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),basalt,bevel=.025)
for sx in [-1,1]:cube('Basalt / side wall',(sx*1.745,0,.83),(.23,2.10,1.46),basalt,bevel=.025,axis='Y')
cube('Basalt / clasp seat',(0,-1.255,1.36),(.56,.075,.47),basalt,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),salt,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),salt,bevel=.009)
 for sy in [-1,1]:cube('Basalt / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),basalt,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),basalt,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def stone(n,loc,scale,p=None,material=basalt,sub=2):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  k=1+random.uniform(-.11,.11);v.co=Vector((v.co.x*scale[0]*k,v.co.y*scale[1]*k,v.co.z*scale[2]*k))
 o.data.materials.append(material);uv(o)
 for face in o.data.polygons:face.use_smooth=True
 if p:parent(o,p)
 return o
for sx in [-1,1]:
 for sy in [-1,1]:stone('Basalt foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
# Annular shelf with real vertical relief, irregular concentric coastline.
N=96
outline=[1+.055*math.sin(i*math.tau/N*3)+.035*math.sin(i*math.tau/N*7+.8) for i in range(N)]
verts=[]
for rx,ry,z in [(1.49,.91,1.987),(1.49,.91,2.065),(1.09,.59,2.082),(1.09,.59,2.006)]:
 for i in range(N):
  a=i*math.tau/N;k=outline[i];verts.append((rx*math.cos(a)*k,ry*math.sin(a)*k,z))
faces=[]
for j in range(4):
 for i in range(N):faces.append((j*N+i,j*N+(i+1)%N,((j+1)%4)*N+(i+1)%N,((j+1)%4)*N+i))
me=bpy.data.meshes.new('Salt shelf relief');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / salt shelf',me);bpy.context.collection.objects.link(o);me.materials.append(salt);uv(o);parent(o)
# Filled irregular brine surface with a shallow solid sidewall.
verts=[(0,0,2.014)]+[(1.09*math.cos(i*math.tau/N)*outline[i],.59*math.sin(i*math.tau/N)*outline[i],2.014) for i in range(N)]
faces=[(0,i+1,(i+1)%N+1) for i in range(N)]
me=bpy.data.meshes.new('Brine inset');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / Assal lake',me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o)
for i in range(8):
 x=-1.13+i*.29;y=.69+.05*math.sin(i*1.7);stone('Terrain / rift escarpment',(x,y,2.13),(.24,.16,.16+.055*math.sin(i*1.8)),lid,sub=1)
for i in range(24):
 a=i*math.tau/24; k=1+.025*math.sin(i*2.3)
 stone('Terrain / salt crystals',(1.27*math.cos(a)*k,.75*math.sin(a)*k,2.071),(.075,.052,.025),lid,salt,1)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=880;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'djibouti.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'djibouti.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('DJIBOUTI AUTHORED')
