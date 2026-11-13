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
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Ceramic face UV')
 for face in o.data.polygons:
  ax=max(range(3),key=lambda i:abs(face.normal[i])); axes=[i for i in range(3) if i!=ax]
  for li in face.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]/.82+.5,co[axes[1]]/.82+.5)

def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
# Included by setup.py into the standalone author.py.
ceramic=mat('Iznik / ivory floral glaze',(.78,.74,.63),.27)
maptex(ceramic,'ceramic-color.png','Base Color');maptex(ceramic,'ceramic-roughness.png','Roughness',True)
blue=mat('Iznik / cobalt glaze',(.012,.05,.22),.24);maptex(blue,'cobalt-roughness.png','Roughness',True)
ivory=mat('Iznik / ivory inset',(.79,.76,.65),.3)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
red=mat('Iznik / tomato red relief',(.54,.031,.019),.3)
green=mat('Iznik / turquoise foliage',(.014,.22,.17),.32)
seam=mat('Seam / deep cobalt',(.008,.018,.05),.7)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(ivory if o.name.startswith('Interior') else gold)
for sy in [-1,1]:cube('Ceramic / front' if sy<0 else 'Ceramic / rear',(0,sy*1.145,.83),(3.26,.19,1.46),ceramic,bevel=.014)
for sx in [-1,1]:cube('Ceramic / side',(sx*1.745,0,.83),(.23,2.48,1.46),ceramic,bevel=.014)
cube('Ceramic / clasp seat',(0,-1.255,1.36),(.56,.075,.47),blue,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Ceramic / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),blue,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),blue,lid,.045)
cube('Ornament / ivory panel',(0,0,1.989),(3.20,1.86,.038),ivory,lid,.015)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Cobalt / foot',(sx*1.47,sy*.91,-.075),(.49,.43,.30),blue,bevel=.07)
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
# Three raised original tulip silhouettes, not copied museum motifs.
def relief(name,xy,material):
 n=len(xy);verts=[(x,y,z) for z in [2.006,2.065] for x,y in xy]
 faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(material);parent(o);return o
for i,x in enumerate([-.92,0,.92]):
 top=.30 if i!=1 else .55
 pts=[(x-.04,-.68,2.018),(x-.12,-.34,2.018),(x+.03,-.05,2.018),(x,top-.18,2.018)]
 tube('Ornament / stem '+str(i),pts,[.019]*4,green,sides=8)
 shape=[(-.17,-.12),(-.26,.18),(-.10,.10),(0,.31),(.10,.10),(.26,.18),(.17,-.12),(0,-.22)]
 relief('Ornament / tulip '+str(i),[(x+a,top+b) for a,b in shape],red)
 for side in [-1,1]:
  relief('Ornament / leaf '+str(i)+' '+str(side),[(x,-.25),(x+side*.30,-.05),(x+side*.21,-.41),(x,-.46)],green)
# Cobalt beaded border is co-moving with the ceramic panel.
for sy in [-1,1]:
 for j in range(23):
  x=-1.43+j*2.86/22
  bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=4,radius=1,location=(x,sy*.82,2.018));o=bpy.context.object;o.name='Ornament / cobalt border';o.scale=(.026,.026,.012);o.data.materials.append(blue);parent(o)
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
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=960;scene.render.resolution_y=880;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'turkey.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'turkey.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('TURKEY AUTHORED')
