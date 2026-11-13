from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; J=R.parent/'japan-cedar-v1'
for f in ['mechanism.blend','THREE-LICENSE.txt','motion.mjs']:
 shutil.copyfile(J/f,R/f)
for f in ['verify_source.py','verify_parity.py','build.py','verify_browser.py','viewer.js','template.html','package.json']:
 s=(J/f).read_text(encoding='utf8').replace('japan-cedar-v1','sri-lanka-v1').replace('japan.blend','sri-lanka.blend').replace('japan.glb','sri-lanka.glb').replace('Japan / Cedar & Moss','Sri Lanka / Dumbara Weave').replace('Japan Cedar and Moss','Sri Lanka Dumbara Weave').replace('Yakushima cedar. Mossed granite. Quiet brass.','Ivory fibre. Geometric rhythm. Warm brass.').replace('inspired by the original Japan concept','inspired by Sri Lankan Dumbara weaving; invented geometric motifs, not artisan-made traditional work').replace('JAPAN ·','SRI LANKA ·')
 if f=='viewer.js':s=s.replace('(-5,3.7,7)','(-5,5.2,7)')
 if f=='verify_browser.py':s=s.replace("page.wait_for_timeout(70);assert", "page.wait_for_function('pilot.progress===1');assert").replace("page.wait_for_timeout(60);assert", "page.wait_for_function('pilot.progress===0');assert")
 (R/f).write_text(s,encoding='utf8')
shutil.copyfile(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
s=(J/'author.py').read_text()
s=s[:s.index('trunk=[')]+s[s.index('# Medallion'):]
s=s[:s.index("stone('Terrain / granite'")]+s[s.index('def tube('):]
s=s.replace('japan.blend','sri-lanka.blend').replace('japan.glb','sri-lanka.glb').replace('JAPAN AUTHORED','SRI LANKA AUTHORED')
s=s.replace("wood=mat('Cedar / fine longitudinal grain',(.4,.18,.08),.4);maptex(wood,'cedar-color.png','Base Color');maptex(wood,'cedar-roughness.png','Roughness',True)","wood=mat('Timber / dark structure',(.075,.038,.018),.5);maptex(wood,'timber.png','Base Color')\nweave=mat('Dumbara inspired / ivory weave',(.6,.5,.3),.88);maptex(weave,'weave-color.png','Base Color');maptex(weave,'weave-roughness.png','Roughness',True)")
s=s.replace("maptex(end,'cedar-end.png','Base Color')","maptex(end,'timber.png','Base Color')").replace("maptex(granite,'granite.png','Base Color')","maptex(granite,'timber.png','Base Color')")
s=s.replace("(.035,.07,.032)","(.025,.023,.018)")
s=s.replace("# Medallion is solid",'''# Woven inset panels are real skins, set clear of static fittings.
for sy in [-1,1]:
 cube('Weave / broad front rear',(0,sy*1.247,.78),(3.25,.012,1.20),weave,bevel=.002)
for sx in [-1,1]:
 cube('Weave / broad side',(sx*1.866,0,.78),(.012,1.94,1.20),weave,bevel=.002,axis='Y')
cube('Weave / lid panel',(0,0,1.987),(3.16,1.84,.018),weave,lid,.004)
threadm=[mat('Thread / brick red',(.25,.045,.026),.85),mat('Thread / charcoal',(.018,.018,.014),.85),mat('Thread / ochre',(.46,.29,.05),.85)]
# Three nested diamonds, fine raised tubes, each seated into the fibre carrier.
for k,cx in enumerate([-.92,0,.92]):
 for ring in range(3):
  rx=.40-ring*.075;ry=.65-ring*.10
  points=[(cx-rx,0,2.015),(cx,-ry,2.015),(cx+rx,0,2.015),(cx,ry,2.015)]
  for j in range(4):tube('Weave diamond %d ring %d segment %d'%(k,ring,j),[points[j],points[(j+1)%4]],[.023,.023],threadm[(k+ring)%3],sides=8)
# Medallion is solid''')
s=s.replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=3;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820').replace('(-5.6,-7.8,4.5)','(-5.6,-7.8,6.4)')
s=s.replace('Cedar /','Timber /').replace('Cedar foliage /','Unused palette /').replace('Cedar /','Timber /').replace('Cedar tree','Unused tree').replace('Mineral seam / moss green','Dark seam').replace('Granite foot','Timber foot')
(R/'author.py').write_text(s,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n*.blend1\n__pycache__/\n')
print('Scaffold ready')
