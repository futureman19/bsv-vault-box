"""One-time adaptation of read-only Japan mechanism and offline harness."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; B=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','package.json','THREE-LICENSE.txt']:
 shutil.copy2(B/n,R/n)
for n in ['viewer.js','template.html','build.py','verify_browser.py','verify_source.py','verify_parity.py']:
 s=(B/n).read_text(encoding='utf8').replace('japan-cedar-v1','arctic-ocean-v1').replace('japan.glb','arctic.glb').replace('japan.blend','arctic.blend').replace('Japan / Cedar & Moss','Arctic Ocean / Floes & Blue Leads').replace('Japan Cedar and Moss','Arctic Ocean Floes and Blue Leads').replace('Yakushima cedar. Mossed granite. Quiet brass.','Polar floes. Blue leads. Quiet brass.').replace('inspired by the original Japan concept','inspired by Arctic sea-ice landscapes').replace('JAPAN ·','ARCTIC OCEAN ·')
 (R/n).write_text(s,encoding='utf8')
# Retain utility functions and proven fittings only, not Japan exterior or tree.
s=(B/'author.py').read_text(); lines=s.splitlines(True)
header=''.join(lines[3:19])
utilities=''.join(lines[28:42])
hardware=''.join(lines[124:131])
ending=''.join(lines[132:148]).replace('japan','arctic').replace('JAPAN','ARCTIC').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=2').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
(R/'author.py').write_text(header+(R/'materials.part').read_text()+utilities+(R/'geometry.part').read_text()+hardware+ending,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n')
