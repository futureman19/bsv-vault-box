"""Jordan / Wadi Rum: independently procedural sandstone and carved massifs.
Inherited trimmed BoxSV articulation only. All resources resolve in this folder.
"""
import bpy,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(1377)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;s=m.node_tree.nodes.get('Principled BSDF');s.inputs['Base Color'].default_value=(*c,1);s.inputs['Roughness'].default_value=r;s.inputs['Metallic'].default_value=metal;return m
def tex(m,f,slot,non=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/f),check_existing=True)
 if non:t.image.colorspace_settings.name='Non-Color'
 t.image.pack();m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[slot])
stone=mat('Sandstone / rose and ochre',(.42,.17,.08),.78);tex(stone,'sandstone-color.png','Base Color');tex(stone,'sandstone-roughness.png','Roughness',True)
red=mat('Lid / satin dark rose sandstone',(.22,.075,.04),.34);tex(red,'lid-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
liner=mat('Interior / warm dark stone',(.14,.055,.027),.6)
sand=mat('Sand / ochre valley',(.50,.28,.115),.92)
seam=mat('Seam / dark umber',(.055,.021,.012),.85)
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone coordinates')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   u=(co.x+co.y)*.18+.5;v=(co.y*.4+.5) if abs(p.normal.z)>.7 else co.z*.55
   layer.data[li].uv=(u,v)
def cube(n,loc,dim,m,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if bevel:
  mod=o.modifiers.new('Eroded edges','BEVEL');mod.width=min(bevel,min(dim)*.35);mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(liner if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Sandstone / front' if sy<0 else 'Sandstone / rear',(0,sy*1.145,.83),(3.72,.19,1.46),stone,bevel=.026)
for sx in [-1,1]:cube('Sandstone / side',(sx*1.745,0,.83),(.23,2.10,1.46),stone,bevel=.025)
cube('Sandstone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Sandstone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),red,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Sandstone / foot',(sx*1.47,sy*.91,-.09),(.48,.42,.32),red,bevel=.09)
# Low sandy inset leaves the dark stone border clearly visible.
cube('Terrain / sandy inset',(0,0,1.991),(3.12,1.90,.03),sand,lid,.01)
def mesh(n,vs,fs,m,p=lid):
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(m);uv(o)
 if p:parent(o,p)
 return o
# Two eroded massifs: unequal scalloped rings, vertical flutes, irregular summits.
# Convex footprint stays on its own side of the real open central siq.
def massif(n,cx,cy,rx,ry,height,phase):
 vs=[];fs=[];segments=64;levels=12
 for j in range(levels+1):
  t=j/levels
  taper=1-.13*t-.10*t*t
  for k in range(segments):
   a=k*math.tau/segments;flute=1+.065*math.cos(a*11+phase)+.035*math.sin(a*17+phase)
   rr=taper*flute*(1+.014*math.sin(t*29+phase+a*2))
   z=2.005+t*height*(.91+.065*math.sin(a*3+phase)+.025*math.cos(a*7))
   vs.append((cx+rx*math.cos(a)*rr,cy+ry*math.sin(a)*rr,z))
 for j in range(levels):
  for k in range(segments):a=j*segments+k;b=j*segments+(k+1)%segments;fs.append((a,b,b+segments,a+segments))
 fs.append(tuple(reversed(range(segments))));fs.append(tuple(levels*segments+k for k in range(segments)))
 return mesh(n,vs,fs,stone)
massif('Terrain / west fluted massif',-.73,.13,.57,.67,.73,.3)
massif('Terrain / east fluted massif',.52,.35,.40,.48,.57,1.7)
# Actual continuous arch band, swept in the XZ plane, open below.
vs=[];fs=[];N=24
for i in range(N+1):
 a=math.pi*i/N
 for radius,y in [(.30,-.62),(.41,-.62),(.41,-.43),(.30,-.43)]:
  vs.append((.92+radius*math.cos(a),y,2.005+radius*math.sin(a)))
for i in range(N):
 for k in range(4):a=i*4+k;b=i*4+(k+1)%4;fs.append((a,b,b+4,a+4))
fs.extend([(3,2,1,0),tuple(N*4+k for k in range(4))]);mesh('Terrain / open sandstone arch',vs,fs,stone)
# Dark meandering inlay emphasizes negative space between the massifs.
vs=[];fs=[]
for i in range(33):
 y=-.88+i*1.70/32;x=-.09+.045*math.sin(y*4)
 vs.extend([(x-.055,y,2.008),(x+.055,y,2.008)])
for i in range(32):a=i*2;fs.append((a,a+1,a+3,a+2))
mesh('Terrain / siq shadow inlay',vs,fs,seam)
def disk(n,loc,r,depth,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold);mod=o.modifiers.new('Rounded brass','BEVEL');mod.width=.005;mod.segments=3;select(o);bpy.ops.object.modifier_apply(modifier=mod.name);return o
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035)
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(0,-1.282,.87),major_radius=.107,minor_radius=.008,rotation=(math.pi/2,0,0));bpy.context.object.name='Medallion / raised rim';bpy.context.object.data.materials.append(gold)
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for im in list(bpy.data.images):
 if im.users==0:bpy.data.images.remove(im)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.26
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.20))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'jordan.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'jordan.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('JORDAN AUTHORED')
