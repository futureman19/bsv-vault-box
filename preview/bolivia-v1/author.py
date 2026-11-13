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
salt=mat('Salt / halite ivory',(.8,.8,.75),.64);maptex(salt,'salt-color.png','Base Color');maptex(salt,'salt-roughness.png','Roughness',True)
t=salt.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/salt-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=salt.node_tree.nodes.new('ShaderNodeNormalMap');salt.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);salt.node_tree.links.new(n.outputs['Normal'],salt.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / slate',(.16,.20,.23),.8)
blue=mat('Sky reflection / pale blue',(.30,.55,.68),.18,.28)
ochre=mat('Tunupa / ochre rock',(.34,.15,.055),.85)
ridge=mat('Salt / raised white ridges',(.92,.90,.82),.7)
wood=salt;granite=salt
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   normal=p.normal
   if abs(normal.z)>.7:u,v=co.x,co.y
   elif abs(normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u*.45+.5,v*.45+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(salt if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for i in range(8):
 z=.10+(i+.5)*1.46/8;h=1.46/8
 for sy in [-1,1]:cube('Salt body / long course '+str(i),(0,sy*1.145,z),(3.72,.19,h),salt,bevel=.004)
 for sx in [-1,1]:cube('Salt body / end course '+str(i),(sx*1.745,0,z),(.23,2.10,h),salt,bevel=.004)
cube('Salt / clasp seat',(0,-1.255,1.36),(.56,.075,.47),salt,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Salt / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),salt,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),salt,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
cube('Uyuni / sky inset',(0,0,1.992),(2.90,1.80,.028),blue,lid,.012)
def stone(n,loc,scale,p=None,material=granite,sub=2):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  k=1+random.uniform(-.11,.11);v.co=Vector((v.co.x*scale[0]*k,v.co.y*scale[1]*k,v.co.z*scale[2]*k))
 o.data.materials.append(material);uv(o)
 for face in o.data.polygons:face.use_smooth=True
 if p:parent(o,p)
 return o
for sx in [-1,1]:
 for sy in [-1,1]:stone('Salt foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)
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
# Honeycomb network: narrow physical ridges, not painted cracks.
for row in range(4):
 for col in range(6):
  x=-1.22+col*.44+(row%2)*.22;y=-.60+row*.40
  if x>1.30:continue
  pts=[(x+.245*math.cos(math.tau*j/6),y+.245*math.sin(math.tau*j/6),2.016) for j in range(7)]
  tube('Uyuni / salt polygon',pts,[.009]*7,ridge,sides=5)
# Small irregular ochre massif; basal skirt intersects inset for attachment.
verts=[];faces=[]
# Multi-summit eroded relief: concentric irregular contours, not a cone.
for ring in range(5):
 r=1-ring*.21
 for j in range(24):
  a=j*math.tau/24;rr=r*(1+.075*math.sin(j*2.3+ring))
  z=1.999+.48*(1-r)**.8+.07*math.sin(a*3+ring*.8)*(1-r)
  verts.append((.85+math.cos(a)*.44*rr,.55+math.sin(a)*.30*rr,z))
for ring in range(4):
 for j in range(24):
  a=ring*24+j;b=ring*24+(j+1)%24;c=b+24;d=a+24
  faces.extend([(a,b,d),(b,c,d)])
verts.append((.84,.55,2.52))
for j in range(24):faces.append((96+j,96+(j+1)%24,120))
faces.append(tuple(reversed(range(24))))
me=bpy.data.meshes.new('Tunupa relief');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Uyuni / Tunupa relief',me);bpy.context.collection.objects.link(o);me.materials.append(ochre);parent(o);uv(o)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'bolivia.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'bolivia.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('BOLIVIA AUTHORED')
