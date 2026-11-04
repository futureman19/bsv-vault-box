"""Mexico v1: original ceramic tiles and agave sculpture on inherited mechanism."""
import bpy,sys,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R));random.seed(1462)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
from helpers import *
latch=bpy.data.objects['Latch_Pivot']
ceramic=mat('Ceramic / cobalt floral glaze',(.7,.65,.5),.4);maptex(ceramic,'ceramic-color.png','Base Color');maptex(ceramic,'ceramic-roughness.png','Roughness',True)
clay=mat('Terracotta / fired earth',(.36,.12,.055),.72);maptex(clay,'terracotta-color.png','Base Color')
gold=mat('Brass / satin fittings',(.48,.30,.10),.28,.8)
grout=mat('Grout / dark cobalt',(.018,.032,.065),.9)
rock=mat('Volcanic feet / charcoal',(.055,.046,.041),.88)
leaves=[mat('Agave / blue green '+str(i),c,.48) for i,c in enumerate([(.075,.24,.23),(.12,.32,.30),(.18,.38,.35)])]
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(clay if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Real separated ceramic skins, each tile has a whole original floral repeat.
for sy in [-1,1]:
 cube('Grout / front rear bed',(0,sy*1.125,.83),(3.72,.21,1.46),grout,bevel=.01)
 for row in range(3):
  for col in range(8):cube('Ceramic tile / front rear',(-1.86+(col+.5)*3.72/8,sy*1.218,.1+(row+.5)*1.46/3),(3.72/8-.014,.044,1.46/3-.014),ceramic,bevel=.005)
for sx in [-1,1]:
 cube('Grout / side bed',(sx*1.735,0,.83),(.23,2.38,1.46),grout,bevel=.01)
 for row in range(3):
  for col in range(5):cube('Ceramic tile / side',(sx*1.858,-1.19+(col+.5)*2.38/5,.1+(row+.5)*1.46/3),(.02,2.38/5-.014,1.46/3-.014),ceramic,bevel=.004)
cube('Terracotta / clasp seat',(0,-1.255,1.36),(.56,.075,.47),clay,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),grout,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),grout,bevel=.009)
 for sy in [-1,1]:cube('Terracotta / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),clay,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),clay,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  stone('Volcanic foot',(sx*1.47,sy*.91,-.1),(.32,.27,.19),material=rock,sub=2)
# Tile-bordered lid; center is a warm clay island, no cloned old terrain.
for row in range(4):
 for col in range(7):
  if row in (0,3) or col in (0,6):cube('Lid ceramic / border',(-1.5+col*.5,-.75+row*.5,1.986),(.486,.486,.026),ceramic,lid,.005)
stone('Agave / soil island',(.25,.22,1.995),(.85,.63,.12),lid,clay,sub=3)
# Thick tapered diamond-section lance leaves. Inner spear ring rises above outer ring.
root=Vector((.25,.22,2.10))
for j in range(24):
 ring=j//8;az=(j%8)*math.tau/8+ring*.29
 length=[.72,.53,.28][ring];height=[.32,.58,.84][ring];width=[.085,.075,.055][ring]
 radial=Vector((math.cos(az),math.sin(az),0));side=Vector((-math.sin(az),math.cos(az),0));verts=[];faces=[]
 for k in range(7):
  t=k/7;center=root+radial*(.035+length*t**1.25)+Vector((0,0,height*(t*.85+.15*math.sin(t*math.pi/2))))
  w=width*(.42+.75*math.sin(math.pi*t))*(1-t*.65);thick=.018*(1-.7*t)
  verts.extend([center-side*w,center+Vector((0,0,thick)),center+side*w,center-Vector((0,0,thick))])
 for k in range(6):
  for q in range(4):faces.append((k*4+q,k*4+(q+1)%4,(k+1)*4+(q+1)%4,(k+1)*4+q))
 faces.append((3,2,1,0));tip=len(verts);verts.append(root+radial*(.035+length)+Vector((0,0,height)))
 for q in range(4):faces.append((24+q,24+(q+1)%4,tip))
 me=bpy.data.meshes.new('Ridged taper');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Agave / leaf %02d'%j,me);bpy.context.collection.objects.link(o);me.materials.append(leaves[j%3]);parent(o)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,4.9));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'mexico.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'mexico.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('MEXICO AUTHORED')
