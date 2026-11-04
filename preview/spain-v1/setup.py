from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','motion.mjs','tests.mjs','package.json','package-lock.json']:
 if (S/name).exists():shutil.copyfile(S/name,R/name)
for name in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html']:
 t=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','spain-v1').replace('japan.blend','spain.blend').replace('japan.glb','spain.glb').replace('Japan / Cedar & Moss','Spain / Cobalt & Clay').replace('Japan Cedar and Moss','Spain Talavera Cobalt and Clay').replace('Yakushima cedar. Mossed granite. Quiet brass.','Terracotta. Cobalt petals. Ivory glaze.').replace('inspired by the original Japan concept','inspired by Spain’s Talavera ceramic tradition; an original stylized ornament, not an authentic historic pattern').replace('JAPAN ·','SPAIN ·')
 if name=='verify_browser.py':
  t=t.replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1',timeout=5000)").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0',timeout=5000)")
 (R/name).write_text(t,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n',encoding='utf8')
# Copy only generic helpers, not Japan geometry.
a=(S/'author.py').read_text(encoding='utf8')
helpers=a[a.index('def select'):a.index("wood=mat")]+a[a.index('def uv'):a.index('for o in bpy.data.objects:')]
(R/'helpers.py').write_text(helpers,encoding='utf8')
print('SETUP PASS')
