"""Sarajevo copper craft-inspired pilot. Authored mesh and maps; no photogrammetry.
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
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z
   if axis=='Y' and abs(p.normal.z)>.7:v=co.x
   layer.data[li].uv=(u/3.72+.5,v/1.7+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
copper=mat('Copper / hammered satin',(.40,.16,.07),.42,.78)
maptex(copper,'copper-color.png','Base Color');maptex(copper,'copper-roughness.png','Roughness',True)
t=copper.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/copper-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack()
n=copper.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.32;copper.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);copper.node_tree.links.new(n.outputs['Normal'],copper.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
bronze=mat('Bronze / dark interior',(.065,.032,.018),.58,.6)
seam=mat('Patina / dark teal seam',(.018,.065,.055),.8,.2)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(bronze if o.name.startswith('Interior') else gold)
for sy in [-1,1]:cube('Copper / front rear skin',(0,sy*1.145,.83),(3.26,.19,1.46),copper,bevel=.008)
for sx in [-1,1]:cube('Copper / side skin',(sx*1.745,0,.83),(.23,2.48,1.46),copper,bevel=.008,axis='Y')
cube('Copper / clasp seat',(0,-1.255,1.36),(.56,.075,.47),copper,bevel=.025)
for sy in [-1,1]:cube('Patina seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Patina seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:
  cube('Copper / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),copper,bevel=.004)
  cube('Bronze / foot',(sx*1.47,sy*.91,-.08),(.48,.42,.34),bronze,bevel=.06)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),copper,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def disc(name,r,z,depth,material):
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=depth,location=(0,0,z));o=bpy.context.object;o.name=name;o.data.materials.append(material);uv(o);parent(o);return o
disc('Ornament / copper tray',.78,1.991,.032,copper)
disc('Ornament / central boss',.115,2.025,.06,gold)
def tube(n,points,radii,material,p=lid,sides=9):
 verts=[];faces=[]
 for i,c in enumerate(points):
  c=Vector(c);t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);t.normalize();a=t.cross(Vector((0,1,0)))
  if a.length<.01:a=t.cross(Vector((1,0,0)))
  a.normalize();b=t.cross(a).normalized()
  for j in range(sides):verts.append(c+radii[i]*(a*math.cos(j*math.tau/sides)+b*math.sin(j*math.tau/sides)))
 for i in range(len(points)-1):
  for j in range(sides):a=i*sides+j;bb=i*sides+(j+1)%sides;faces.append((a,bb,bb+sides,a+sides))
 faces.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))]);me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material)
 for f in me.polygons:f.use_smooth=True
 if p:parent(o,p)
 return o
for radius in [.76,.24]:
 pts=[(radius*math.cos(j*math.tau/96),radius*math.sin(j*math.tau/96),2.014) for j in range(97)]
 tube('Ornament / ring',pts,[.012]*len(pts),gold,sides=8)
for k in range(8):
 a=k*math.tau/8;pts=[]
 for j in range(49):
  t=j*math.tau/48;rad=.46+.20*math.cos(t);side=.10*math.sin(t)
  pts.append((rad*math.cos(a)-side*math.sin(a),rad*math.sin(a)+side*math.cos(a),2.022))
 tube('Ornament / petal '+str(k),pts,[.014]*len(pts),gold,sides=8)
for sy in [-1,1]:
 for k in range(25):
  x=-1.5+k*.125
  bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=4,radius=.022,location=(x,sy*.97,1.985));o=bpy.context.object;o.name='Border / punched bead';o.data.materials.append(gold);parent(o)
for sx in [-1,1]:
 for k in range(13):
  bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=4,radius=.022,location=(sx*1.57,-.78+k*.13,1.985));o=bpy.context.object;o.name='Border / punched bead';o.data.materials.append(gold);parent(o)
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
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'bosnia-and-herzegovina.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'bosnia-and-herzegovina.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('BOSNIA AND HERZEGOVINA AUTHORED')
