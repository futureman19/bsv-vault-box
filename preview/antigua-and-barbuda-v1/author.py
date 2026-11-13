"""Original coastal miniature; inherited family mechanism only."""
import bpy,math,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(281)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def maptex(m,file,slot,noncolor=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file),check_existing=True)
 if noncolor:t.image.colorspace_settings.name='Non-Color'
 t.image.pack();m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[slot])
stone=mat('Limestone / porous warm cream',(.65,.58,.43),.8);maptex(stone,'limestone-color.png','Base Color');maptex(stone,'limestone-roughness.png','Roughness',True)
sand=mat('Shell sand / pink',(.70,.32,.29),.86);maptex(sand,'shell-sand.png','Base Color')
gold=mat('Brass / satin',(.48,.30,.10),.28,.8)
water=mat('Lagoon / turquoise',(.015,.26,.28),.22,.10)
seam=mat('Mineral seam / dark teal',(.018,.065,.063),.85)
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Physical stone projection')
 for p in o.data.polygons:
  axis=max(range(3),key=lambda i:abs(p.normal[i]));axes=[i for i in range(3) if i!=axis]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;layer.data[li].uv=(co[axes[0]]*.7+.5,co[axes[1]]*.7+.5)
def cube(n,loc,dim,material,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o)
 if bevel:
  m=o.modifiers.new('Soft edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=2;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Limestone / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),stone,bevel=.022)
for sx in [-1,1]:cube('Limestone / side wall',(sx*1.745,0,.83),(.23,2.10,1.46),stone,bevel=.022)
cube('Limestone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Limestone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Limestone foot',(sx*1.47,sy*.91,-.08),(.51,.43,.33),stone,bevel=.09)
cube('Coast / lagoon',(0,0,1.995),(2.98,1.68,.045),water,lid,.014)
# Continuous irregular ribbon, not isolated sand dots. Solid triangle strip.
verts=[];faces=[];N=51
for i in range(N):
 t=i/(N-1);a=math.radians(65+265*t);radius=.65+.035*math.sin(t*19)
 for r,z in [(radius,2.025),(radius+.19,2.025),(radius,2.075),(radius+.19,2.075)]:verts.append((-.34+math.cos(a)*r*1.2,math.sin(a)*r*.85,z))
for i in range(N-1):
 k=i*4;n=k+4
 faces.extend([(k+2,n+2,n+3,k+3),(k,n,k+2),(n,n+2,k+2),(k+1,k+3,n+1),(n+1,k+3,n+3),(k,k+1,n+1,n)])
faces.extend([(0,2,3,1),tuple((N-1)*4+j for j in (0,1,3,2))])
me=bpy.data.meshes.new('Pink barrier shore');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Coast / pink barrier shore',me);bpy.context.collection.objects.link(o);me.materials.append(sand);uv(o);parent(o,lid)
# True arch opening: uprights and continuous arced crown with empty space below.
for x in [.35,1.15]:cube('Bridge / limestone abutment',(x,.43,2.13),(.25,.38,.28),stone,lid,.045)
verts=[];faces=[];N=25
for i in range(N):
 a=math.pi*i/(N-1)
 for y,r in [(.25,.40),(.61,.40),(.25,.54),(.61,.54)]:verts.append((.75+math.cos(a)*r,y,2.20+math.sin(a)*r*.65))
for i in range(N-1):
 k=i*4;n=k+4
 faces.extend([(k,n,n+1,k+1),(k+2,k+3,n+3,n+2),(k,k+2,n+2,n),(k+1,n+1,n+3,k+3)])
faces.extend([(0,1,3,2),tuple((N-1)*4+j for j in (0,2,3,1))])
me=bpy.data.meshes.new('Natural bridge crown');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Bridge / open limestone arch',me);bpy.context.collection.objects.link(o);me.materials.append(stone);uv(o);parent(o,lid)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for im in list(bpy.data.images):
 if im.users==0:bpy.data.images.remove(im)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.26
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=1000;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.use_nodes=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'antigua-and-barbuda.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'antigua-and-barbuda.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('AUTHOR PASS')
