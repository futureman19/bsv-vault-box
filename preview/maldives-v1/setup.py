from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','THREE-LICENSE.txt','motion.mjs']:
 shutil.copyfile(S/n,R/n)
for n in ['viewer.js','template.html','build.py','verify_source.py','verify_parity.py','verify_browser.py','package.json']:
 s=(S/n).read_text(encoding='utf8').replace('japan-cedar-v1','maldives-v1').replace('japan.glb','maldives.glb').replace('japan.blend','maldives.blend').replace('Japan / Cedar & Moss','Maldives / Faro & Lagoon').replace('Japan Cedar and Moss','Maldives Faro and Lagoon').replace('Yakushima cedar. Mossed granite. Quiet brass.','Coralline sand. Turquoise lagoon. Satin brass.').replace('inspired by the original Japan concept','inspired by Maldivian reef lagoons; an invented miniature, not a mapped atoll').replace('JAPAN ·','MALDIVES ·')
 if n=='viewer.js':s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.5,7)')
 (R/n).write_text(s,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
# Reuse only the proven primitive/hardware helpers; no inherited country geometry.
s=(S/'author.py').read_text(); pre=s[s.index('import bpy'):s.index('wood=mat')]
pre=pre.replace('Reference-led Japan','Maldives')
helpers=s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
helpers=helpers.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z", "u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z")
stone=s[s.index('def stone('):s.index("stone('Terrain / granite'")]
stone=stone.replace("for sx in [-1,1]:\n for sy in [-1,1]:stone('Granite foot'", "for sx in [-1,1]:\n for sy in [-1,1]:stone('Sandstone foot'")
hardware=s[s.index('# Medallion is solid'):s.index('# Clean obsolete')]
finish=s[s.index('# Clean obsolete'):].replace('japan.blend','maldives.blend').replace('japan.glb','maldives.glb').replace('JAPAN AUTHORED','MALDIVES AUTHORED').replace('(-5.6,-7.8,4.5)','(-5.6,-7.8,6.5)').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
(R/'author.py').write_text(pre+(R/'geometry.py').read_text().split('# HELPERS')[0]+helpers+(R/'geometry.py').read_text().split('# HELPERS')[1]+stone+hardware+finish)
print('SETUP PASS')
