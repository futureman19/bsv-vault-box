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

wood=mat('Timber / dark supporting frame',(.075,.035,.018),.6)
cloth=mat('Ngatu / invented ochre geometry',(.6,.4,.2),.85);maptex(cloth,'ngatu-color.png','Base Color');maptex(cloth,'ngatu-roughness.png','Roughness',True)
cream=mat('Ngatu / cream relief panel',(.60,.40,.21),.85);maptex(cream,'fiber-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
ink=mat('Dyed relief / dark brown',(.09,.025,.009),.9)
seam=mat('Seam / shadow',(.025,.015,.01),.9)
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
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
for sy in [-1,1]:
 cube('Ngatu / broad panel',(0,sy*1.145,.83),(3.72,.19,1.46),cloth,bevel=.012)
for sx in [-1,1]:
 cube('Ngatu / side panel',(sx*1.745,0,.83),(.23,2.48,1.46),cloth,axis='Y')
 for sy in [-1,1]:cube('Timber / corner',(sx*1.75,sy*1.15,.83),(.24,.24,1.47),wood)
for z in [.16,1.50]:
 for sy in [-1,1]:cube('Timber / long rail',(0,sy*1.24,z),(3.72,.055,.10),wood)
 for sx in [-1,1]:cube('Timber / short rail',(sx*1.87,0,z),(.055,2.48,.10),wood)
cube('Timber / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam)
for sx in [-1,1]:cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
cube('Lid / ngatu panel',(0,0,1.995),(3.10,1.75,.04),cream,lid,.012)
for sy in [-1,1]:cube('Lid / border long',(0,sy*.91,2.005),(3.25,.055,.055),ink,lid,.008)
for sx in [-1,1]:cube('Lid / border short',(sx*1.60,0,2.005),(.055,1.86,.055),ink,lid,.008)
# Six hollow diamonds: mesh bars retain a real open center.
for i,x in enumerate([-1.03,0,1.03]):
 for j,y in enumerate([-.43,.43]):
  outer=[(x,y-.27),(x+.33,y),(x,y+.27),(x-.33,y)];inner=[(x,y-.215),(x+.265,y),(x,y+.215),(x-.265,y)]
  vs=[(a,b,z) for z in [2.013,2.038] for ring in [outer,inner] for a,b in ring];fs=[]
  for k in range(4):
   n=(k+1)%4;fs += [(k,n,n+8,k+8),(k+4,k+12,n+12,n+4),(k+8,n+8,n+12,k+12),(k,k+4,n+4,n)]
  me=bpy.data.meshes.new('Diamond');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Lid / diamond '+str(i*2+j),me);bpy.context.collection.objects.link(o);me.materials.append(ink);parent(o)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Timber / foot',(sx*1.47,sy*.91,-.10),(.48,.42,.35),wood,bevel=.05)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=2;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'tonga.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'tonga.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('TONGA AUTHORED')
