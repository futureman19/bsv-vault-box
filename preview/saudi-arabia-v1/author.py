"""Saudi Arabia / AlUla Sandstone. Original procedural landscape interpretation."""
import bpy,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(1293)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
exec((R/'helpers.py').read_text())
sand=mat('Sandstone / ochre sediment',(.55,.29,.13),.8);maptex(sand,'sandstone-color.png','Base Color');maptex(sand,'sandstone-roughness.png','Roughness',True)
granite=mat('Sandstone / dark feet',(.30,.16,.09),.87);maptex(granite,'sandstone-dark.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / dark bronze',(.075,.047,.028),.8)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(sand if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Sandstone / wall',(0,sy*1.145,.83),(3.72,.19,1.46),sand,bevel=.025)
for sx in [-1,1]:cube('Sandstone / end wall',(sx*1.745,0,.83),(.23,2.10,1.46),sand,bevel=.025)
cube('Sandstone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),sand,bevel=.025)
for sy in [-1,1]:cube('Bronze seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Bronze seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Sandstone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),sand,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),sand,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
exec((R/'stone-helper.py').read_text())
# Ring-built eroded monoliths: coarsely rounded tops, varying ledges, seated bottoms.
for k,(cx,cy,rx,ry,h) in enumerate([(-.95,.30,.43,.35,.68),(.12,.54,.40,.33,.95),(.98,.16,.36,.32,.53)]):
 vs=[];fs=[];N=40;L=16
 for j in range(L):
  t=j/(L-1);profile=(1-.12*t)*(1-.34*max(0,(t-.7)/.3)**2)
  ledge=1+.055*math.sin(t*37+k)+.035*math.sin(t*73)
  for i in range(N):
   a=i*math.tau/N;r=profile*ledge*(1+.09*math.sin(a*3+k)+.035*math.sin(a*7+t*4))
   z=1.97+h*t+(.024*math.sin(a*3+k)*math.sin(t*math.pi/2))
   vs.append((cx+rx*r*math.cos(a)+.045*t*t,cy+ry*r*math.sin(a),z))
 for j in range(L-1):
  for i in range(N):a=j*N+i;b=j*N+(i+1)%N;fs.append((a,b,b+N,a+N))
 fs.append(tuple(reversed(range(N))));fs.append(tuple((L-1)*N+i for i in range(N)))
 me=bpy.data.meshes.new('Eroded strata');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('AlUla / outcrop '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(sand);uv(o);parent(o)
 for f in me.polygons:f.use_smooth=len(f.vertices)==4
# Low sand islands ground each outcrop; no tray.
for k,(x,y,sx,sy) in enumerate([(-.95,.30,.55,.45),(.12,.54,.52,.44),(.98,.16,.48,.42)]):
 stone('AlUla / sand apron '+str(k),(x,y,1.977),(sx,sy,.026),lid,sand,2)
exec((R/'hardware-helper.py').read_text())
exec((R/'finish-helper.py').read_text())
