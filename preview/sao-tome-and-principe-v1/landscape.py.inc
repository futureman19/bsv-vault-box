for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(granite if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Phonolite / body long',(0,sy*1.145,.83),(3.72,.19,1.46),granite,bevel=.025)
for sx in [-1,1]:cube('Phonolite / body side',(sx*1.745,0,.83),(.23,2.48,1.46),granite,bevel=.025)
cube('Phonolite / clasp seat',(0,-1.255,1.36),(.56,.075,.47),granite,bevel=.025)
for sy in [-1,1]:cube('Forest / seam long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Forest / seam side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Phonolite / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),granite,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),granite,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  stone('Phonolite foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
def mesh(n,v,f,m):
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(m);uv(o);parent(o);return o
# Irregular forest island: closed skirt seated into the stone lid.
N=64;v=[(0,0,2.16)];f=[]
for k in range(1,9):
 r=k/8
 for j in range(N):
  a=j*math.tau/N;edge=1+.07*math.sin(3*a)+.045*math.cos(5*a)
  x=1.34*r*math.cos(a)*edge;y=.72*r*math.sin(a)*edge
  z=1.98+.18*(1-r*r)+.018*math.sin(x*7)*math.sin(y*6)*(1-r)
  v.append((x,y,z))
for j in range(N):f.append((0,1+j,1+(j+1)%N))
for k in range(7):
 for j in range(N):
  a=1+k*N+j;b=1+k*N+(j+1)%N;f.append((a,a+N,b+N,b))
base=len(v)
for j in range(N):x,y,z=v[1+7*N+j];v.append((x,y,1.973))
for j in range(N):a=1+7*N+j;b=1+7*N+(j+1)%N;f.append((a,base+j,base+(j+1)%N,b))
f.append(tuple(reversed(range(base,base+N))))
terrain=mesh('Terrain / rainforest bed',v,f,forest)
for p in terrain.data.polygons:p.use_smooth=True
# Phonolitic needle: near-vertical irregular walls then rounded asymmetrical cap.
N=40;levels=[(2.09,.36),(2.23,.33),(2.42,.29),(2.63,.25),(2.85,.21),(3.02,.15),(3.12,.075)]
v=[];f=[]
for k,(z,r) in enumerate(levels):
 for j in range(N):
  a=j*math.tau/N;flute=1+.055*math.sin(9*a)+.045*math.cos(5*a+.4);cx=.4+.04*k/6;cy=.28+.035*math.sin(k/6*2)
  v.append((cx+r*flute*math.cos(a),cy+r*.86*flute*math.sin(a),z+.008*math.sin(3*a)))
for k in range(len(levels)-1):
 for j in range(N):a=k*N+j;b=k*N+(j+1)%N;f.append((a,b,b+N,a+N))
f.append(tuple(reversed(range(N))));v.append((.44,.31,3.145));top=len(v)-1
for j in range(N):f.append(((len(levels)-1)*N+j,(len(levels)-1)*N+(j+1)%N,top))
needle=mesh('Terrain / Pico Cao Grande inspired needle',v,f,granite)
for p in needle.data.polygons:p.use_smooth=True
# Distinct leafy canopy patches around the rock, each seated in terrain.
for i in range(54):
 a=i*2.399;r=.28+.58*((i%11)/10)**.5;x=1.20*r*math.cos(a);y=.64*r*math.sin(a)
 if ((x-.4)/.40)**2+((y-.28)/.36)**2<1:continue
 rr=((x/1.34)**2+(y/.72)**2)**.5;z=1.98+.18*(1-rr*rr)+.018*math.sin(x*7)*math.sin(y*6)*(1-rr)
 size=.10+.035*random.random()
 stone('Terrain / forest canopy', (x,y,z+.025),(size,size*.84,.08),lid,canopy[0 if x<-.3 else (1 if y<.1 else 2)],2)
