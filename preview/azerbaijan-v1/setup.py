from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','package.json','THREE-LICENSE.txt']:
 shutil.copy2(S/n,R/n)
for n in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html']:
 t=(S/n).read_text(encoding='utf8').replace('japan-cedar-v1','azerbaijan-v1').replace('japan.glb','azerbaijan.glb').replace('japan.blend','azerbaijan.blend').replace('Japan / Cedar & Moss','Azerbaijan / Lahij Copper').replace('Japan Cedar and Moss','Azerbaijan Lahij Copper').replace('Yakushima cedar. Mossed granite. Quiet brass.','Hammered copper. Botanical relief. Satin brass.').replace('inspired by the original Japan concept','inspired by Lahij copper craftsmanship; original abstract botanical ornament').replace('JAPAN ·','AZERBAIJAN ·')
 if n=='template.html':
  t=t.replace('@media(max-width:600px)'+t.split('@media(max-width:600px)')[1].split('</style>')[0], '@media(max-width:600px){main{padding:18px}header{margin-top:20px}.top{gap:10px}.tag{max-width:150px;text-align:right}#stage{height:350px}h1{font-size:30px}.foot{flex-direction:column}}')
 if n=='verify_browser.py':
  t=t.replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1", "page.wait_for_function('pilot.progress===1',timeout=3000)").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0", "page.wait_for_function('pilot.progress===0',timeout=3000)")
 (R/n).write_text(t,encoding='utf8')
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
# Reuse only mechanics, helper primitives and studio setup, not cedar art.
t=(S/'author.py').read_text(); helpers=t[t.index('def select'):t.index("wood=mat")]+t[t.index('def uv'):t.index('for o in bpy.data.objects:')]
helpers=helpers.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z", "u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z")
(R/'helpers.py').write_text(helpers)
print('SETUP PASS')
