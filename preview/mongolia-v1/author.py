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

felt=mat('Felt / ivory fibers',(.65,.58,.42),.88);maptex(felt,'felt-color.png','Base Color');maptex(felt,'felt-roughness.png','Roughness',True)
wood=mat('Frame / ochre red lacquer',(.25,.055,.022),.38)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / midnight blue',(.018,.047,.065),.85)
grass=mat('Steppe / olive grass',(.18,.23,.055),.95);maptex(grass,'steppe-color.png','Base Color')
stone=mat('Foot / dark stone',(.07,.065,.05),.85)
rope=mat('Ger / dark ropes',(.085,.055,.025),.85)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
for sy in [-1,1]:
 cube('Felt / long panel',(0,sy*1.145,.83),(3.72,.19,1.46),felt,bevel=.025)
 for z in [.16,1.49]:cube('Frame / long rail',(0,sy*1.247,z),(3.72,.035,.11),wood,bevel=.012)
for sx in [-1,1]:
 cube('Felt / side panel',(sx*1.745,0,.83),(.23,2.10,1.46),felt,bevel=.025,axis='Y')
 for z in [.16,1.49]:cube('Frame / side rail',(sx*1.875,0,z),(.035,2.38,.11),wood,bevel=.012)
 for sy in [-1,1]:
  cube('Frame / corner binding',(sx*1.74,sy*1.248,.83),(.12,.04,1.46),wood,bevel=.01)
  cube('Stone foot',(sx*1.47,sy*.91,-.10),(.48,.42,.29),stone,bevel=.08)
cube('Frame / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Frame / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# Closed oval relief: top rings plus skirt reaching the actual lid.
verts=[(0,0,2.10)];faces=[];rings=12;segs=80
for k in range(1,rings+1):
 r=k/rings
 for j in range(segs):
  a=j*math.tau/segs;x=1.48*r*math.cos(a);y=.83*r*math.sin(a)
  z=2.06+.045*math.sin(x*2.7)*math.cos(y*3.1)
  if (x-.55)**2+(y-.25)**2<.46**2:z=2.10
  verts.append((x,y,z))
for j in range(segs):faces.append((0,1+j,1+(j+1)%segs))
for k in range(rings-1):
 for j in range(segs):
  a=1+k*segs+j;b=1+k*segs+(j+1)%segs;faces.append((a,a+segs,b+segs,b))
start=len(verts)
for j in range(segs):a=j*math.tau/segs;verts.append((1.48*math.cos(a),.83*math.sin(a),1.97))
for j in range(segs):a=1+(rings-1)*segs+j;b=1+(rings-1)*segs+(j+1)%segs;faces.append((a,start+j,start+(j+1)%segs,b))
faces.append(tuple(reversed(range(start,start+segs))))
me=bpy.data.meshes.new('Steppe closed relief');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Steppe / rolling oval',me);bpy.context.collection.objects.link(o);me.materials.append(grass);uv(o);parent(o)
def cone(n,z,r1,r2,depth,material):
 bpy.ops.mesh.primitive_cone_add(vertices=64,radius1=r1,radius2=r2,depth=depth,location=(.55,.25,z));o=bpy.context.object;o.name=n;o.data.materials.append(material);uv(o);parent(o)
 for p in o.data.polygons:p.use_smooth=len(p.vertices)==4
 return o
cone('Ger / felt wall',2.25,.40,.40,.30,felt)
cone('Ger / peaked felt roof',2.525,.42,.105,.25,felt)
cone('Ger / crown',2.655,.105,.105,.018,wood)
cube('Ger / red door',(.55,-.153,2.235),(.16,.018,.25),wood,lid,.008)
cube('Ger / door brass pull',(.595,-.169,2.235),(.013,.015,.035),gold,lid,.004)
for z in [2.17,2.34]:
 bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=6,major_radius=.401,minor_radius=.009,location=(.55,.25,z));o=bpy.context.object;o.name='Ger / rope band';o.data.materials.append(rope);parent(o)
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

for j in range(12):
 a=j*math.tau/12
 tube('Ger / roof cord',[(.55+.108*math.cos(a),.25+.108*math.sin(a),2.654),(.55+.425*math.cos(a),.25+.425*math.sin(a),2.403)],[.005,.005],rope,sides=6)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'mongolia.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'mongolia.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('MONGOLIA AUTHORED')
