"""Reference-led Japan pilot. Authored mesh and maps; no photogrammetry.
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
chalk=mat('Chalk / warm pale mineral',(.72,.70,.65),.82)
maptex(chalk,'chalk-color.png','Base Color');maptex(chalk,'chalk-roughness.png','Roughness',True)
flint=mat('Flint / charcoal',(.045,.052,.057),.55);maptex(flint,'flint-color.png','Base Color')
granite=flint
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
green=mat('Plateau / beech canopy abstraction',(.10,.19,.055),.91)
water=mat('Baltic / turquoise inset',(.025,.30,.34),.19,.15)
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
  o.data.materials.clear();o.data.materials.append(chalk if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Chalk body / long',(0,sy*1.145,.83),(3.72,.19,1.46),chalk,bevel=.025)
for sx in [-1,1]:cube('Chalk body / end',(sx*1.745,0,.83),(.23,2.10,1.46),chalk,bevel=.025,axis='Y')
cube('Chalk / clasp seat',(0,-1.255,1.36),(.56,.075,.47),chalk,bevel=.025)
for sy in [-1,1]:cube('Flint seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),flint,bevel=.009)
for sx in [-1,1]:
 cube('Flint seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),flint,bevel=.009)
 for sy in [-1,1]:cube('Chalk / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),chalk,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),chalk,lid,.045)
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
 for sy in [-1,1]:stone('Flint foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
cube('Baltic / water inset',(0,0,1.992),(2.85,1.65,.026),water,lid,.009)
# Irregular contiguous escarpment with a genuinely raised green plateau.
for k in range(3):
 x0=-1.36+k*.90;n=12;verts=[]
 for j in range(n+1):
  x=x0+.90*j/n;y=.10+.085*math.sin((j+k*12)*1.7);z=2.35+.14*math.sin((j+k*12)*.43)+.035*math.sin(j*2.7)
  verts.extend([(x,y,2.006),(x,y,z),(x,.77,z-.035),(x,.77,2.006)])
 faces=[]
 for j in range(n):
  a=4*j;b=a+4
  faces.extend([(a,b,b+1,a+1),(a+1,b+1,b+2,a+2),(a+2,b+2,b+3,a+3),(a+3,b+3,b,a)])
 faces.extend([(3,2,1,0),(4*n,4*n+1,4*n+2,4*n+3)])
 me=bpy.data.meshes.new('Chalk cliff');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Landscape / chalk cliff '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(chalk);me.materials.append(green)
 for i,p in enumerate(me.polygons):
  if i<n*4 and i%4==1:p.material_index=1
 uv(o);parent(o)
for j in range(24):
 x=-1.30+j*.112;y=-.025+.022*math.sin(j*2)
 stone('Landscape / flint shore',(x,y,2.02),(.061,.045,.025),lid,flint,1)
# Clean obsolete unreferenced theme resources from source.
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
# Studio rendering is a real render of the exact exported mesh.
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,4.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.use_nodes=False;scene.render.resolution_x=960;scene.render.resolution_y=880;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'denmark.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'denmark.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('DENMARK AUTHORED')
