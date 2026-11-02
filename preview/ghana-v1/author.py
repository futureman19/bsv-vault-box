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
wood=mat('Cocoa wood / satin',(.16,.07,.035),.5);maptex(wood,'wood-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
textile=mat('Kente inspired / original strip geometry',(.65,.30,.05),.73);maptex(textile,'kente-color.png','Base Color');maptex(textile,'kente-roughness.png','Roughness',True)
seam=mat('Dark seam',(.018,.014,.01),.9)
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
  if o.name.startswith('Interior'):uv(o,'Y' if 'end' in o.name else 'X')

# Dark frame with broad original textile-inspired rigid inlays.
for sy in [-1,1]:
 cube('Cocoa / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.018)
 for i in range(8):
  o=cube('Kente / body strip',( -1.54+i*.44,sy*1.246,.83),(.42,.015,1.16),textile,bevel=.003)
  for poly in o.data.polygons:
   for li in poly.loop_indices:
    co=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers.active.data[li].uv=(co.x/.42+.5,co.z/1.16+.5)
for sx in [-1,1]:
 cube('Cocoa / side wall',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.018)
 for i in range(5):
  o=cube('Kente / side strip',(sx*1.867,-.80+i*.4,.83),(.014,.38,1.16),textile,bevel=.003)
  for poly in o.data.polygons:
   for li in poly.loop_indices:
    co=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers.active.data[li].uv=(co.y/.38+.5,co.z/1.16+.5)
cube('Cocoa / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Dark seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.12 if sy<0 else .07,.08),seam,bevel=.008)
for sx in [-1,1]:cube('Dark seam / side',(sx*1.74,0,1.618),(.12,2.05,.08),seam,bevel=.008)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
for i in range(8):
 o=cube('Kente / lid strip '+str(i),(-1.54+i*.44,0,1.987),(.42,1.97,.018),textile,lid,.003)
 for poly in o.data.polygons:
  for li in poly.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers.active.data[li].uv=(co.x/.42+.5,co.y/1.97+.5)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Cocoa / foot',(sx*1.48,sy*.90,-.065),(.40,.36,.30),wood,bevel=.045)
  cube('Brass / foot ferrule',(sx*1.48,sy*.90,-.14),(.412,.372,.08),gold,bevel=.015)
# A modest original stepped diamond, not an attributed traditional symbol.
for j,w in enumerate([.60,.40,.20]):
 o=cube('Ornament / stepped diamond '+str(j),(0,0,2.012+j*.026),(w,w,.024),gold,lid,.006)
 o.rotation_euler.z=math.pi/4
for sy in [-1,1]:cube('Lid / brass border',(0,sy*1.035,1.989),(3.20,.025,.018),gold,lid,.005)
# Clean obsolete unreferenced theme resources from source.
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
# Studio rendering is a real render of the exact exported mesh.
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.215
bpy.ops.object.camera_add(location=(-5.6,-7.8,4.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'ghana.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'ghana.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('GHANA AUTHORED')
