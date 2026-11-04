"""Original Bandiagara-inspired miniature; inherited articulated hardware only."""
import bpy,sys,math,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R))
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
from helpers import *
random.seed(516)
latch=bpy.data.objects['Latch_Pivot']
earth=mat('Ochre / porous sandstone',(.5,.27,.11),.8);maptex(earth,'ochre-color.png','Base Color');maptex(earth,'ochre-roughness.png','Roughness',True)
dark=mat('Earth / recessed strata',(.24,.12,.05),.9);maptex(dark,'earth-dark.png','Base Color')
gold=mat('Bronze / warm satin',(.38,.23,.085),.34,.8)
seam=mat('Seam / dark earth',(.045,.025,.012),.9)
# Physical-scale projection across all three axes, rather than wood grain UVs.
def stone_uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Mineral projection')
 for p in o.data.polygons:
  axis=max(range(3),key=lambda i:abs(p.normal[i]));axes=[i for i in range(3) if i!=axis]
  for li in p.loop_indices:
   co=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]*.6,co[axes[1]]*.6)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(dark if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):stone_uv(o)
for sy in [-1,1]:cube('Sandstone / wall',(0,sy*1.145,.83),(3.72,.19,1.46),earth,bevel=.025)
for sx in [-1,1]:cube('Sandstone / side',(sx*1.745,0,.83),(.23,2.10,1.46),earth,bevel=.025)
cube('Sandstone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),earth,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Sandstone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),earth,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),earth,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Sandstone / foot',(sx*1.47,sy*.91,-.10),(.54,.46,.31),dark,bevel=.06)
# One closed, terraced rock mass. Three uneven shoulders and two deep gullies.
N=96;M=24;verts=[];faces=[]
for j in range(M+1):
 v=j/M
 for i in range(N+1):
  x=-1.40+2.8*i/N
  front=.10+.055*math.sin(x*8)+.035*math.sin(x*19)
  back=.99+.035*math.sin(x*9)
  y=front+(back-front)*v
  shoulders=.48+.15*math.exp(-((x+.95)/.25)**4)+.26*math.exp(-((x-.02)/.32)**4)+.08*math.exp(-((x-.98)/.22)**4)
  gullies=.21*math.exp(-((x+.50)/.09)**2)+.25*math.exp(-((x-.61)/.11)**2)
  envelope=min(1,max(0,(1.4-abs(x))/.15))
  # Front ledges ascend in four unequal benches; rear slope roots into lid.
  terrace=[.10,.32,.62,.86,1][min(4,int(v*8))] if v<.63 else max(.06,1-(v-.63)*2.4)
  z=1.995+envelope*((shoulders-gullies)*terrace+.012*math.sin(x*31+y*17))
  verts.append((x,y,z))
for j in range(M):
 for i in range(N):
  a=j*(N+1)+i;faces.append((a,a+1,a+N+2,a+N+1))
# Close perimeter down to lid; skirt intentionally seats 0.008 inside lid.
bound=list(range(N+1))+[j*(N+1)+N for j in range(1,M+1)]+[M*(N+1)+i for i in range(N-1,-1,-1)]+[j*(N+1) for j in range(M-1,0,-1)]
bottom=[]
for k in bound:bottom.append(len(verts));verts.append((verts[k][0],verts[k][1],1.970))
for k in range(len(bound)):
 q=(k+1)%len(bound);faces.append((bound[q],bound[k],bottom[k],bottom[q]))
faces.append(tuple(reversed(bottom)))
me=bpy.data.meshes.new('Eroded terraced escarpment');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / Bandiagara escarpment',me);bpy.context.collection.objects.link(o);me.materials.append(earth);parent(o)
for ob in bpy.data.objects:
 if ob.type=='MESH' and any(m==earth or m==dark for m in ob.data.materials):stone_uv(ob)
# Family side-ring, carried by a real mount on the static left wall.
bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.085,depth=.035,location=(-1.875,0,1.05),rotation=(0,math.pi/2,0));mount=bpy.context.object;mount.name='Side ring / mount';mount.data.materials.append(gold)
bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=10,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging bronze';bpy.context.object.data.materials.append(gold)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for im in list(bpy.data.images):
 if im.users==0:bpy.data.images.remove(im)
for ob in bpy.data.objects:
 if ob.name=='Studio / shadow floor':ob.location.z=-.28
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.7));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.2))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.9
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=1000;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'mali.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in bpy.data.objects:
 if not ob.name.startswith('Studio') and ob.type in ['MESH','EMPTY']:ob.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'mali.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('MALI AUTHORED')
