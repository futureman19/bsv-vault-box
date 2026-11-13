from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for f in ['mechanism.blend','THREE-LICENSE.txt','package.json']:
 shutil.copyfile(S/f,R/f)
 if f=='package.json':
  p=R/f;p.write_text(p.read_text().replace('boxsv-japan-cedar-v1','boxsv-micronesia-v1'))
for f in ['build.py','viewer.js','template.html','motion.mjs','verify_source.py','verify_parity.py','verify_browser.py']:
 s=(S/f).read_text(encoding='utf8').replace('japan-cedar-v1','micronesia-v1').replace('japan.glb','micronesia.glb').replace('japan.blend','micronesia.blend').replace('Japan','Micronesia').replace('JAPAN','MICRONESIA').replace('Cedar & Moss','Basalt & Tidal Canals').replace('Yakushima cedar. Mossed granite. Quiet brass.','Pohnpei-inspired basalt. Tidal channels. Quiet brass.').replace('inspired by the original Micronesia concept','inspired by Pohnpei basalt and constructed lagoon islets; an invented arrangement, not a monument reconstruction')
 if f=='viewer.js':s=s.replace('Micronesia Cedar and Moss','Micronesia Basalt and Tidal Canals')
 if f=='verify_browser.py':
  s=s.replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1',timeout=3000);assert page.evaluate('pilot.progress')==1").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0',timeout=3000);assert page.evaluate('pilot.progress')==0")
 (R/f).write_text(s,encoding='utf8')
s=(S/'author.py').read_text(encoding='utf8')
# Retain well-tested helper and mechanical skin dimensions, replace art/materials entirely.
a=s[:s.index("wood=mat")]
a+='''wood=mat('Basalt / mineral grain',(.08,.12,.13),.7);maptex(wood,'basalt-color.png','Base Color');maptex(wood,'basalt-roughness.png','Roughness',True)
end=wood
granite=mat('Pale stone / coral limestone inspired',(.48,.52,.45),.82);maptex(granite,'pale-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / muted teal',(.025,.09,.08),.8)
water=mat('Tidal channels / teal inlay',(.018,.25,.24),.24,.12)
'''
a+=s[s.index('def uv('):s.index('# Exterior skins')]
a=a.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z\n   if axis=='Y' and abs(p.normal.z)>.7:v=co.x", "n=p.normal\n   if abs(n.z)>.7:u,v=co.x,co.y\n   elif abs(n.x)>.7:u,v=co.y,co.z\n   else:u,v=co.x,co.z").replace('u/3.72+.5,v/1.7+.5','u/1.6+.5,v/1.6+.5').replace('m.segments=3','m.segments=1')
a+='''# Real stone courses with staggered vertical joints, continuous liner behind.
for row in range(7):
 z=.10+(row+.5)*1.46/7;h=1.46/7-.009
 for sy in [-1,1]:
  cuts=[-1.86]+[x for x in [-1.2+(.30 if row%2 else 0),-.35+(.30 if row%2 else 0),.55+(.30 if row%2 else 0),1.32+(.18 if row%2 else 0)] if x<1.86]+[1.86]
  for j,(lo,hi) in enumerate(zip(cuts,cuts[1:])):cube('Basalt course / long %s %s %s'%(row,sy,j),((lo+hi)/2,sy*1.145,z),(hi-lo-.012,.19,h),wood,bevel=.015)
 for sx in [-1,1]:
  for j in range(3):cube('Basalt course / end %s %s %s'%(row,sx,j),(sx*1.745,-.69+j*.69,z),(.23,.678,h),wood,bevel=.015)
'''
a+=s[s.index('# Small collar'):s.index('# A thin satin')]
a+=s[s.index('# Restrained brass'):s.index("stone('Terrain / granite'")]
a+='''# Abstract constructed islets separated by a continuous connected water inlay.
cube('Lagoon / connected tidal inlay',(0,0,1.993),(3.18,1.82,.032),water,lid,.025)
platforms=[(-1.04,-.48,.72,.48),(-.08,-.48,.70,.48),(.94,-.48,.76,.48),(-1.02,.37,.76,.64),(.03,.39,.78,.66),(1.04,.39,.67,.60)]
for i,(x,y,w,d) in enumerate(platforms):
 cube('Islet / platform %02d'%i,(x,y,2.035),(w,d,.09),granite,lid,.035)
 # Small cut-stone edging adds genuine depth, not a copied map.
 for j in range(3):cube('Islet / edge %02d %02d'%(i,j),(x-w*.30+j*w*.30,y-d*.40,2.095),(w*.26,.055,.07),wood,lid,.009)
# A low OPEN enclosure evokes header/stretcher stonework, no funerary content.
x,y=-1.02,.37
for k in range(3):
 z=2.13+k*.095
 for sy in [-1,1]:cube('Basalt enclosure / long %s %s'%(k,sy),(x,y+sy*.205,z),(.64,.095,.082),wood,lid,.012)
 for sx in [-1,1]:cube('Basalt enclosure / end %s %s'%(k,sx),(x+sx*.27,y,z),(.095,.31,.082),wood,lid,.012)
# Smaller paired stone prisms on the far-right platform.
for j in range(3):cube('Basalt relief / prism '+str(j),(1.04,.21+j*.16,2.13),(.49,.10,.09),wood,lid,.012)
'''
a+=s[s.index('# Medallion'):]
a=a.replace('Cedar /','Basalt /').replace('Granite foot','Stone foot').replace('japan.blend','micronesia.blend').replace('japan.glb','micronesia.glb').replace('JAPAN AUTHORED','MICRONESIA AUTHORED')
a=a.replace("scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000", "scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=800")
(R/'author.py').write_text(a,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n',encoding='utf8')
print('SETUP PASS')
