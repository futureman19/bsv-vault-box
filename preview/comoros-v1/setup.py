from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','package.json','viewer.js','template.html','motion.mjs','verify_source.py','verify_parity.py','verify_browser.py','build.py']:
 if name.endswith(('.blend','.txt')):shutil.copyfile(S/name,R/name);continue
 text=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','comoros-v1').replace('japan.glb','comoros.glb').replace('japan.blend','comoros.blend').replace('Japan / Cedar & Moss','Comoros / Karthala & Perfume Isles').replace('Japan Cedar and Moss','Comoros Karthala and Perfume Isles').replace('Yakushima cedar. Mossed granite. Quiet brass.','Volcanic stone. Yellow blossoms. Indian Ocean.').replace('original Japan concept','Comoros volcanic landscapes and perfume flora').replace('JAPAN','COMOROS').replace('Invalid Japan','Invalid Comoros')
 (R/name).write_text(text,encoding='utf8')
s=(S/'author.py').read_text()
# Copy inspected geometry helpers and mechanical/studio sections only.
helpers=s[s.index('def select'):s.index('wood=mat')]
uvcube=s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
stone=s[s.index('def stone('):s.index('for sx in [-1,1]:\n for sy in [-1,1]:stone')]
hardware=s[s.index('# Medallion is solid'):s.index('# Clean obsolete')]
studio=s[s.index('# Clean obsolete'):].replace('japan.blend','comoros.blend').replace('japan.glb','comoros.glb').replace('JAPAN AUTHORED','COMOROS AUTHORED')
(R/'helpers.py').write_text('import bpy,math,random\nfrom mathutils import Vector\n'+helpers+uvcube+stone,encoding='utf8')
(R/'hardware.inc').write_text(hardware,encoding='utf8')
(R/'studio.inc').write_text(studio,encoding='utf8')
print('Scoped reusable mechanism/viewer helpers prepared')
