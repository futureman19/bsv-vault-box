import bpy,math,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(98)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
# Load function definitions first, with foot material needed by default argument.
text=(R/'helpers.py').read_text();exec(text[:text.index('def uv(')])
granite=mat('Tufa / dark foot',(.4,.36,.27),.85);maptex(granite,'stone-foot.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
exec(text[text.index('def uv('):])
tufa=mat('Tufa / porous cream',(.62,.56,.4),.8);maptex(tufa,'tufa-color.png','Base Color');maptex(tufa,'tufa-roughness.png','Roughness',True)
water=mat('Water / turquoise inlay',(.033,.32,.29),.18,.15)
foam=mat('Water / pale cascade',(.23,.57,.49),.24)
moss=mat('Bank / olive moss',(.09,.16,.035),.95)
seam=mat('Mineral seam / dark olive',(.035,.06,.025),.9)
for o in list(bpy.data.objects):
 if o.type=='MESH' and not o.name.startswith(('Studio','Medallion','Side ring')):
  o.data.materials.clear();o.data.materials.append(tufa if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Continuous skins, butt joined without coplanar corner overlap.
for sy in [-1,1]:cube('Tufa / long wall',(0,sy*1.145,.83),(3.26,.19,1.46),tufa,bevel=.012)
for sx in [-1,1]:cube('Tufa / end wall',(sx*1.745,0,.83),(.23,2.48,1.46),tufa,bevel=.012)
cube('Tufa / clasp seat',(0,-1.255,1.36),(.56,.075,.47),tufa,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:
  cube('Tufa / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),tufa,bevel=.004)
  stone('Stone foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),tufa,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def pool(n,x,y,rx,ry,z,material,bottom):
 N=40;vs=[]
 for h in [bottom,z]:
  for j in range(N):
   a=j*math.tau/N;r=1+.045*math.sin(3*a)+.025*math.cos(5*a)
   vs.append((x+rx*r*math.cos(a),y+ry*r*math.sin(a),h))
 faces=[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(j,(j+1)%N,(j+1)%N+N,j+N) for j in range(N)]
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o);return o
for i,(x,y,z) in enumerate([(-.87,-.12,2.12),(0,.13,2.30),(.87,.22,2.48)]):
 pool('Terrace / '+str(i),x,y,.57,.67,z,tufa,1.965)
 pool('Lake / '+str(i),x,y,.48,.55,z+.008,water,z-.008)
 for k in range(5):
  a=(k/5)*math.pi+math.pi*.1
  stone('Bank moss / '+str(i),(x+math.cos(a)*.53,y+math.sin(a)*.61,z+.012),(.065,.048,.023),lid,moss,1)
# Continuous sloping ribbons link lake surfaces through the terrace edges.
for i,(x,y,z) in enumerate([(-.87,-.12,2.128),(0,.13,2.308)]):
 xx=x+.87; yy=[.13,.22][i]; zz=z+.18
 path=[(x+.18,y,z+.018),(xx-.64,yy,zz+.018),(xx-.38,yy,zz+.018)]
 verts=[(px,py+side*.075,pz) for px,py,pz in path for side in [-1,1]]
 me=bpy.data.meshes.new('Cascade');me.from_pydata(verts,[],[(0,2,3,1),(2,4,5,3)]);me.update();o=bpy.data.objects.new('Cascade / '+str(i),me);bpy.context.collection.objects.link(o);me.materials.append(foam);parent(o)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.7));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.8
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=1000;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.use_nodes=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'croatia.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'croatia.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('CROATIA AUTHOR PASS')
