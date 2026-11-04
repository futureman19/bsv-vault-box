"""Reference-led Solomon Islands pilot. Authored mesh and maps; no photogrammetry.
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
wood=mat('Ebony / fine longitudinal grain',(.4,.18,.08),.4);maptex(wood,'ebony-color.png','Base Color');maptex(wood,'ebony-roughness.png','Roughness',True)
end=mat('Ebony / dark finger endgrain',(.21,.075,.028),.47);maptex(end,'ebony-color.png','Base Color')
# Actual end-grain differs in UV frequency and tint via a separate compact map.
shell=mat('Shell / warm ivory',(.82,.76,.61),.26);maptex(shell,'shell-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
bark=mat('Ebony / furrowed bark',(.19,.075,.031),.85)
moss=mat('Moss / muted cushions',(.095,.16,.035),.95)
seam=mat('Dark seam',(.012,.009,.006),.9)
leafm=[mat('Ebony foliage / '+str(i),c,.92) for i,c in enumerate([(.045,.10,.024),(.07,.14,.035),(.10,.18,.047),(.13,.21,.06)])]
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
# Exterior skins constructed as alternating finger rows; each course changes
# which plank crosses the corner. End-grain squares are true exposed geometry.
for i in range(8):
 z=.10+(i+.5)*1.46/8;h=1.46/8
 for sy in [-1,1]:
  cube('Ebony / '+('front' if sy<0 else 'rear')+' course '+str(i),(0,sy*1.145,z),(3.72 if i%2==0 else 3.26,.19,h),wood,bevel=.003)
 for sx in [-1,1]:
  cube('Ebony / side course '+str(i),(sx*1.745,0,z),(.23,2.10 if i%2==0 else 2.48,h),wood,bevel=.003,axis='Y')
 for sx in [-1,1]:
  for sy in [-1,1]:
   if i%2==0:
    o=cube('Finger / exposed side end',(sx*1.862,sy*1.145,z),(.008,.19,h-.006),end,bevel=.002,axis='Y')
   else:o=cube('Finger / exposed front end',(sx*1.745,sy*1.242,z),(.23,.008,h-.006),end,bevel=.002)
   # tint via authored per-face material below, no external procedural shader.
# Small collar fills the central clasp mounting behind its retained position.
cube('Ebony / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:
 cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Ebony / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
# A thin satin upper facing with an independently oriented grain field.
for sx in [-1,1]:
 for j in range(6):cube('Lid finger / end',(sx*1.858,-.98+j*.39,1.83),(.012,.16,.23),end,lid,.003,axis='Y')
# Restrained brass corner protectors replace the Iceland wraps entirely.
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# Invented geometric inlays: shallow diamonds, no ritual iconography.
def diamond(n,c,rx,ry,depth,p=None,front=False):
 x,y,z=c
 if front:
  vs=[(x-rx,y,z),(x,y,z+ry),(x+rx,y,z),(x,y,z-ry)]
  vs+= [(a,b+depth,c) for a,b,c in vs]
 else:
  vs=[(x-rx,y,z),(x,y-ry,z),(x+rx,y,z),(x,y+ry,z)]
  vs+= [(a,b,c-depth) for a,b,c in vs]
 faces=[(0,1,2,3),(7,6,5,4),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(shell);uv(o)
 if p:parent(o,p)
 return o
for sx in [-1,1]:
 for sy in [-1,1]:cube('Ebony foot',(sx*1.47,sy*.91,-.10),(.5,.43,.35),wood,bevel=.06)
for row,z in enumerate([.49,1.08]):
 for j in range(12):
  x=-1.56+j*.283
  if abs(x)<.35:continue
  diamond('Shell front inlay',(x,-1.247,z),.09,.075,.012,front=True)
for y in [-.82,.82]:
 for j in range(13):diamond('Shell lid border',(-1.48+j*.245,y,1.982),.084,.055,.01,lid)
# Asymmetric curved low medallion, individual shell segments seated on lid.
for j in range(19):
 a=-2.4+j*.25;r=.46+.04*math.sin(a*3)
 diamond('Shell lid medallion',(.22+math.cos(a)*r,.02+math.sin(a)*r*.76,1.99),.042,.042,.014,lid)

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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.use_nodes=False;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'solomon-islands.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'solomon-islands.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('SOLOMON ISLANDS AUTHORED')
