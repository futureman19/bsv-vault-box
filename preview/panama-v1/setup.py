"""One-time scaffold from read-only mechanical pilot; never overwrites siblings."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','package.json']:
 shutil.copy2(S/name,R/name)
for name in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','motion.mjs','template.html']:
 s=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','panama-v1').replace('japan.glb','panama.glb').replace('japan.blend','panama.blend').replace('Japan / Cedar & Moss','Panama / Mangrove & Jade').replace('Japan Cedar and Moss','Panama Mangrove and Jade').replace('JAPAN','PANAMA').replace('Japan','Panama')
 s=s.replace('Yakushima cedar. Mossed granite. Quiet brass.','Darien tidal forest. Jade-toned mineral. Quiet brass.').replace('inspired by the original Panama concept','inspired by Darien coastal habitats')
 (R/name).write_text(s,encoding='utf8')
s=(S/'author.py').read_text()
s=s.replace('Reference-led Japan pilot','Brief-led Panama pilot').replace('japan.blend','panama.blend').replace('japan.glb','panama.glb').replace('JAPAN AUTHORED','PANAMA AUTHORED')
s=s.replace('Cedar / fine longitudinal grain','Jade / mottled mineral').replace('cedar-color.png','jade-color.png').replace('cedar-roughness.png','jade-roughness.png').replace('Cedar / dark finger endgrain','Sediment / dark matrix').replace('cedar-end.png','sediment.png').replace('Cedar / furrowed bark','Mangrove / brown bark').replace('Cedar foliage / ','Mangrove canopy / ')
a=s.index('def uv(');b=s.index('def cube(',a)
s=s[:a]+'''def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Physical mineral projection')
 for p in o.data.polygons:
  n=p.normal;major=max(range(3),key=lambda k:abs(n[k]));axes=[k for k in range(3) if k!=major]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co+o.location
   layer.data[li].uv=(co[axes[0]]*.6,co[axes[1]]*.6)
'''+s[b:]
a=s.index('# Exterior skins');b=s.index('# Small collar',a)
s=s[:a]+'''# Continuous mineral skins around the inherited hollow liner.
for sy in [-1,1]:cube('Jade / front' if sy<0 else 'Jade / rear',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.025)
for sx in [-1,1]:cube('Jade / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.025)
'''+s[b:]
s=s.replace('Cedar / clasp seat','Jade / clasp seat').replace('Cedar / rim corner','Jade / rim corner')
a=s.index('# A thin satin');b=s.index('# Restrained brass',a);s=s[:a]+s[b:]
a=s.index("stone('Terrain / granite'");b=s.index('def tube(',a);s=s[:a]+s[b:]
a=s.index('trunk=[');b=s.index('# Medallion',a)
s=s[:a]+'''# A continuous sinuous tidal inlet and two contiguous sediment banks.
water=mat('Tidal water / turquoise',(.025,.24,.23),.18,.12)
sand=mat('Sediment / warm silt',(.23,.18,.105),.86);maptex(sand,'sediment.png','Base Color')
def ribbon(n,side,material):
 verts=[];faces=[];N=40
 for i in range(N+1):
  x=-1.40+2.8*i/N;c=.22*math.sin(2.2*x)
  ys=(c-.14,c+.14) if side==0 else ((c+.14,.85) if side==1 else (-.85,c-.14))
  z=2.018 if side==0 else 2.042
  for y in ys:verts.append((x,y,z))
 for i in range(N):faces.append((2*i,2*i+2,2*i+3,2*i+1))
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o)
 return o
ribbon('Tide / continuous inlet',0,water)
ribbon('Bank / north',1,sand);ribbon('Bank / south',-1,sand)
# Three spreading stilt-root mangroves; leaf diamonds batched by palette.
vs=[[] for _ in leafm];fs=[[] for _ in leafm]
for ti,(x,y) in enumerate([(-.85,.57),(.10,-.55),(.95,.55)]):
 trunk=[(x,y,2.045),(x+.025,y,2.25),(x-.025,y+.015,2.49),(x+.015,y,2.67)]
 tube('Mangrove / trunk '+str(ti),trunk,[.046,.043,.029,.008],bark)
 for j in range(5):
  a=j*math.tau/5;rx=x+math.cos(a)*.18;ry=y+math.sin(a)*.15
  tube('Mangrove / stilt root '+str(ti)+' '+str(j),[(rx,ry,2.042),(x+math.cos(a)*.11,y+math.sin(a)*.09,2.18),trunk[1]],[.013,.018,.022],bark,sides=7)
 for j in range(10):
  az=j*2.399;rad=.23+random.random()*.12;start=Vector((x,y,2.40+j*.019));tip=start+Vector((math.cos(az)*rad,math.sin(az)*rad,.11))
  tube('Mangrove / branch',[start,start.lerp(tip,.5)+Vector((0,0,.05)),tip],[.014,.009,.002],bark,sides=7)
  for k in range(24):
   a=random.uniform(0,math.tau);r=random.random()**.5*.17;q=tip+Vector((math.cos(a)*r,math.sin(a)*r,random.uniform(-.04,.045)))
   ang=random.uniform(0,math.tau);d=Vector((math.cos(ang),math.sin(ang),.12));w=Vector((-math.sin(ang),math.cos(ang),0))*.033
   length=.085+random.random()*.035;mi=random.randrange(4);n=len(vs[mi]);mid=q+d*length*.5
   vs[mi].extend([q,mid+w,q+d*length,mid-w,mid+Vector((0,0,.008))]);fs[mi].extend([(n,n+1,n+4),(n+1,n+2,n+4),(n+2,n+3,n+4),(n+3,n,n+4)])
for i in range(4):
 me=bpy.data.meshes.new('Broadleaf canopy');me.from_pydata(vs[i],[],fs[i]);me.update();o=bpy.data.objects.new('Mangrove / foliage '+str(i),me);bpy.context.collection.objects.link(o);me.materials.append(leafm[i]);parent(o)
 for f in me.polygons:f.use_smooth=True
'''+s[b:]
s=s.replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=800')
(R/'author.py').write_text(s)
(R/'.gitattributes').write_text('* -text\n')
print('Scaffold created only under',R)
