"""Saint Lucia landscape miniature; script-authored, not surveyed terrain."""
import bpy,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(1161)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
exec((R/'helpers.py').read_text())
rock=mat('Volcanic stone / gray green',(.15,.19,.16),.8);maptex(rock,'stone-color.png','Base Color');maptex(rock,'stone-roughness.png','Roughness',True)
forest=mat('Forest / tropical slopes',(.08,.18,.05),.9);maptex(forest,'forest-color.png','Base Color')
exposed=mat('Weathered dacitic accents',(.19,.23,.17),.86)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
water=mat('Caribbean / polished teal',(.015,.15,.18),.23,.25)
seam=mat('Jade / narrow reveal',(.025,.06,.04),.85)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(rock if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Volcanic body / long',(0,sy*1.145,.83),(3.72,.19,1.46),rock,bevel=.025)
for sx in [-1,1]:cube('Volcanic body / side',(sx*1.745,0,.83),(.23,2.10,1.46),rock,bevel=.025)
cube('Volcanic body / clasp seat',(0,-1.255,1.36),(.56,.075,.47),rock,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Stone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),rock,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),water,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  stone('Volcanic foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),material=rock,sub=2)
# Connected coastal relief with explicitly asymmetric eroded peaks.
# A gridded height field makes a continuous saddle, not two unrooted cones.
vs=[(0,.15,2.198)];fs=[];rings=18;sides=96
for k in range(1,rings+1):
 r=k/rings
 for j in range(sides):
  a=j*math.tau/sides;shore=1+.035*math.sin(5*a)+.025*math.cos(9*a)
  x=1.34*r*math.cos(a)*shore;y=.15+.67*r*math.sin(a)*shore
  h=(.08+.14*math.exp(-((x/.95)**2+((y-.3)/.35)**2)))*(1-r**6)
  vs.append((x,y,1.977+h))
for j in range(sides):fs.append((0,1+j,1+(j+1)%sides))
for k in range(rings-1):
 for j in range(sides):
  a=1+k*sides+j;b=1+k*sides+(j+1)%sides;fs.extend([(a,a+sides,b+sides),(a,b+sides,b)])
me=bpy.data.meshes.new('Continuous coastal ridge');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Terrain / Piton Mitan inspired ridge',me);bpy.context.collection.objects.link(o);me.materials.append(forest);uv(o);parent(o)
# Closed radial ring meshes: broad vs narrow shoulder, slanted summit,
# irregular fluting, fully separated upper silhouettes above shared ridge.
def peak(name,cx,cy,rx,ry,h,phase):
 verts=[];faces=[];rings=15;sides=40;base=2.035
 for k in range(rings):
  t=k/rings;radius=(1-t)**.72
  for j in range(sides):
   a=j*math.tau/sides;flute=1+.09*math.sin(a*7+phase)+.04*math.sin(a*13+t*3)
   verts.append((cx+math.cos(a)*rx*radius*flute+t*.06,cy+math.sin(a)*ry*radius*flute,base+h*t+.015*math.sin(a*5)*math.sin(math.pi*t)))
 for k in range(rings-1):
  for j in range(sides):
   a=k*sides+j;b=k*sides+(j+1)%sides;faces.extend([(a,b,b+sides),(a,b+sides,a+sides)])
 top=len(verts);verts.append((cx+.06,cy,base+h))
 for j in range(sides):faces.append(((rings-1)*sides+j,(rings-1)*sides+(j+1)%sides,top))
 faces.append(tuple(reversed(range(sides))))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(forest);me.materials.append(exposed)
 for f in me.polygons:
  f.material_index=1 if f.center.z>2.2 and random.random()<.065 else 0
 uv(o);parent(o)
peak('Terrain / Gros Piton',-.62,.27,.58,.44,.90,.5)
peak('Terrain / Petit Piton',.58,.35,.39,.36,.82,1.8)
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035)
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(0,-1.282,.87),major_radius=.107,minor_radius=.008,rotation=(math.pi/2,0,0));bpy.context.object.name='Medallion / raised rim';bpy.context.object.data.materials.append(gold)
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.25))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.8
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=1000;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.use_nodes=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'saint-lucia.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'saint-lucia.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('SAINT LUCIA AUTHORED')
