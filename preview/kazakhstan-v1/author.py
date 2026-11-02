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

felt=mat('Felt / warm wool',(.55,.42,.24),.92);maptex(felt,'felt-color.png','Base Color');maptex(felt,'felt-roughness.png','Roughness',True)
wood=mat('Wood / dark warm frame',(.18,.065,.023),.48);maptex(wood,'wood-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
red=mat('Applique / oxblood felt',(.20,.024,.033),.91)
seam=mat('Seam / dark wool',(.045,.027,.018),.95)

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

# Continuous skins around the retained five-sided hollow liner.
for sy in [-1,1]:cube('Felt body / front' if sy<0 else 'Felt body / rear',(0,sy*1.145,.83),(3.72,.19,1.46),felt,bevel=.025)
for sx in [-1,1]:cube('Felt body / side',(sx*1.745,0,.83),(.23,2.10,1.46),felt,bevel=.025,axis='Y')
for z in [.16,1.52]:
 for sy in [-1,1]:cube('Frame / long',(0,sy*1.245,z),(3.72,.05,.09),wood,bevel=.015)
 for sx in [-1,1]:cube('Frame / side',(sx*1.87,0,z),(.05,2.42,.09),wood,bevel=.015)
for sx in [-1,1]:
 for sy in [-1,1]:cube('Frame / corner',(sx*1.78,sy*1.17,.83),(.16,.16,1.40),wood,bevel=.02)
cube('Frame / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.08),seam,bevel=.009)
for sx in [-1,1]:cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.08),seam,bevel=.009)
for sx in [-1,1]:
 for sy in [-1,1]:cube('Frame / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
cube('Lid felt / inset',(0,0,1.981),(3.26,1.92,.024),felt,lid,.008)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Foot / wood',(sx*1.47,sy*.91,-.10),(.42,.36,.32),wood,bevel=.06)

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

# Original paired inward curls, generated independently of third-party imagery.
def curlpair(name,cx,cy,cz,plane='lid',p=lid,scale=1):
 for side in [-1,1]:
  points=[]
  for i in range(45):
   t=i/44;angle=-math.pi/2+t*math.pi*2.0;r=(.21-.145*t)*scale
   u=side*(.18*scale+r*math.cos(angle));v=r*math.sin(angle)
   points.append((cx+u,cy+v,cz) if plane=='lid' else ((cx,cy+u,cz+v) if plane=='side' else (cx+u,cy,cz+v)))
  tube(name,points,[.027*scale]*len(points),red,p,sides=8)
for x in [-1.02,1.02]:
 for y in [-.52,.52]:curlpair('Lid scroll / paired horn',x,y,2.025,scale=.95)
for x in [-1.05,1.05]:
 for sy in [-1,1]:curlpair('Body scroll / paired horn',x,sy*1.255,.88,'front',None,1.35)
for sx in [-1,1]:
 for y in [-.65,.65]:curlpair('Side scroll / paired horn',sx*1.875,y,.83,'side',None,.85)
# Circular low raised lattice, an original craft allusion, not official emblem.
pts=[(.49*math.cos(i*math.tau/80),.49*math.sin(i*math.tau/80),2.06) for i in range(81)]
tube('Lid medallion / circular wood rim',pts,[.033]*81,wood,sides=10)
for axis in [0,1]:
 for offset in [-.22,0,.22]:
  extent=math.sqrt(.46**2-offset**2)
  pts=[(-extent+2*extent*i/16,offset,2.06+.025*(1-((-extent+2*extent*i/16)/.46)**2)) for i in range(17)]
  if axis:pts=[(y,x,z+.045) for x,y,z in pts]
  tube('Lid medallion / lattice',pts,[.018]*len(pts),wood,sides=8)

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
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'kazakhstan.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'kazakhstan.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('KAZAKHSTAN AUTHORED')