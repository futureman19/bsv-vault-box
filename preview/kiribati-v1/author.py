"""Kiribati / Pandanus & Lagoon. Procedural source; original fantasy design."""
import bpy,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(134416)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p=lid):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def tex(m,file,socket,noncolor=False,normal=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file),check_existing=True)
 if noncolor:t.image.colorspace_settings.name='Non-Color'
 t.image.pack();out=t.outputs['Color']
 if normal:
  n=m.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.45;m.node_tree.links.new(out,n.inputs['Color']);out=n.outputs['Normal']
 m.node_tree.links.new(out,m.node_tree.nodes.get('Principled BSDF').inputs[socket])
fibre=mat('Pandanus / invented over-under weave',(.48,.28,.10),.7)
tex(fibre,'pandanus-color.png','Base Color');tex(fibre,'pandanus-roughness.png','Roughness',True);tex(fibre,'pandanus-normal.png','Normal',True,True)
frame=mat('Coconut brown / satin frame',(.105,.052,.020),.42)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
sand=mat('Coral sand / pale rim',(.70,.58,.35),.85);tex(sand,'sand-color.png','Base Color')
seam=mat('Seam / deep teal',(.013,.055,.050),.8)
enamel=mat('Lid / deep Pacific teal',(.008,.085,.10),.32,.08)
water=mat('Lagoon / opaque turquoise inlay',(.008,.27,.35),.22,.08)
reef=mat('Reef / shallow aqua',(.10,.55,.49),.36)
leaves=[mat('Coastal vegetation / '+str(i),c,.86) for i,c in enumerate([(.07,.16,.04),(.11,.24,.06),(.17,.28,.07)])]
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Physical projection')
 for f in o.data.polygons:
  for li in f.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   if abs(f.normal.z)>.7:u,v=co.x,co.y
   elif abs(f.normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u/3.72+.5,v/1.86+.5)
def cube(n,loc,dim,m,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if bevel:
  b=o.modifiers.new('Soft edges','BEVEL');b.width=min(bevel,min(dim)*.35);b.segments=2;bpy.ops.object.modifier_apply(modifier=b.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(frame if o.name.startswith('Interior') else gold)
# Woven skins, backed by the inherited continuous hollow liner.
for sy in [-1,1]:
 cube('Pandanus / front' if sy<0 else 'Pandanus / rear',(0,sy*1.145,.83),(3.48,.19,1.46),fibre,bevel=.018)
 for z in [.15,1.51]:cube('Frame / long rail',(0,sy*1.15,z),(3.72,.20,.10),frame,bevel=.016)
for sx in [-1,1]:
 cube('Pandanus / side',(sx*1.745,0,.83),(.23,2.10,1.46),fibre,bevel=.018)
 for z in [.15,1.51]:cube('Frame / short rail',(sx*1.745,0,z),(.23,2.38,.10),frame,bevel=.016)
 for sy in [-1,1]:cube('Frame / corner post',(sx*1.745,sy*1.145,.83),(.23,.19,1.46),frame,bevel=.014)
cube('Frame / clasp seat',(0,-1.255,1.36),(.56,.075,.47),frame,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Frame / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),frame,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),enamel,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def stone(n,loc,scale,m,p=None):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  k=1+random.uniform(-.09,.09);v.co=Vector((v.co.x*scale[0]*k,v.co.y*scale[1]*k,v.co.z*scale[2]*k))
 o.data.materials.append(m);uv(o)
 for f in o.data.polygons:f.use_smooth=True
 if p:parent(o,p)
 return o
for sx in [-1,1]:
 for sy in [-1,1]:stone('Coral foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sand)
# Genuine C-shaped rim mesh. Gap at 225 degrees (-X,-Y), never closed by sand.
N=100;rows=6;verts=[];faces=[]
for i in range(N+1):
 a=math.radians(242.5)+math.radians(325)*i/N
 wobble=1+.025*math.sin(7*a)+.018*math.sin(11*a+.4)
 for j in range(rows):
  t=j/(rows-1);rx=1.06+.34*t;ry=.46+.33*t
  z=1.983+(.045+.125*math.sin(math.pi*t)**.8)*(.88+.12*math.sin(3*a))
  z-=.025*(abs(i-N/2)/(N/2))**8
  verts.append((rx*math.cos(a)*wobble,ry*math.sin(a)*wobble,z))
for i in range(N):
 for j in range(rows-1):
  k=i*rows+j;faces.append((k,k+rows,k+rows+1,k+1))
me=bpy.data.meshes.new('Atoll sculpted ring');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Atoll / continuous C rim',me);bpy.context.collection.objects.link(o);me.materials.append(sand);uv(o);parent(o)
for f in me.polygons:f.use_smooth=True
# Water extends below the inner slope and through the front-left passage.
bpy.ops.mesh.primitive_cylinder_add(vertices=100,radius=1,depth=.018,location=(0,0,1.991));o=bpy.context.object;o.name='Lagoon / inset basin';o.scale=(1.17,.57,1);select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(water);parent(o)
# Shallow passage lies in the opening, connects basin to teal exterior.
verts=[];faces=[]
for i in range(17):
 a=math.radians(213+i*1.5)
 for rx,ry in [(1.02,.47),(1.40+.018*math.sin(i*.7),.79)]:verts.append((rx*math.cos(a),ry*math.sin(a),2.001))
for i in range(16):k=i*2;faces.append((k,k+1,k+3,k+2))
me=bpy.data.meshes.new('Curved tidal passage');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Lagoon / open passage',me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o)
# A narrow shallow-water inner rim uses lower sparse stones, not a photo plane.
for i in range(18):
 a=math.radians(20+i*8);rx=1.24;ry=.635
 stone('Atoll vegetation / low coastal patch',(rx*math.cos(a),ry*math.sin(a),2.125),(.13,.065,.065),leaves[i%3],lid)
def disk(n,loc,r,depth,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold);b=o.modifiers.new('Rounded brass','BEVEL');b.width=.005;b.segments=2;select(o);bpy.ops.object.modifier_apply(modifier=b.name);return o
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035)
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(0,-1.282,.87),major_radius=.107,minor_radius=.008,rotation=(math.pi/2,0,0));bpy.context.object.name='Medallion / raised rim';bpy.context.object.data.materials.append(gold)
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for im in list(bpy.data.images):
 if im.users==0:bpy.data.images.remove(im)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.10))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.8
s=bpy.context.scene;s.camera=cam;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=1000;s.render.resolution_y=900;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.use_nodes=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'kiribati.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'kiribati.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
s.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('KIRIBATI AUTHORED')
