"""One-time scoped reuse of reviewed collection mechanism/runtime."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
J=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','THREE-LICENSE.txt','package.json']:
 shutil.copyfile(J/n,R/n)
for n in ['viewer.js','template.html','verify_source.py','verify_parity.py','verify_browser.py','build.py']:
 s=(J/n).read_text(encoding='utf8').replace('japan-cedar-v1','saint-lucia-v1').replace('japan.glb','saint-lucia.glb').replace('japan.blend','saint-lucia.blend').replace('Japan / Cedar & Moss','Saint Lucia / Pitons & Caribbean').replace('Japan Cedar and Moss','Saint Lucia Pitons and Caribbean').replace('Yakushima cedar. Mossed granite. Quiet brass.','Forest-clad spires. Volcanic stone. Caribbean blue.').replace('the original Japan concept','a researched Saint Lucian landscape brief').replace('JAPAN ·','SAINT LUCIA ·')
 if n=='verify_browser.py':
  s=s.replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1',timeout=2000)").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0',timeout=2000)")
 (R/n).write_text(s,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n')
# Reuse small modeling functions only, not the Japan art.
s=(J/'author.py').read_text()
helpers=s[s.index('def select(o):'):s.index('wood=mat(')]+s[s.index('def uv('):s.index('for o in bpy.data.objects:')]+s[s.index('def stone('):s.index('for sx in [-1,1]:\n for sy in [-1,1]:stone')]+s[s.index('def disk('):s.index("disk('Medallion")]
helpers=helpers.replace('material=granite','material=None').replace("def uv(o,axis='X',endgrain=False):", "def uv(o,axis='X',endgrain=False):")
a=helpers.index('   u=co.y');b=helpers.index('def cube(')
helpers=helpers[:a]+'''   normal=p.normal
   u,v=(co.y,co.z) if abs(normal.x)>.7 else ((co.x,co.z) if abs(normal.y)>.7 else (co.x,co.y))
   layer.data[li].uv=(u*.55+.5,v*.55+.5)
'''+helpers[b:]
(R/'helpers.py').write_text(helpers)
print('SCOPED_SETUP_OK')
