from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','package.json','motion.mjs','tests.mjs','viewer.js','template.html','build.py','verify_source.py','verify_parity.py','verify_browser.py','maps.py','author.py']:
 p=S/name
 if not p.exists():continue
 if p.suffix=='.blend':shutil.copy2(p,R/name);continue
 s=p.read_text(encoding='utf8').replace('japan-cedar-v1','liberia-v1').replace('japan.glb','liberia.glb').replace('japan.blend','liberia.blend').replace('Japan / Cedar & Moss','Liberia / Sapo Rainforest & River').replace('Yakushima cedar. Mossed granite. Quiet brass.','Upper Guinean forest. Winding water. Warm brass.').replace('the original Japan concept','Liberia’s Sapo rainforest landscape').replace('JAPAN','LIBERIA').replace('Cedar','Timber').replace('cedar','timber')
 (R/name).write_text(s,encoding='utf8')
s=(R/'maps.py').read_text().replace('167*v,87*v,46*v','112*v,66*v,36*v');(R/'maps.py').write_text(s)
s=(R/'author.py').read_text();start=s.index("stone('Terrain / granite'");end=s.index('def tube(',start);s=s[:start]+s[end:]
start=s.index('trunk=[');end=s.index('# Medallion',start)
s=s[:start]+'''# Liberia-specific lowland canopy and winding water, all on the lid.
forest=mat('Forest floor / deep green',(.035,.085,.038),.9)
water=mat('River / dark turquoise',(.025,.20,.19),.20,.15)
cube('Terrain / inset forest',(0,0,1.995),(3.10,1.90,.025),forest,lid,.008)
# Continuous broad ribbon, gently curved in plan, explicitly closed-sided.
verts=[];faces=[]
for j in range(33):
 y=-.88+j*1.76/32;x=.19*math.sin(j/32*math.tau)+.10
 verts.extend([(x-.10,y,2.016),(x+.10,y,2.016),(x-.10,y,2.009),(x+.10,y,2.009)])
for j in range(32):
 a=j*4;b=a+4
 faces.extend([(a,a+1,b+1,b),(a+2,b+2,b+3,a+3),(a,b,b+2,a+2),(a+1,a+3,b+3,b+1)])
faces.extend([(0,2,3,1),(128,129,131,130)])
me=bpy.data.meshes.new('Sinuous water');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('River / continuous ribbon',me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o)
for k,(x,y,h) in enumerate([(-.87,.47,.60),(.86,.48,.72),(-.83,-.46,.46)]):
 tube('Broadleaf / trunk '+str(k),[(x,y,2.012),(x+.035,y,2.18),(x-.025,y,2.01+h)],[.065,.045,.018],bark)
 for j in range(5):
  a=j*math.tau/5+.3*k;tx=x+math.cos(a)*.23;ty=y+math.sin(a)*.20;z=2.01+h-.06+random.uniform(-.055,.055)
  tube('Broadleaf / branch',[(x+.015,y,2.20),(tx,ty,z)],[.025,.008],bark,sides=7)
  stone('Broadleaf / crown',(tx,ty,z),(.27,.23,.095),lid,leafm[(j+k)%4],2)
 for j in range(4):
  a=j*math.tau/4;tube('Broadleaf / buttress',[(x+math.cos(a)*.15,y+math.sin(a)*.15,2.013),(x,y,2.20)],[.022,.028],bark,sides=7)
''' +s[end:]
(R/'author.py').write_text(s,encoding='utf8')
print('Prepared Liberia-specific sources; original previews untouched')
