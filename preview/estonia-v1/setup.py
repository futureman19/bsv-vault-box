from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','THREE-LICENSE.txt','motion.mjs']:
 shutil.copy2(S/n,R/n)
for n in ['build.py','verify_browser.py','verify_source.py','verify_parity.py','viewer.js','template.html','package.json']:
 s=(S/n).read_text(encoding='utf8').replace('japan-cedar-v1','estonia-v1').replace('japan.blend','estonia.blend').replace('japan.glb','estonia.glb').replace('Japan / Cedar & Moss','Estonia / Limestone & Bog').replace('Japan Cedar and Moss','Estonia Limestone and Bog').replace('Yakushima cedar. Mossed granite. Quiet brass.','Pale limestone. Quiet bog pools. A path across the moss.').replace('inspired by the original Japan concept','inspired by Estonian limestone and bog landscapes').replace('JAPAN ·','ESTONIA ·')
 if n=='template.html':
  s=s.replace('h1{font-siz... [truncated]','h1{font-size:30px}.foot{flex-direction:column;gap:14px}}')
 if n=='viewer.js':
  s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.8,7)').replace('controls.maxDistance=11','controls.maxDistance=14')
  s=s.replace("bindAction(open,()=>{target=target?0:1;", "function snap(){if(ready&&reduced.matches){progress=target;const p=pose(progress);lid.rotation.x=p.lid;latch.rotation.x=p.latch;window.pilot.progress=progress;window.pilot.lid=p.lid;window.pilot.latch=p.latch;}}\n bindAction(open,()=>{target=target?0:1;snap();")
  s=s.replace("controls.reset();open.textContent", "controls.reset();snap();open.textContent")
 (R/n).write_text(s,encoding='utf8')
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
print('SETUP PASS')
