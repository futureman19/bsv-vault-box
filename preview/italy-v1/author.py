"""Italy: original procedural stone/inlay design over inherited articulation."""
import bpy,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge']
def parent(o):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=lid;o.matrix_world=mw;return o
def mat(name,color,rough=.4,metal=0,texture=None):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
 if texture:
  for file,socket in [(texture+'.png','Base Color'),('roughness.png','Roughness')]:
   t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file),check_existing=True)
   if socket=='Roughness':t.image.colorspace_settings.name='Non-Color'
   t.image.pack();m.node_tree.links.new(t.outputs['Color'],p.inputs[socket])
 return m
ivory=mat('Ivory / veined stone',(.73,.69,.60),texture='ivory');green=mat('Green / polished stone',(.03,.07,.04),texture='green');red=mat('Terracotta / colored stone',(.40,.12,.06),texture='terracotta');gold=mat('Brass / satin',(.48,.30,.10),.28,.8);seam=mat('Mineral seam',(.025,.045,.03),.8)
def uv(o):
 u=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone projection')
 for f in o.data.polygons:
  a=max(range(3),key=lambda i:abs(f.normal[i]));axes=[i for i in range(3) if i!=a]
  for li in f.loop_indices:
   c=o.data.vertices[o.data.loops[li].vertex_index].co;u.data[li].uv=(c[axes[0]]/2+.5,c[axes[1]]/2+.5)
def cube(n,loc,dim,m,moving=False,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if bevel:
  b=o.modifiers.new('Stone edge','BEVEL');b.width=min(bevel,min(dim)*.35);b.segments=3;bpy.ops.object.modifier_apply(modifier=b.name)
 if moving:parent(o)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(green if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Butt-jointed stone skins, no corner volume overlap.
for sy in [-1,1]:cube('Stone skin / front rear',(0,sy*1.145,.83),(3.26,.19,1.46),ivory)
for sx in [-1,1]:cube('Stone skin / side',(sx*1.745,0,.83),(.23,2.48,1.46),ivory)
cube('Stone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),ivory,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Stone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),ivory,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),green,True,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,True,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,True,.005)
  cube('Stone foot',(sx*1.47,sy*.91,-.10),(.52,.45,.35),green,bevel=.09)
# Original raised stone marquetry: separate closed prisms, all lid-owned.
def prism(name,pts,material):
 z0=1.977;z1=2.015;n=len(pts);v=[(x,y,z) for z in [z0,z1] for x,y in pts];faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o)
for k in range(8):
 a=k*math.tau/8;pts=[]
 for r,da in [(.18,0),(.43,-.20),(.66,0),(.43,.20)]:pts.append((r*math.cos(a+da),r*math.sin(a+da)))
 prism('Inlay / petal '+str(k),pts,red if k%2==0 else ivory)
for sx in [-1,1]:
 for sy in [-1,1]:
  for j in range(2):
   cx=sx*(.85+j*.34);cy=sy*(.42-j*.10);a=sy*sx*.55
   pts=[(cx+x*math.cos(a)-y*math.sin(a),cy+x*math.sin(a)+y*math.cos(a)) for x,y in [(-.19,0),(0,-.09),(.19,0),(0,.09)]]
   prism('Inlay / leaf',pts,ivory)
for sy in [-1,1]:cube('Inlay / brass border',(0,sy*.91,1.986),(3.04,.025,.016),gold,True,.004)
for sx in [-1,1]:cube('Inlay / brass border',(sx*1.51,0,1.986),(.025,1.80,.016),gold,True,.004)
bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.135,depth=.038,location=(0,0,1.997));o=bpy.context.object;o.name='Inlay / flower heart';o.data.materials.append(gold);parent(o)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.29
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.8));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.1))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
s=bpy.context.scene;s.camera=cam;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=1000;s.render.resolution_y=900;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.use_nodes=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'italy.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'italy.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
s.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('ITALY AUTHORED PASS')
