"""One-time scoped reuse of the proven Japan mechanism and viewer."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
B=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','THREE-LICENSE.txt','package.json','motion.mjs','build.py','verify_browser.py','verify_source.py','verify_parity.py','viewer.js','template.html']:
 if n.endswith(('.blend','.txt')): shutil.copyfile(B/n,R/n)
 else:
  s=(B/n).read_text(encoding='utf8').replace('japan-cedar-v1','bahamas-v1').replace('japan.glb','bahamas.glb').replace('japan.blend','bahamas.blend').replace('Japan / Cedar & Moss','Bahamas / Pink Sands & Blue Hole').replace('Japan Cedar and Moss','Bahamas Pink Sands and Blue Hole').replace('Yakushima cedar. Mossed granite. Quiet brass.','Pink shores. Turquoise shallows. Deep blue.').replace('inspired by the original Japan concept','inspired by Bahamian coastal landscapes').replace('JAPAN ·','BAHAMAS ·')
  (R/n).write_text(s,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n')
s=(B/'author.py').read_text()
# Retain small authoring helpers and hardware, replace the entire country form.
header=s[:s.index('wood=mat')]
helpers=s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
helpers=helpers[:helpers.index(' layer=')]+''' layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Mineral planar')
 for face in o.data.polygons:
  axis=max(range(3),key=lambda i:abs(face.normal[i]))
  axes=[i for i in range(3) if i!=axis]
  for li in face.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]*.8+.5,co[axes[1]]*.8+.5)
'''+helpers[helpers.index('def cube('):]
stone=s[s.index('def stone('):s.index("stone('Terrain / granite'")]
hardware=s[s.index('# Medallion is solid'):s.index('# Clean obsolete')]
finish=s[s.index('# Clean obsolete'):].replace('japan','bahamas').replace('JAPAN','BAHAMAS').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=4').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
body='''
wood=mat('Limestone / creamy shell grain',(.7,.59,.43),.72);maptex(wood,'limestone.png','Base Color');maptex(wood,'roughness.png','Roughness',True)
granite=wood
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / deep teal',(.018,.07,.068),.8)
sand=mat('Pink sand / shell flecks',(.75,.44,.39),.84);maptex(sand,'sand.png','Base Color')
water=mat('Lagoon / turquoise enamel',(.018,.38,.42),.20,.12)
deep=mat('Blue hole / deep cobalt',(.004,.035,.11),.22,.08)
transition=mat('Blue hole / submerged rim',(.015,.15,.24),.23,.1)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Limestone / wall',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.018)
for sx in [-1,1]:cube('Limestone / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.018)
cube('Limestone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Limestone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
cube('Lagoon / aquamarine inset',(0,0,1.991),(3.22,1.88,.024),water,lid,.008)
def bank(name,cx,cy,rx,ry):
 # Concentric irregular rings produce an actual raised bank, not a decal.
 N=64;verts=[];faces=[]
 for k in range(4):
  scale=[1,.92,.72,.32][k];z=[2.004,2.045,2.11,2.15][k]
  for i in range(N):
   a=math.tau*i/N;f=1+.075*math.sin(a*3)+.035*math.cos(a*7)
   verts.append((cx+rx*scale*f*math.cos(a),cy+ry*scale*f*math.sin(a),z+.008*math.sin(a*4)*k))
 for k in range(3):
  for i in range(N):
   a=k*N+i;b=k*N+(i+1)%N;faces.append((a,b,b+N,a+N))
 faces.append(tuple(range(3*N,4*N)))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(sand);uv(o);parent(o)
 return o
bank('Pink shore / long bank',-.72,-.22,.40,.61)
bank('Pink shore / northern cay',.30,.69,.65,.16)
def ring(name,r0,r1,z,material):
 N=80;vs=[];fs=[]
 if r0==0:
  vs=[(.55,.12,z)]+[(.55+r1*math.cos(i*math.tau/N),.12+r1*math.sin(i*math.tau/N),z) for i in range(N)]
  fs=[(0,i+1,(i+1)%N+1) for i in range(N)]
 else:
  vs=[(.55+r*math.cos(i*math.tau/N),.12+r*math.sin(i*math.tau/N),z) for r in [r0,r1] for i in range(N)]
  fs=[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(material);parent(o)
ring('Blue hole / rim',.30,.36,2.005,transition)
ring('Blue hole / deep center',0,.30,2.006,deep)
'''
(R/'author.py').write_text(header+helpers+body+stone+hardware+finish,encoding='utf8')
print('Scoped scaffold created')
