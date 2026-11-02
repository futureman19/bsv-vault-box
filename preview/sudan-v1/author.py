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
sand=mat('Sandstone / ochre porous',(.57,.31,.10),.84)
maptex(sand,'sand-color.png','Base Color');maptex(sand,'sand-roughness.png','Roughness',True)
node=sand.node_tree.nodes.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(R/'maps/sand-normal.png'));node.image.colorspace_settings.name='Non-Color';node.image.pack()
normal=sand.node_tree.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.25;sand.node_tree.links.new(node.outputs['Color'],normal.inputs['Color']);sand.node_tree.links.new(normal.outputs['Normal'],sand.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
interior=mat('Interior / warm dark earth',(.13,.065,.025),.9)
seam=mat('Mineral seam / dark umber',(.045,.022,.01),.95)
granite=sand
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
  o.data.materials.clear();o.data.materials.append(interior if o.name.startswith('Interior') else gold)
# Solid exterior masonry courses with restrained joints; no inherited finger joints.
for i in range(6):
 z=.10+(i+.5)*1.46/6;h=1.46/6-.006
 for sy in [-1,1]:cube('Sandstone / long course '+str(i),(0,sy*1.145,z),(3.72,.19,h),sand,bevel=.006)
 for sx in [-1,1]:cube('Sandstone / side course '+str(i),(sx*1.745,0,z),(.23,2.10,h),sand,bevel=.006,axis='Y')
cube('Sandstone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),sand,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Sandstone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),sand,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),sand,lid,.045)
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
 for sy in [-1,1]:stone('Sandstone foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
# Shallow uneven sand field: elliptical rings avoid a rectangular plinth silhouette.
verts=[(0,0,2.095)];faces=[];N=80;K=10
for k in range(1,K+1):
 r=k/K
 for j in range(N):
  a=j*math.tau/N;x=1.64*r*math.cos(a);y=.96*r*math.sin(a)
  z=1.978+(1-r*r)*(.10+.035*math.sin(4*x+2*y)+.02*math.cos(7*y-x))
  verts.append((x,y,z))
for j in range(N):faces.append((0,1+j,1+(j+1)%N))
for k in range(K-1):
 for j in range(N):
  a=1+k*N+j;b=1+k*N+(j+1)%N;faces.append((a,a+N,b+N,b))
me=bpy.data.meshes.new('Dune terrain');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / ochre dunes',me);bpy.context.collection.objects.link(o);me.materials.append(sand);uv(o);parent(o)
for f in me.polygons:f.use_smooth=True
# Each monument is one editable closed mesh, with shallow stepped masonry courses.
for index,(x,y,w,h) in enumerate([(-1.02,-.22,.56,.55),(-.12,.32,.76,1.05),(.94,-.10,.65,.80)]):
 vs=[];fs=[];courses=12;z=2.065
 for k in range(courses):
  zz=z+h*k/courses;zt=z+h*(k+1)/courses
  bottom=w*(1-k/courses)/2;top=max(.003,w*(1-(k+1)/courses)/2-.003)
  base=len(vs)
  for height,radius in [(zz,bottom),(zt,top)]:
   vs.extend([(x-radius,y-radius,height),(x+radius,y-radius,height),(x+radius,y+radius,height),(x-radius,y+radius,height)])
  fs.extend([(base,base+3,base+2,base+1),(base+4,base+5,base+6,base+7)])
  for j in range(4):fs.append((base+j,base+(j+1)%4,base+4+(j+1)%4,base+4+j))
 me=bpy.data.meshes.new('Pyramid masonry');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Pyramid / '+str(index+1),me);bpy.context.collection.objects.link(o);me.materials.append(sand);uv(o);parent(o)
 o['height_contract']=h;o['width_contract']=w;o['courses']=courses
 # Small eastern-style chapel volume is intentionally omitted: not a replica.
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
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'sudan.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'sudan.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('SUDAN AUTHORED')
