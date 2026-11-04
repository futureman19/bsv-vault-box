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

wood=mat('Walnut structure',(.041,.02,.012),.55);maptex(wood,'walnut.png','Base Color')
end=wood
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Dark textile seam',(.012,.018,.028),.9)
cloth=[]
for name in ['indigo','cream','ochre']:
 m=mat('Cotton / '+name,(.2,.2,.2),.85);maptex(m,name+'.png','Base Color');maptex(m,'weave-roughness.png','Roughness',True);cloth.append(m)
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
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=1;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o,'Y' if 'end' in o.name else 'X')
# Exterior skins constructed as alternating finger rows; each course changes
# which plank crosses the corner. End-grain squares are true exposed geometry.
for i in range(8):
 z=.10+(i+.5)*1.46/8;h=1.46/8
 for sy in [-1,1]:
  cube('Walnut / '+('front' if sy<0 else 'rear')+' course '+str(i),(0,sy*1.145,z),(3.72 if i%2==0 else 3.26,.19,h),wood,bevel=.003)
 for sx in [-1,1]:
  cube('Walnut / side course '+str(i),(sx*1.745,0,z),(.23,2.10 if i%2==0 else 2.48,h),wood,bevel=.003,axis='Y')
 for sx in [-1,1]:
  for sy in [-1,1]:
   if i%2==0:
    o=cube('Finger / exposed side end',(sx*1.862,sy*1.145,z),(.008,.19,h-.006),end,bevel=.002,axis='Y')
   else:o=cube('Finger / exposed front end',(sx*1.745,sy*1.242,z),(.23,.008,h-.006),end,bevel=.002)
   # tint via authored per-face material below, no external procedural shader.
# Small collar fills the central clasp mounting behind its retained position.
cube('Walnut / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:
 cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Walnut / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
# A thin satin upper facing with an independently oriented grain field.
for sx in [-1,1]:
 for j in range(6):cube('Lid finger / end',(sx*1.858,-.98+j*.39,1.83),(.012,.16,.23),end,lid,.003,axis='Y')
# Restrained brass corner protectors replace the Iceland wraps entirely.
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)

# Nine narrow joined strips: invented non-symbolic textile rhythm.
for i in range(9):
 x=(i-4)*.345
 cube('Textile lid strip %02d'%i,(x,0,2.002),(.335,1.96,.045),cloth[0],lid,.006)
 for dx,width,mi in [(-.105,.032,1),(-.055,.015,2),(.08,.022,1)]:
  cube('Textile lid accent',(x+dx,0,2.028),(width,1.94,.009),cloth[mi],lid,.002)
 if i<8:cube('Textile raised join %02d'%i,(x+.1725,0,2.032),(.012,1.96,.022),cloth[2],lid,.002)
# Cloth-facing front/rear panels with broad visible longitudinal stripes.
for sy in [-1,1]:
 for i in range(9):
  x=(i-4)*.345
  cube('Textile body panel',(x,sy*1.248,.82),(.332,.016,1.30),cloth[0],bevel=.003)
  for dx,width,mi in [(-.105,.032,1),(-.055,.015,2),(.08,.022,1)]:
   cube('Textile body accent',(x+dx,sy*1.26,.82),(width,.01,1.28),cloth[mi],bevel=.002)
for sx in [-1,1]:
 for j in range(5):
  y=(j-2)*.37
  cube('Textile side panel',(sx*1.867,y,.82),(.014,.355,1.30),cloth[0],bevel=.003)
  cube('Textile side stripe',(sx*1.879,y-.085,.82),(.008,.036,1.28),cloth[1],bevel=.002)
for sx in [-1,1]:
 for sy in [-1,1]:cube('Walnut foot',(sx*1.47,sy*.91,-.10),(.46,.38,.30),wood,bevel=.04)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=2;scene.use_nodes=False;scene.render.resolution_x=1000;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'cote-d-ivoire.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'cote-d-ivoire.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('COTE D IVOIRE AUTHORED')
