"""One-time scoped adaptation of the repository's Japan mechanical harness."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','viewer.js','THREE-LICENSE.txt','package.json','build.py','verify_source.py','verify_parity.py','verify_browser.py','template.html']:
 if n.endswith('.blend'):shutil.copyfile(S/n,R/n);continue
 t=(S/n).read_text(encoding='utf8').replace('japan-cedar-v1','republic-of-the-congo-v1').replace('japan.glb','congo.glb').replace('japan.blend','congo.blend')
 t=t.replace('Japan / Cedar & Moss','Republic of the Congo / Odzala Bai').replace('Yakushima cedar. Mossed granite. Quiet brass.','Forest canopy. A quiet wetland clearing. Warm brass.').replace('inspired by the original Japan concept','inspired by Odzala-Kokoua forest and wetland clearings').replace('JAPAN · 3D / 001','CONGO · 3D / 001')
 (R/n).write_text(t,encoding='utf8')
a=(S/'author.py').read_text(encoding='utf8')
a=a[:a.index('# Exterior skins')]+'''# Continuous umber exterior skins; no Japanese joinery attribution.
for sy in [-1,1]:cube('Forest body / long',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.035)
for sx in [-1,1]:cube('Forest body / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.035,axis='Y')
cube('Forest body / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.09),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.09),seam,bevel=.009)
 for sy in [-1,1]:cube('Forest / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
'''+a[a.index('# Restrained brass'):a.index("stone('Terrain / granite'")]+a[a.index('def tube('):a.index('trunk=[')]+'''# Low-relief forest wetland: irregular clearing, no photographic/map claim.
soil=mat('Bai / ochre silt',(.34,.255,.11),.93)
water=mat('Bai / reflective water',(.035,.13,.105),.19,.12)
# Solid shallow radial disks give the clearing an irregular shoreline.
def pool(n,rx,ry,z,material):
 verts=[(0,-.12,z)]; count=64
 for i in range(count):
  a=i*math.tau/count;k=1+.08*math.sin(a*3)+.04*math.cos(a*7)
  verts.append((math.cos(a)*rx*k,-.12+math.sin(a)*ry*k,z+.002*math.sin(a*5)))
 faces=[(0,i+1,(i+1)%count+1) for i in range(count)]
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);parent(o);return o
pool('Bai / clearing',1.39,.82,1.988,soil)
pool('Bai / water',.99,.52,1.997,water)
# Broadleaf forest islands at the clearing's sides and rear, leaving its center open.
for k,(x,y,h) in enumerate([(-1.19,.45,.42),(-.63,.79,.52),(.05,.88,.44),(.73,.72,.55),(1.25,.26,.40),(-1.30,-.39,.30),(1.28,-.45,.29)]):
 stone('Forest / root island '+str(k),(x,y,2.005),(.27,.24,.045),lid,moss,2)
 tube('Forest / trunk '+str(k),[(x,y,2.00),(x+.025,y,2.12),(x-.02,y+.015,2.0+h*.75)],[.038,.028,.015],bark,sides=8)
 for j in range(3):
  a=j*math.tau/3+k;tx=x+math.cos(a)*.15;ty=y+math.sin(a)*.12;tz=2+h-(j%2)*.06
  tube('Forest / branch '+str(k)+' '+str(j),[(x,y,2+h*.55),(tx,ty,tz-.05)],[.019,.007],bark,sides=7)
  stone('Forest / broadleaf crown '+str(k)+' '+str(j),(tx,ty,tz),(.23,.19,.105),lid,leafm[(j+k)%4],2)
# Sparse sedge patches emphasize the bai edge, not a lawn over the water.
for k in range(24):
 a=k*math.tau/24;x=1.17*math.cos(a);y=-.12+.65*math.sin(a)
 for j in range(3):
  tube('Bai / sedge',[(x+j*.012,y,1.995),(x+.015+j*.012,y+.012,2.035+random.random()*.04)],[.006,.0018],moss,sides=5)
'''+a[a.index('# Medallion'):]
a=a.replace('japan.blend','congo.blend').replace('japan.glb','congo.glb').replace('JAPAN AUTHORED','CONGO AUTHORED').replace('Reference-led Japan pilot','Odzala-inspired Republic of the Congo pilot').replace('Cedar / fine longitudinal grain','Forest / umber grain').replace('Cedar / dark finger endgrain','Forest / dark grain').replace('Cedar / furrowed bark','Forest / bark').replace('Cedar foliage / ','Forest canopy / ').replace('cedar-color.png','forest-color.png').replace('cedar-roughness.png','forest-roughness.png').replace('cedar-end.png','forest-end.png')
a=a.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z","u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z")
a=a.replace("[(.045,.10,.024),(.07,.14,.035),(.10,.18,.047),(.13,.21,.06)]","[(.025,.095,.045),(.04,.14,.063),(.065,.19,.075),(.11,.23,.09)]")
(R/'author.py').write_text(a,encoding='utf8')
print('Scoped author and harness adaptation created')
