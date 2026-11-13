"""Copy reviewed mechanical/viewer lineage; never copy old acceptance results."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
J=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','motion.mjs','package.json','THREE-LICENSE.txt']:
 shutil.copy2(J/name,R/name)
for name in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html']:
 text=(J/name).read_text(encoding='utf8').replace('japan-cedar-v1','mauritania-v1').replace('japan.blend','mauritania.blend').replace('japan.glb','mauritania.glb').replace('Japan / Cedar & Moss','Mauritania / Richat').replace('Japan Cedar and Moss','Mauritania Richat').replace('Yakushima cedar. Mossed granite. Quiet brass.','Eye of the Sahara. Eroded ridges. Desert brass.').replace('inspired by the original Japan concept','inspired by Mauritania’s Richat Structure').replace('JAPAN ·','MAURITANIA ·')
 (R/name).write_text(text,encoding='utf8')
# Reuse helper definitions and source studio/export setup, not Japan scenery.
s=(J/'author.py').read_text(encoding='utf8')
helpers=s[s.index('def select'):s.index("wood=mat")]+s[s.index('def uv'):s.index('for o in bpy.data.objects:')]
footer=s[s.index('# Clean obsolete'):].replace('japan.blend','mauritania.blend').replace('japan.glb','mauritania.glb').replace('JAPAN AUTHORED','MAURITANIA AUTHORED')
(R/'author_helpers.py').write_text(helpers,encoding='utf8')
(R/'author_finish.py').write_text(footer,encoding='utf8')
print('Reviewed lineage copied; no old evidence copied.')
