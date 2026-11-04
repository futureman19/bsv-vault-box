"""Prepare Denmark-specific author script from read-only pilot helpers."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
head=s[:s.index("wood=mat(")]
helpers=s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
stone=s[s.index('def stone('):s.index('for sx in [-1,1]:\n for sy in [-1,1]:stone')]
end=s[s.index('# Clean obsolete'):].replace('japan','denmark').replace('JAPAN','DENMARK').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=2;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=960').replace('resolution_y=1000','resolution_y=880')
material='''chalk=mat('Chalk / warm pale mineral',(.72,.70,.65),.82)
maptex(chalk,'chalk-color.png','Base Color');maptex(chalk,'chalk-roughness.png','Roughness',True)
flint=mat('Flint / charcoal',(.045,.052,.057),.55);maptex(flint,'flint-color.png','Base Color')
granite=flint
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
green=mat('Plateau / beech canopy abstraction',(.10,.19,.055),.91)
water=mat('Baltic / turquoise inset',(.025,.30,.34),.19,.15)
'''
body='''for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(chalk if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Chalk body / long',(0,sy*1.145,.83),(3.72,.19,1.46),chalk,bevel=.025)
for sx in [-1,1]:cube('Chalk body / end',(sx*1.745,0,.83),(.23,2.10,1.46),chalk,bevel=.025,axis='Y')
cube('Chalk / clasp seat',(0,-1.255,1.36),(.56,.075,.47),chalk,bevel=.025)
for sy in [-1,1]:cube('Flint seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),flint,bevel=.009)
for sx in [-1,1]:
 cube('Flint seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),flint,bevel=.009)
 for sy in [-1,1]:cube('Chalk / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),chalk,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),chalk,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
'''
land='''for sx in [-1,1]:
 for sy in [-1,1]:stone('Flint foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
cube('Baltic / water inset',(0,0,1.992),(2.85,1.65,.026),water,lid,.009)
# Irregular contiguous escarpment with a genuinely raised green plateau.
for k in range(3):
 x0=-1.36+k*.90;n=12;verts=[]
 for j in range(n+1):
  x=x0+.90*j/n;y=.10+.085*math.sin((j+k*12)*1.7);z=2.35+.14*math.sin((j+k*12)*.43)+.035*math.sin(j*2.7)
  verts.extend([(x,y,2.006),(x,y,z),(x,.77,z-.035),(x,.77,2.006)])
 faces=[]
 for j in range(n):
  a=4*j;b=a+4
  faces.extend([(a,b,b+1,a+1),(a+1,b+1,b+2,a+2),(a+2,b+2,b+3,a+3),(a+3,b+3,b,a)])
 faces.extend([(3,2,1,0),(4*n,4*n+1,4*n+2,4*n+3)])
 me=bpy.data.meshes.new('Chalk cliff');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Landscape / chalk cliff '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(chalk);me.materials.append(green)
 for i,p in enumerate(me.polygons):
  if i<n*4 and i%4==1:p.material_index=1
 uv(o);parent(o)
for j in range(24):
 x=-1.30+j*.112;y=-.025+.022*math.sin(j*2)
 stone('Landscape / flint shore',(x,y,2.02),(.061,.045,.025),lid,flint,1)
'''
(R/'author.py').write_text(head+material+helpers+body+stone+land+end,encoding='utf8')
