"""One-time scoped scaffold from the repository's existing Japan mechanics."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','motion.mjs','THREE-LICENSE.txt']:
 shutil.copyfile(S/name,R/name)
for name in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html','package.json']:
 text=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','albania-v1').replace('japan.blend','albania.blend').replace('japan.glb','albania.glb').replace('Japan / Cedar & Moss','Albania / Stone City').replace('Japan Cedar and Moss','Albania Stone City').replace('Yakushima cedar. Mossed granite. Quiet brass.','Limestone walls. Silver-grey roofs. A city in miniature.').replace('inspired by the original Japan concept','inspired by Gjirokastra stone architecture').replace('JAPAN ·','ALBANIA ·')
 if name=='template.html':
  text=text.replace('h1{font-siz... [truncated]','h1{font-size:30px}.foot{flex-direction:column}.folio{white-space:normal}}')
 if name=='viewer.js':text=text.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.5,7)').replace('controls.maxDistance=11','controls.maxDistance=14')
 if name=='verify_browser.py':
  text=text.replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1');assert page.evaluate('pilot.progress')==1").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0');assert page.evaluate('pilot.progress')==0")
 (R/name).write_text(text,encoding='utf8')
shutil.copyfile(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
# Compose using reviewed helpers and studio, not the Japan exterior or tree.
s=(S/'author.py').read_text()
head=s[:s.index("wood=mat(")]
helpers=s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
helpers=helpers.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z\n   if axis=='Y' and abs(p.normal.z)>.7:v=co.x","u,v=(co.x,co.y) if abs(p.normal.z)>.7 else ((co.y,co.z) if abs(p.normal.x)>.7 else (co.x,co.z))").replace('u/3.72+.5,v/1.7+.5','u/1.5+.5,v/1.5+.5')
tail=s[s.index('# Clean obsolete'):].replace('japan','albania').replace('JAPAN','ALBANIA').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820').replace('(-5.6,-7.8,4.5)','(-5.6,-7.8,6.4)')
(R/'author.py').write_text(head+(R/'geometry.py').read_text().split('# HELPERS')[0]+helpers+(R/'geometry.py').read_text().split('# HELPERS')[1]+tail)
print('SCAFFOLD PASS')
