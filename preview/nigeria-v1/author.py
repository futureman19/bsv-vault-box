"""Nigeria / Indigo & Resist. Script-authored Blender, independent patterns."""
import bpy, math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge']; latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw
 return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
indigo=mat('Indigo / independently authored resist cotton',(.008,.037,.147),.72)
p=indigo.node_tree.nodes.get('Principled BSDF')
for file,channel in [('indigo-color.png','Base Color'),('indigo-roughness.png','Roughness'),('indigo-normal.png','Normal')]:
 t=indigo.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file));t.image.pack()
 if channel!='Base Color':t.image.colorspace_settings.name='Non-Color'
 if channel=='Normal':
  normal=indigo.node_tree.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.35;indigo.node_tree.links.new(t.outputs['Color'],normal.inputs['Color']);indigo.node_tree.links.new(normal.outputs['Normal'],p.inputs[channel])
 else:indigo.node_tree.links.new(t.outputs['Color'],p.inputs[channel])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
lining=mat('Midnight / inner lining',(.012,.026,.057),.87)
seam=mat('Indigo / dark seam',(.006,.013,.030),.86)
solid=mat('Indigo / enamel relief',(.012,.055,.17),.29,.08)
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Physical weave')
 for f in o.data.polygons:
  for li in f.loop_indices:
   c=o.data.vertices[o.data.loops[li].vertex_index].co
   if abs(f.normal.z)>.7:u,v=c.x,c.y
   elif abs(f.normal.x)>.7:u,v=c.y,c.z
   else:u,v=c.x,c.z
   layer.data[li].uv=(u/2.0+.5,v/2.0+.5)
def cube(n,loc,dim,material,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o)
 if bevel:
  m=o.modifiers.new('Soft edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(lining if o.name.startswith('Interior') else gold)
# Solid continuous outer panels; inner shell remains the inherited hollow shell.
for sy in [-1,1]:cube('Indigo / front' if sy<0 else 'Indigo / rear',(0,sy*1.145,.83),(3.72,.19,1.46),indigo,bevel=.025)
for sx in [-1,1]:cube('Indigo / side',(sx*1.745,0,.83),(.23,2.10,1.46),indigo,bevel=.025)
cube('Indigo / clasp seat',(0,-1.255,1.36),(.56,.075,.47),solid,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:
  cube('Indigo / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),solid,bevel=.004)
  cube('Indigo / low foot',(sx*1.47,sy*.91,-.10),(.48,.42,.32),solid,bevel=.055)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),indigo,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def disk(n,loc,r,depth,material,p=None,rot=(0,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(material);m=o.modifiers.new('Rounded relief','BEVEL');m.width=min(.005,depth*.35);m.segments=3;select(o);bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
def torus(n,loc,r,minor,p=None,rot=(0,0,0)):
 bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=10,location=loc,major_radius=r,minor_radius=minor,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold)
 for f in o.data.polygons:f.use_smooth=True
 if p:parent(o,p)
 return o
for i,x in enumerate([-1.05,0,1.05]):
 disk('Resist / raised indigo disc '+str(i),(x,0,1.994),.32,.04,solid,lid)
 torus('Resist / brass ring '+str(i),(x,0,2.021),.29,.014,lid)
 # Small central pale brass point refers to tied seed, not an emblem.
 disk('Resist / seed point '+str(i),(x,0,2.024),.04,.018,gold,lid)
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035,gold,rot=(math.pi/2,0,0))
torus('Medallion / raised rim',(0,-1.282,.87),.107,.008,rot=(math.pi/2,0,0))
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,gold,rot=(0,math.pi/2,0))
torus('Side ring / hanging brass',(-1.91,0,.91),.125,.018,rot=(0,math.pi/2,0))
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.265
bpy.ops.object.camera_add(location=(-5.6,-7.8,4.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.05))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'nigeria.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'nigeria.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('NIGERIA_AUTHORED_PASS')
