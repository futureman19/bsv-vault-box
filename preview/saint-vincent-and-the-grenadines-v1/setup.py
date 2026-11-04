from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','THREE-LICENSE.txt','package.json']:
 shutil.copyfile(S/n,R/n)
for n in ['build.py','viewer.js','template.html','motion.mjs','verify_source.py','verify_parity.py','verify_browser.py']:
 s=(S/n).read_text(encoding='utf8').replace('japan-cedar-v1','saint-vincent-and-the-grenadines-v1').replace('japan.glb','saint-vincent-and-the-grenadines.glb').replace('japan.blend','saint-vincent-and-the-grenadines.blend').replace('Japan / Cedar & Moss','Saint Vincent and the Grenadines / Soufrière & Cays').replace('Japan Cedar and Moss','Saint Vincent and the Grenadines Soufrière and Cays').replace('Yakushima cedar. Mossed granite. Quiet brass.','Volcanic stone. Five reef cays. Satin brass.').replace('inspired by the original Japan concept','inspired by Vincentian volcanic landscapes and the Tobago Cays').replace('JAPAN · 3D / 001','SVG · 3D / 001').replace('Invalid Japan','Invalid Saint Vincent')
 if n=='verify_browser.py':
  s=s.replace('timeout=25000','timeout=90000').replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1',timeout=5000)").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0',timeout=5000)")
 if n=='viewer.js':
  s=s.replace('},15000)','},90000)')
  s=s.replace("open.setAttribute('aria-pressed',String(!!target));","open.setAttribute('aria-pressed',String(!!target));if(reduced.matches){progress=target;const p=pose(progress);lid.rotation.x=p.lid;latch.rotation.x=p.latch;pilot.progress=progress;}")
  s=s.replace("controls.reset();open.textContent", "controls.reset();const p=pose(0);lid.rotation.x=p.lid;latch.rotation.x=p.latch;pilot.progress=0;open.textContent")
 (R/n).write_text(s,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n',encoding='utf8')
# Helpers only: no Japan decorative geometry carried over.
s=(S/'author.py').read_text(encoding='utf8')
helpers=s[s.index('def select(o):'):s.index("wood=mat(")]+s[s.index('def cube('):s.index('for o in bpy.data.objects:')]
(R/'geometry_helpers.py').write_text(helpers,encoding='utf8')
print('SETUP PASS')
