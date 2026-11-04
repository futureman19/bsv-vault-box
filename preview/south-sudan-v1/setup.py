from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','package.json','THREE-LICENSE.txt']:
 shutil.copy2(S/n,R/n)
for n in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html']:
 s=(S/n).read_text().replace('japan-cedar-v1','south-sudan-v1').replace('japan.blend','south-sudan.blend').replace('japan.glb','south-sudan.glb').replace('Japan / Cedar & Moss','South Sudan / Sudd & Papyrus').replace('Japan Cedar and Moss','South Sudan Sudd and Papyrus').replace('Yakushima cedar. Mossed granite. Quiet brass.','Sudd waterways. Papyrus umbrellas. Silt and satin brass.').replace('inspired by the original Japan concept','inspired by the Sudd wetland landscape').replace('JAPAN ·','SOUTH SUDAN ·')
 if n=='viewer.js':s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.4,7)')
 if n=='verify_browser.py':s=s.replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1');assert page.evaluate('pilot.progress')==1").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0');assert page.evaluate('pilot.progress')==0")
 (R/n).write_text(s)
s=(S/'author.py').read_text();s=s[:s.index("stone('Terrain / granite'")]+s[s.index('def tube('):s.index('trunk=[')]+'''# Wetland is an invented miniature, not a map.
water=mat('Sudd / blue green water',(.035,.22,.23),.22,.15)
bank=mat('Sudd / floating vegetation',(.17,.25,.045),.9)
reed=mat('Papyrus / green stems',(.19,.28,.055),.8)
waterbed=cube('Wetland / water',(0,0,2.005),(3.22,1.82,.045),water,lid,.02)
centres=[(-.95,-.36),(.15,.4),(1.03,-.25)]
for k,(cx,cy) in enumerate(centres):
 stone('Wetland / bank '+str(k),(cx,cy,2.04),(.48,.32,.085),lid,bank,2)
 for j in range(7):
  a=j*2.399;x=cx+math.cos(a)*.20;y=cy+math.sin(a)*.13;z=2.09;h=.25+.07*((j+k)%4)
  tube('Papyrus / stem',[(x,y,z),(x+.015,y,z+h)],[.012,.007],reed,sides=6)
  for q in range(8):
   ang=q*math.tau/8
   tube('Papyrus / umbrella',[(x+.015,y,z+h),(x+.015+.105*math.cos(ang),y+.105*math.sin(ang),z+h-.045)],[.006,.002],reed,sides=5)
''' + s[s.index('# Medallion is solid'):]
s=s.replace('japan.blend','south-sudan.blend').replace('japan.glb','south-sudan.glb').replace("print('JAPAN AUTHORED')","print('SOUTH SUDAN AUTHORED')")
s=s.replace("(.4,.18,.08)","(.4,.30,.12)").replace('Cedar / fine longitudinal grain','Silt / reed-fibre surface').replace('Cedar / dark finger endgrain','Silt / dark edges').replace('Cedar / furrowed bark','Earth / dark ochre').replace('Cedar /','Silt /').replace('Cedar /','Silt /')
s=s.replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=4;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820').replace('location=(-5.6,-7.8,4.5)','location=(-5.6,-7.8,6.7)')
(R/'author.py').write_text(s)
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
(R/'.gitattributes').write_text('* -text\n')
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
