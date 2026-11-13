"""Original Earthen Courtyard; inherited mechanics, authored geometry/maps."""
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
earth=mat('Earth / fine plaster',(.40,.112,.04),.82);maptex(earth,'earth-color.png','Base Color');maptex(earth,'earth-roughness.png','Roughness',True)
t=earth.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/earth-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=earth.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.22;earth.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);earth.node_tree.links.new(n.outputs['Normal'],earth.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
cream=mat('Pigment / cream',(.79,.63,.35),.8)
charcoal=mat('Pigment / charcoal',(.03,.02,.015),.9)
ochre=mat('Earth / ochre roof',(.59,.30,.11),.85)
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
  o.data.materials.clear();o.data.materials.append(earth if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Continuous earthen skins, not inherited cedar courses.
for sy in [-1,1]:cube('Earth / front' if sy<0 else 'Earth / rear',(0,sy*1.145,.83),(3.72,.19,1.46),earth,bevel=.045)
for sx in [-1,1]:cube('Earth / side',(sx*1.745,0,.83),(.23,2.10,1.46),earth,bevel=.045)
cube('Earth / clasp seat',(0,-1.255,1.36),(.56,.075,.47),earth,bevel=.025)
# Invented framing lines: no named traditional or sacred motif.
for z in [.32,.43,1.24]:
 for sy in [-1,1]:cube('Border / horizontal cream',(0,sy*1.244,z),(3.47,.012,.025),cream,bevel=.003)
 for sx in [-1,1]:cube('Border / side cream',(sx*1.865,0,z),(.012,2.08,.025),cream,bevel=.003)
for sy in [-1,1]:
 for sx in [-1,1]:
  for x in [sx*.6,sx*1.13,sx*1.55]:
   cube('Border / charcoal panel',(x,sy*1.246,.84),(.033,.014,.61),charcoal,bevel=.003)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),charcoal,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),charcoal,bevel=.009)
 for sy in [-1,1]:cube('Earth / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),earth,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),earth,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Earth / foot',(sx*1.47,sy*.91,-.10),(.55,.46,.37),ochre,bevel=.09)
# Low abstract architectural volumes; not a scale model of the Royal Court.
for i,(x,y,w,d,h) in enumerate([(-.95,.27,.65,.74,.43),(.05,.46,.72,.58,.53),(.92,.20,.63,.78,.33)]):
 cube('Courtyard / volume '+str(i),(x,y,1.977+h/2),(w,d,h),earth,lid,.10)
 cube('Courtyard / roof '+str(i),(x,y,1.977+h-.015),(w+.04,d+.04,.055),ochre,lid,.018)
 cube('Courtyard / doorway '+str(i),(x,y-d/2-.006,2.057),(.13,.014,.16),charcoal,lid,.028)
 for z in [2.16,2.21]:
  if z<1.977+h-.04:cube('Courtyard / framing '+str(i),(x,y-d/2-.009,z),(w-.16,.014,.018),cream,lid,.003)
# Connected U-enclosure with a deliberate open front entrance.
for x in [-1.4,1.4]:cube('Courtyard / enclosure side',(x,-.03,2.075),(.10,1.58,.196),earth,lid,.03)
cube('Courtyard / enclosure rear',(0,.72,2.075),(2.8,.10,.196),earth,lid,.03)
for x in [-.91,.91]:cube('Courtyard / entrance wing',(x,-.77,2.075),(.98,.10,.196),earth,lid,.03)
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
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'burkina-faso.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'burkina-faso.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('PASS BURKINA FASO AUTHORED')
