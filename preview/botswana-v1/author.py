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
palm=mat('Mokola / coiled palm fibre',(.47,.35,.18),.78)
maptex(palm,'palm-color.png','Base Color');maptex(palm,'palm-roughness.png','Roughness',True)
t=palm.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/palm-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack()
n=palm.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.45;palm.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);palm.node_tree.links.new(n.outputs['Normal'],palm.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
liner=mat('Interior / dark umber',(.085,.047,.024),.85)
seam=mat('Seam / dark woven umber',(.048,.025,.012),.9)
granite=mat('Sand / warm island',(.46,.36,.19),.93)
water=mat('Delta / blue green waterways',(.032,.25,.27),.25,.18)
reed=mat('Delta / muted reed islands',(.18,.21,.063),.9)
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
  o.data.materials.clear();o.data.materials.append(liner if o.name.startswith('Interior') else gold)
# Continuous basket-inspired panels over the retained hollow liner.
for sy in [-1,1]:cube('Palm / front rear panel',(0,sy*1.145,.83),(3.72,.19,1.46),palm,bevel=.035)
for sx in [-1,1]:cube('Palm / side panel',(sx*1.745,0,.83),(.23,2.10,1.46),palm,bevel=.035,axis='Y')
cube('Palm / clasp seat',(0,-1.255,1.36),(.56,.075,.47),palm,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Palm / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),palm,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),palm,lid,.045)
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
# Fine physical coil ribs above the mapped fibre. Not just a printed texture.
for i in range(24):
 z=.14+i*.059
 for sy in [-1,1]:cube('Coil / long',(0,sy*1.242,z),(3.60,.016,.019),palm,bevel=.006)
 for sx in [-1,1]:cube('Coil / side',(sx*1.867,0,z),(.016,2.25,.019),palm,bevel=.006,axis='Y')
for sx in [-1,1]:
 for sy in [-1,1]:cube('Foot / woven shoe',(sx*1.47,sy*.91,-.10),(.48,.42,.30),liner,bevel=.07)
# Low continuous sandy fan, with individually shaped wetland islands.
# A level top avoids interpenetrating water ribbons; irregular footprint remains sculptural.
verts=[(0,.03,2.075)];faces=[]
for i in range(64):
 a=i*math.tau/64;r=1+.035*math.sin(5*a)+.018*math.cos(9*a)
 verts.append((1.42*r*math.cos(a),.03+.85*r*math.sin(a),2.075))
for i in range(64):faces.append((0,i+1,(i+1)%64+1))
for i in range(64):
 x,y,z=verts[i+1];verts.append((x*.96,y*.96,1.99))
for i in range(64):faces.append((i+1,65+i,65+(i+1)%64,(i+1)%64+1))
faces.append(tuple(reversed(range(65,129))))
me=bpy.data.meshes.new('Sand fan');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Delta / sand foundation',me);bpy.context.collection.objects.link(o);me.materials.append(granite);parent(o)
# Branching connected channels laid as tapered triangulated ribbons.
paths=[[(.05,.71),(.04,.46),(-.08,.22),(-.1,-.07),(-.34,-.40),(-.58,-.69)],
 [(-.08,.22),(.24,.09),(.52,-.12),(.77,-.35),(1.14,-.53)],
 [(.04,.46),(-.38,.30),(-.67,.09),(-.96,-.21),(-1.20,-.44)],
 [(-.1,-.07),(.16,-.30),(.28,-.57),(.35,-.72)],
 [(-.67,.09),(-.78,-.17),(-.74,-.45),(-.88,-.62)]]
for k,path in enumerate(paths):
 verts=[];faces=[]
 for i,(x,y) in enumerate(path):
  t=Vector(path[min(i+1,len(path)-1)])-Vector(path[max(0,i-1)]);t.normalize();w=.055 if k==0 else .035
  # top has slight height variation, all branches meet above the sand cap.
  for sign in [-1,1]:verts.append((x-sign*t.y*w,y+sign*t.x*w,2.079))
 for i in range(len(path)-1):faces.append((2*i+2,2*i+3,2*i+1,2*i))
 me=bpy.data.meshes.new('Water ribbon');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Delta / channel '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o)
for i,(x,y,rx,ry) in enumerate([(-.38,.02,.18,.19),(.37,-.39,.10,.17),(.67,.12,.26,.21),(-.95,.35,.23,.14),(.3,.51,.16,.13),(-.43,-.54,.10,.09),(.85,-.58,.22,.10),(-1.06,-.09,.13,.12)]):
 stone('Delta / reed island '+str(i),(x,y,2.09),(rx,ry,.075),lid,reed,2)
 # clustered reed blades, each rooted on its own island.
 for j in range(7):
  dx=random.uniform(-rx*.5,rx*.5);dy=random.uniform(-ry*.5,ry*.5)
  tube('Delta / reed',[(x+dx,y+dy,2.12),(x+dx+.025,y+dy,2.22+random.random()*.06)],[.008,.002],reed,sides=4)
# Slim raised woven lid framing, clear of all hardware.
for sy in [-1,1]:cube('Lid / woven border long',(0,sy*.98,2.0),(3.20,.055,.044),palm,lid,.012)
for sx in [-1,1]:cube('Lid / woven border end',(sx*1.58,0,2.0),(.055,1.95,.044),palm,lid,.012,axis='Y')
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
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'botswana.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'botswana.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('BOTSWANA AUTHORED')
