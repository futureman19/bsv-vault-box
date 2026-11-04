from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','motion.mjs']:
 shutil.copy2(S/name,R/name)
for name in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html','package.json']:
 s=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','oman-v1').replace('japan.glb','oman.glb').replace('japan.blend','oman.blend').replace('Japan','Oman').replace('JAPAN','OMAN').replace('Cedar & Moss','Aflaj & Limestone').replace('Cedar and Moss','Aflaj and Limestone').replace('Yakushima cedar. Mossed granite. Quiet brass.','Pale stone. Terraced gardens. A ribbon of water.').replace('inspired by the original Oman concept','inspired by Oman’s aflaj irrigation landscapes')
 if name=='template.html':s=s.replace('h1{font-siz... [truncated]','h1{font-size:30px}.foot{flex-direction:column}.folio{padding-top:8px}}')
 if name=='viewer.js':s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.4,7)').replace('target=target?0:1;open.textContent',"target=target?0:1;if(reduced.matches){progress=target;const p=pose(progress);lid.rotation.x=p.lid;latch.rotation.x=p.latch;window.pilot.progress=progress;window.pilot.lid=p.lid;window.pilot.latch=p.latch;}open.textContent").replace("controls.reset();open.textContent","controls.reset();const p=pose(0);lid.rotation.x=p.lid;latch.rotation.x=p.latch;window.pilot.progress=0;window.pilot.lid=0;window.pilot.latch=0;open.textContent")
 (R/name).write_text(s,encoding='utf8')
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
a=(S/'author.py').read_text(); prefix=a[:a.index("wood=mat")]; helpers=a[a.index('def uv'):a.index('for o in bpy.data.objects:')]; stone=a[a.index('def stone'):a.index("stone('Terrain")]; end=a[a.index('# Medallion'):]
materials="""wood=mat('Limestone / warm pale mineral',(.52,.41,.26),.78);maptex(wood,'stone-color.png','Base Color');maptex(wood,'stone-roughness.png','Roughness',True)
granite=mat('Limestone / foot',(.27,.22,.15),.8);maptex(granite,'foot-color.png','Base Color')
gold=mat('Bronze / satin',(.48,.30,.10),.3,.8)
seam=mat('Mineral seam / dark olive',(.05,.065,.025),.9)
garden=mat('Garden / olive green',(.16,.23,.055),.95)
water=mat('Falaj / turquoise inlay',(.035,.30,.29),.19,.15)
"""
body="""for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Limestone / long skin',(0,sy*1.145,.83),(3.26,.19,1.46),wood,bevel=.014)
for sx in [-1,1]:cube('Limestone / side skin',(sx*1.745,0,.83),(.23,2.48,1.46),wood,bevel=.014)
cube('Limestone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Limestone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# Raised terraced garden beds; central channel remains continuously exposed.
for sx in [-1,1]:
 for j in range(3):
  top=2.10+j*.12;y=-.57+j*.57
  cube('Terrace / stone '+str(sx)+' '+str(j),(sx*.70,y,(1.978+top)/2),(1.10,.52,top-1.978),wood,lid,.012)
  cube('Terrace / garden '+str(sx)+' '+str(j),(sx*.70,y,top+.009),(.92,.36,.018),garden,lid,.005)
cube('Falaj / continuous water',(0,0,1.995),(.16,1.70,.026),water,lid,.006)
for sx in [-1,1]:cube('Falaj / coping',(sx*.115,0,2.014),(.055,1.74,.072),wood,lid,.006)
"""
a=prefix+materials+helpers+body+stone+end
a=a.replace('japan.blend','oman.blend').replace('japan.glb','oman.glb').replace('JAPAN AUTHORED','OMAN AUTHORED').replace('Reference-led Japan pilot','Brief-led Oman pilot').replace('location=(-5.6,-7.8,4.5)','location=(-5.6,-7.8,6.5)').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
# Replace wood-oriented UV projection with face-dominant stone projection.
start=a.index("   u=co.y");stop=a.index('\ndef cube',start)
a=a[:start]+"   axes=(co.x,co.y) if abs(p.normal.z)>.7 else ((co.y,co.z) if abs(p.normal.x)>.7 else (co.x,co.z))\n   layer.data[li].uv=(axes[0]/2,axes[1]/2)\n"+a[stop:]
(R/'author.py').write_text(a)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
print('Prepared Oman-only authoring and verification scripts')
