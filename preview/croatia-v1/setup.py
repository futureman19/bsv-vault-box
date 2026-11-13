from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
J=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','THREE-LICENSE.txt','package.json','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html','build.py']:
 if n.endswith(('.py','.js','.html')):
  s=(J/n).read_text(encoding='utf8').replace('japan-cedar-v1','croatia-v1').replace('japan.blend','croatia.blend').replace('japan.glb','croatia.glb').replace('Japan / Cedar & Moss','Croatia / Plitvice Tufa').replace('Japan Cedar and Moss','Croatia Plitvice Tufa').replace('Yakushima cedar. Mossed granite. Quiet brass.','Pale tufa. Cascading turquoise. Quiet brass.').replace('inspired by the original Japan concept','inspired by Croatia’s Plitvice lake terraces').replace('JAPAN ·','CROATIA ·')
  if n=='viewer.js':s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.8,7)').replace('controls.maxDistance=11','controls.maxDistance=14')
  if n=='verify_browser.py':s=s.replace("page.wait_for_timeout(70);assert", "page.wait_for_function('pilot.progress===1');assert").replace("page.wait_for_timeout(60);assert", "page.wait_for_function('pilot.progress===0');assert")
  (R/n).write_text(s,encoding='utf8')
 else:shutil.copy2(J/n,R/n)
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
# Reuse bounded geometry helpers and proven family hardware, not Japan visible theme.
s=(J/'author.py').read_text()
helpers=s[s.index('def select'):s.index('wood=mat')]
uv=s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
uv=uv.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z", "u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z")
stone=s[s.index('def stone('):s.index("for sx in [-1,1]:\n for sy in [-1,1]:stone")]
hardware=s[s.index('# Medallion is solid'):s.index('# Clean obsolete')]
(R/'helpers.py').write_text(helpers+uv+stone+hardware.replace("# Medallion is solid, never an unexplained front opening.", '# Family fittings; run after materials are defined.'))
# Helpers include stone default=granite; author initializes materials before exec.
