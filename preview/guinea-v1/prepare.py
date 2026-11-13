"""Seed a new country authoring pipeline from read-only mechanical templates."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','package.json','motion.mjs']:
 shutil.copyfile(S/name,R/name)
for name in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','template.html','viewer.js']:
 text=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','guinea-v1').replace('japan.glb','guinea.glb').replace('japan.blend','guinea.blend').replace('Japan','Guinea').replace('JAPAN','GUINEA').replace('Cedar & Moss','Nimba highland').replace('Cedar / Moss','Nimba highland')
 (R/name).write_text(text,encoding='utf8')
s=(S/'author.py').read_text()
s=s[:s.index('# Exterior skins')]+'''# Continuous mineral skins, distinct from the cedar finger-joint precedent.
for sy in [-1,1]:
 cube('Earth / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.025)
for sx in [-1,1]:
 cube('Earth / end wall',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.025,axis='Y')
'''+s[s.index('# Small collar'):s.index('# A thin satin upper')]+s[s.index('# Restrained brass'):s.index("stone('Terrain / granite'")]+'''# Elongated asymmetric closed triangular terrain with three unequal peaks.
def height(x,y):
 peaks=[(-.78,-.02,.51,.30),(.05,.12,.68,.29),(.78,-.06,.43,.25)]
 return 1.982+max(h*math.exp(-((x-px)/w)**2-((y-py)/.25)**2) for px,py,h,w in peaks)
nx,ny=48,20;verts=[];faces=[]
for j in range(ny+1):
 for i in range(nx+1):
  x=-1.23+i*2.46/nx;y=-.48+j*.96/ny
  verts.append((x,y,height(x,y)))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.extend([(a,a+1,a+nx+2),(a,a+nx+2,a+nx+1)])
me=bpy.data.meshes.new('Nimba ridge grid');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / Nimba ridge',me);bpy.context.collection.objects.link(o);me.materials.append(moss);me.materials.append(leafm[2]);me.materials.append(granite)
for f in me.polygons:
 f.material_index=1 if f.center.z>2.20 else (2 if random.random()<.17 else 0)
parent(o);uv(o)
# Low clustered forest relief on lower flanks, deliberately not individual surveyed trees.
for i in range(42):
 x=random.uniform(-1.12,1.12);y=random.choice([-1,1])*random.uniform(.26,.43);z=height(x,y)+.015
 stone('Terrain / forest cluster',(x,y,z),(.07+random.random()*.04,.055,.045+random.random()*.025),lid,leafm[i%2],2)
'''+s[s.index('# Medallion'):]
s=s.replace('japan.blend','guinea.blend').replace('japan.glb','guinea.glb').replace('JAPAN AUTHORED','GUINEA AUTHORED')
s=s.replace('Cedar / fine longitudinal grain','Ferruginous earth / fine mineral mottling').replace('Cedar / dark finger endgrain','Earth / dark cut face').replace('cedar-color.png','earth-color.png').replace('cedar-roughness.png','earth-roughness.png').replace('cedar-end.png','earth-dark.png').replace('Granite / salt and pepper','Nimba / exposed rock').replace('Cedar /','Earth /').replace('Cedar foliage /','Highland foliage /')
s=s.replace("(.095,.16,.035)","(.10,.145,.029)")
s=s.replace('Reference-led Japan pilot.','Guinea Nimba highland pilot.').replace('scene.cycles.samples=32','scene.cycles.samples=24')
(R/'author.py').write_text(s)
print('Pipeline seeded; read-only templates preserved')
