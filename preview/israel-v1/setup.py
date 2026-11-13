"""Copy only the established mechanical/viewer harness, never previous evidence."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for f in ['mechanism.blend','motion.mjs','package.json','THREE-LICENSE.txt']:
 shutil.copyfile(S/f,R/f)
for f in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html']:
 t=(S/f).read_text(encoding='utf8').replace('japan-cedar-v1','israel-v1').replace('japan.blend','israel.blend').replace('japan.glb','israel.glb').replace('Japan / Cedar & Moss','Israel / Negev Erosion').replace('Japan Cedar and Moss','Israel Negev Erosion').replace('Yakushima cedar. Mossed granite. Quiet brass.','Pale limestone. Ochre basin. Desert brass.').replace('inspired by the original Japan concept','inspired by the Negev erosional landscape').replace('JAPAN ·','ISRAEL ·')
 if not (R/f).exists(): (R/f).write_text(t,encoding='utf8')
# Reuse only helper functions and inherited mechanical assembly, not cedar art.
a=(S/'author.py').read_text()
prefix=a[:a.index('wood=mat(')]
prefix=prefix.replace('Reference-led Japan pilot','Negev Erosion pilot')
helpers=a[a.index('def uv('):a.index('for o in bpy.data.objects:')]
stone=a[a.index('def stone('):a.index("for sx in [-1,1]:\n for sy in [-1,1]:stone('Granite foot'")]
finish=a[a.index('# Medallion is solid'):]
finish=finish.replace('japan.blend','israel.blend').replace('japan.glb','israel.glb').replace('JAPAN AUTHORED','ISRAEL AUTHORED')
(R/'author.py').write_text(prefix+(R/'materials.inc').read_text()+helpers+(R/'geometry.inc').read_text()+stone+"\nfor sx in [-1,1]:\n for sy in [-1,1]:stone('Limestone foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)\n"+finish,encoding='utf8')
print('Prepared Israel-only author and inherited mechanical/browser harness')
