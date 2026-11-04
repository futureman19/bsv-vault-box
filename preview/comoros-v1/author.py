"""Comoros: procedural original theme over inherited articulated mechanism."""
import bpy, math, random
from mathutils import Vector
from pathlib import Path
R=Path(__file__).resolve().parent;random.seed(773)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
h=(R/'helpers.py').read_text();exec(h[:h.index('def stone(')])
granite=mat('Basalt / volcanic charcoal',(.034,.047,.045),.8)
maptex(granite,'basalt-color.png','Base Color');maptex(granite,'basalt-roughness.png','Roughness',True)
t=granite.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/basalt-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=granite.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.3;granite.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);granite.node_tree.links.new(n.outputs['Normal'],granite.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
green=mat('Vegetation / muted island green',(.06,.105,.035),.9)
yellow=mat('Ylang / warm yellow',(.71,.55,.14),.58)
seam=mat('Ocean / turquoise reveal',(.04,.20,.22),.35)
exec(h[h.index('def stone('):])
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(granite if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Basalt / front' if sy<0 else 'Basalt / rear',(0,sy*1.145,.83),(3.72,.19,1.46),granite,bevel=.035)
for sx in [-1,1]:cube('Basalt / side',(sx*1.745,0,.83),(.23,2.10,1.46),granite,bevel=.035)
cube('Basalt / clasp seat',(0,-1.255,1.36),(.56,.075,.47),granite,bevel=.025)
for sy in [-1,1]:cube('Ocean seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.08),seam,bevel=.009)
for sx in [-1,1]:
 cube('Ocean seam / side',(sx*1.74,0,1.618),(.16,2.05,.08),seam,bevel=.009)
 for sy in [-1,1]:cube('Basalt / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),granite,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),granite,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  stone('Basalt foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
# Radial relief: depressed crater centre, irregular raised rim, broad shield flanks.
# Closed bottom is within the lid; not a disconnected display pedestal.
verts=[(.25,.12,2.095)];faces=[];N=72
for k in range(1,13):
 r=k/12
 for j in range(N):
  a=j*math.tau/N;ir=1+.035*math.sin(a*5)+.025*math.cos(a*9)
  z=2.00+.40*math.exp(-((r-.37)/.20)**2)+.035*math.sin(a*3)*math.sin(math.pi*r)
  if k==12:z=1.99
  verts.append((.25+1.13*r*math.cos(a)*ir,.12+.78*r*math.sin(a)*ir,z))
for j in range(N):faces.append((0,1+j,1+(j+1)%N))
for k in range(11):
 for j in range(N):
  a=1+k*N+j;b=1+k*N+(j+1)%N;faces.append((a,a+N,b+N,b))
me=bpy.data.meshes.new('Karthala shield radial mesh');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Karthala / recessed crater',me);bpy.context.collection.objects.link(o);me.materials.append(granite);uv(o);parent(o)
for p in me.polygons:p.use_smooth=True
# Irregular green lowland patches follow lower flanks; all are lid children.
for i in range(26):
 a=i*2.399;r=.84+random.uniform(-.06,.10);x=.25+1.13*r*math.cos(a);y=.12+.78*r*math.sin(a)
 stone('Vegetation / lowland',(x,y,2.035),(.12,.075,.045),lid,green,2)
# Stylized six narrow curling petals, rather than claiming botanical scans.
for f,(cx,cy) in enumerate([(-.96,-.55),(-.75,.53),(1.12,-.37)]):
 stone('Ylang / centre '+str(f),(cx,cy,2.045),(.055,.055,.033),lid,gold,2)
 for j in range(6):
  a=j*math.tau/6+f*.4;v=[]
  for k in range(9):
   t=k/8;length=.32;w=.045*math.sin(math.pi*t)+.004
   for side in [-1,1]:
    xx=length*t;yy=side*w+.045*math.sin(math.pi*t)
    v.append((cx+math.cos(a)*xx-math.sin(a)*yy,cy+math.sin(a)*xx+math.cos(a)*yy,2.045+.065*math.sin(math.pi*t)+.012*t))
  fs=[(2*k,2*k+1,2*k+3,2*k+2) for k in range(8)]
  m=bpy.data.meshes.new('Petal ribbon');m.from_pydata(v,[],fs);m.update();p=bpy.data.objects.new('Ylang / petal '+str(f)+' '+str(j),m);bpy.context.collection.objects.link(p);m.materials.append(yellow);parent(p)
exec((R/'hardware.inc').read_text())
exec((R/'studio.inc').read_text())
