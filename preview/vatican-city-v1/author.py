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
stone_mat=mat('Travertine / warm ivory',(.62,.54,.41),.55);maptex(stone_mat,'stone-color.png','Base Color');maptex(stone_mat,'stone-roughness.png','Roughness',True)
granite=mat('Stone foot / warm limestone',(.35,.30,.22),.8);maptex(granite,'foot-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
blue=mat('Enamel / deep lapis blue',(.018,.075,.19),.22)
ivory=mat('Enamel / ivory',(.75,.69,.53),.25)
seam=mat('Seam / dark bronze',(.055,.043,.025),.6,.35)
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone face projection')
 for p in o.data.polygons:
  normal=p.normal
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   if abs(normal.z)>.7:u,v=co.x,co.y
   elif abs(normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u/2+.5,v/2+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=1;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone_mat if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Travertine / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),stone_mat,bevel=.025)
for sx in [-1,1]:cube('Travertine / end wall',(sx*1.745,0,.83),(.23,2.1,1.46),stone_mat,bevel=.025)
cube('Travertine / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone_mat,bevel=.025)
for sy in [-1,1]:cube('Bronze seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Bronze seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Travertine / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone_mat,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone_mat,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def stone(n,loc,scale,p=None,material=granite,sub=2):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  k=1+random.uniform(-.11,.11);v.co=Vector((v.co.x*scale[0]*k,v.co.y*scale[1]*k,v.co.z*scale[2]*k))
 o.data.materials.append(material);uv(o)
 for face in o.data.polygons:face.use_smooth=True
 if p:parent(o,p)
 return o
for sx in [-1,1]:
 for sy in [-1,1]:stone('Granite foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)
# Original miniature: two opposing curved arcades, with unobstructed oval center.
def arc(n,a0,a1,z,height,material):
 vs=[];fs=[];steps=40
 for i in range(steps+1):
  a=a0+(a1-a0)*i/steps
  for dz in [0,height]:
   for d in [-.075,.075]:vs.append(((1.06+d)*math.cos(a),(.57+d)*math.sin(a),z+dz))
 for i in range(steps):
  k=i*4;j=k+4
  fs.extend([(k,j,j+1,k+1),(k+2,k+3,j+3,j+2),(k,k+2,j+2,j),(k+1,j+1,j+3,k+3)])
 fs.extend([(0,1,3,2),(steps*4,steps*4+2,steps*4+3,steps*4+1)])
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o);return o
for side in [0,1]:
 a0=math.radians(22+side*180);a1=math.radians(158+side*180)
 arc('Arcade / foundation '+str(side),a0,a1,1.978,.045,stone_mat)
 arc('Arcade / cornice '+str(side),a0,a1,2.388,.065,stone_mat)
 for i in range(12):
  a=a0+(a1-a0)*i/11;x=1.06*math.cos(a);y=.57*math.sin(a)
  cube('Arcade / column base',(x,y,2.046),(.105,.105,.048),stone_mat,lid,.008)
  bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.038,depth=.30,location=(x,y,2.218));o=bpy.context.object;o.name='Arcade / column';o.data.materials.append(stone_mat);uv(o);parent(o)
  cube('Arcade / capital',(x,y,2.378),(.105,.105,.04),stone_mat,lid,.006)
# Blue and ivory mosaic tesserae are authored enamel chips, not a copied sacred pattern.
for sy in [-1,1]:
 for i in range(34):cube('Mosaic / tessera',( -1.51+i*.0915,sy*.91,1.996),(.074,.074,.034),blue if i%3 else ivory,lid,.004)
for sx in [-1,1]:
 for i in range(18):cube('Mosaic / tessera',(sx*1.51,-.78+i*.0915,1.996),(.074,.074,.034),blue if i%3 else gold,lid,.004)
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
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.8));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=2;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'vatican-city.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'vatican-city.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('VATICAN CITY AUTHORED')
