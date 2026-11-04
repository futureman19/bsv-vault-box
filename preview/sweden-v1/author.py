"""Brief-led Sweden pilot. Authored mesh and maps; no photogrammetry.
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
wood=mat('Falun red / painted wood',(.4,.18,.08),.4);maptex(wood,'red-color.png','Base Color');maptex(wood,'wood-roughness.png','Roughness',True)
end=mat('Pine / exposed endgrain',(.21,.075,.028),.47);maptex(end,'wood-end.png','Base Color')
# Actual end-grain differs in UV frequency and tint via a separate compact map.
granite=mat('Dark wooden feet',(.065,.030,.015),.72)
inner=mat('Pine / pale interior',(.60,.43,.23),.65);maptex(inner,'wood-end.png','Base Color')
blue=mat('Kurbits / blue ground',(.025,.085,.18),.48)
cream=mat('Kurbits / warm ivory',(.83,.67,.40),.5)
green=mat('Kurbits / leaf green',(.052,.13,.050),.6)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
bark=mat('Red wood / furrowed bark',(.19,.075,.031),.85)
moss=mat('Moss / muted cushions',(.095,.16,.035),.95)
seam=mat('Dark seam',(.028,.018,.012),.9)
leafm=[mat('Cedar foliage / '+str(i),c,.92) for i,c in enumerate([(.045,.10,.024),(.07,.14,.035),(.10,.18,.047),(.13,.21,.06)])]
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
  o.data.materials.clear();o.data.materials.append(inner if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o,'Y' if 'end' in o.name else 'X')
# Exterior skins constructed as alternating finger rows; each course changes
# which plank crosses the corner. End-grain squares are true exposed geometry.
for i in range(8):
 z=.10+(i+.5)*1.46/8;h=1.46/8
 for sy in [-1,1]:
  cube('Red wood / '+('front' if sy<0 else 'rear')+' course '+str(i),(0,sy*1.145,z),(3.72 if i%2==0 else 3.26,.19,h),wood,bevel=.003)
 for sx in [-1,1]:
  cube('Red wood / side course '+str(i),(sx*1.745,0,z),(.23,2.10 if i%2==0 else 2.48,h),wood,bevel=.003,axis='Y')
 for sx in [-1,1]:
  for sy in [-1,1]:
   if i%2==0:
    o=cube('Finger / exposed side end',(sx*1.862,sy*1.145,z),(.008,.19,h-.006),end,bevel=.002,axis='Y')
   else:o=cube('Finger / exposed front end',(sx*1.745,sy*1.242,z),(.23,.008,h-.006),end,bevel=.002)
   # tint via authored per-face material below, no external procedural shader.
# Small collar fills the central clasp mounting behind its retained position.
cube('Red wood / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:
 cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Red wood / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
# A thin satin upper facing with an independently oriented grain field.
for sx in [-1,1]:
 for j in range(6):cube('Lid finger / end',(sx*1.858,-.98+j*.39,1.83),(.012,.16,.23),end,lid,.003,axis='Y')
# Restrained brass corner protectors replace the Iceland wraps entirely.
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
 for sy in [-1,1]:cube('Dark wood foot',(sx*1.47,sy*.91,-.10),(.46,.40,.30),granite,bevel=.045)
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
# Invented kurbits-inspired relief, not a historical motif reproduction.
cube('Kurbits / blue inset',(0,0,2.00),(3.10,1.72,.060),blue,lid,.015)
def leaf(n,x,y,angle,scale,material):
 # Closed lenticular prism with a gently raised central ridge.
 verts=[(-scale,0,0),(0,-scale*.38,0),(scale,0,0),(0,scale*.38,0),(0,0,.028)]
 verts=[(x+u*math.cos(angle)-v*math.sin(angle),y+u*math.sin(angle)+v*math.cos(angle),2.026+z) for u,v,z in verts]
 faces=[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(3,2,1,0)]
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);parent(o)
for side in [-1,1]:
 points=[(0,-.62,2.054),(side*.28,-.36,2.054),(side*.56,-.02,2.054),(side*.86,.25,2.054),(side*1.12,.37,2.054)]
 tube('Kurbits / curling stem',points,[.025]*5,cream,sides=8)
 for j in range(5):
  x=side*(.22+j*.18);y=-.37+j*.15
  leaf('Kurbits / green leaf',x,y+.14,side*1.0,.16,green)
  leaf('Kurbits / ivory leaf',x+.06*side,y-.12,side*-.65,.13,cream)
for cx,cy,r in [(0,.34,.25),(-1.12,.39,.18),(1.12,.39,.18)]:
 for j in range(8):
  a=j*math.tau/8
  leaf('Kurbits / flower petal',cx+math.cos(a)*r*.60,cy+math.sin(a)*r*.60,a,r*.57,cream)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=1,location=(cx,cy,2.064));o=bpy.context.object;o.name='Kurbits / red flower heart';o.scale=(r*.40,r*.40,.035);o.data.materials.append(wood);uv(o);parent(o)
tube('Kurbits / central stem',[(0,-.62,2.054),(0,-.2,2.054),(0,.34,2.054)],[.024]*3,cream,sides=8)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'sweden.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'sweden.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('SWEDEN AUTHORED')
