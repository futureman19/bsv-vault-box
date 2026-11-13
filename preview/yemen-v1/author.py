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
earth=mat('Ochre fired earth',(.48,.22,.10),.8);maptex(earth,'earth.png','Base Color');maptex(earth,'roughness.png','Roughness',True)
gypsum=mat('Ivory gypsum',(.88,.82,.66),.82)
stone=mat('Stone foundation',(.20,.17,.14),.9);maptex(stone,'stone.png','Base Color')
gold=mat('Satin brass',(.48,.30,.10),.28,.8)
seam=mat('Warm dark seam',(.065,.035,.025),.9)
window=mat('Recess shadow',(.035,.025,.02),.95)
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   normal=p.normal
   if abs(normal.z)>.7:u,v=co.x,co.y
   elif abs(normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u*.7+.5,v*.7+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(earth if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Earth / facade',(0,sy*1.145,.83),(3.26,.19,1.46),earth)
for sx in [-1,1]:cube('Earth / side',(sx*1.745,0,.83),(.23,2.48,1.46),earth)
cube('Earth / clasp seat',(0,-1.255,1.36),(.56,.075,.47),earth,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:
  cube('Earth / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),earth,bevel=.004)
  cube('Stone foot',(sx*1.47,sy*.91,-.10),(.54,.48,.36),stone,bevel=.06)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),earth,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
for z in [.33,.41,1.03]:
 for sy in [-1,1]:cube('Gypsum / facade band',(0,sy*1.247,z),(3.70,.024,.035),gypsum,bevel=.004)
 for sx in [-1,1]:cube('Gypsum / side band',(sx*1.87,0,z),(.024,2.45,.035),gypsum,bevel=.004)
for x in [-1.45,-1.05,-.65,.65,1.05,1.45]:
 for sign in [-1,1]:
  o=cube('Gypsum / diamond',(x+sign*.065,-1.252,.68),(.018,.024,.20),gypsum,bevel=.003);o.rotation_euler.y=sign*.75
  o=cube('Gypsum / diamond',(x+sign*.065,-1.252,.82),(.018,.024,.20),gypsum,bevel=.003);o.rotation_euler.y=-sign*.75
for sx in [-1,1]:
 for y in [-.8,-.4,.4,.8]:
  for sign in [-1,1]:
   o=cube('Gypsum / side diamond',(sx*1.88,y+sign*.065,.68),(.024,.018,.20),gypsum,bevel=.003);o.rotation_euler.x=sign*.75
   o=cube('Gypsum / side diamond',(sx*1.88,y+sign*.065,.82),(.024,.018,.20),gypsum,bevel=.003);o.rotation_euler.x=-sign*.75
for i,(x,h) in enumerate([(-.80,.65),(0,.92),(.80,.75)]):
 y=.30;w=.52
 cube('Tower / house '+str(i),(x,y,1.978+h/2),(w,.50,h),earth,lid,.018)
 for z in [2.01,2.18,2.40,1.978+h-.025]:
  if z<1.978+h:
   cube('Tower / gypsum course',(x,y,z),(w+.018,.518,.024),gypsum,lid,.004)
 for z in [2.25,2.52]:
  if z+.10<1.978+h:
   for dx in [-.13,.13]:
    cube('Tower / window surround',(x+dx,y-.257,z),(.135,.025,.17),gypsum,lid,.018)
    cube('Tower / dark window',(x+dx,y-.273,z),(.085,.012,.12),window,lid,.012)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'yemen.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'yemen.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('YEMEN AUTHORED')
