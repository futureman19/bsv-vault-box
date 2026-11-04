"""One-time local lineage copy; only writes this new pilot directory."""
from pathlib import Path
import shutil,hashlib,json
R=Path(__file__).resolve().parent
J=R.parent/'japan-cedar-v1'
files=['mechanism.blend','viewer.js','template.html','motion.mjs','build.py','verify_source.py','verify_parity.py','verify_browser.py','THREE-LICENSE.txt','package.json']
record={}
for name in files:
 p=J/name; data=p.read_bytes();record[name]=hashlib.sha256(data).hexdigest()
 if p.suffix in ['.py','.js','.html','.mjs']:
  s=data.decode().replace('japan-cedar-v1','burundi-v1').replace('japan.blend','burundi.blend').replace('japan.glb','burundi.glb').replace('Japan Cedar and Moss','Burundi Sisal and Sweetgrass').replace('Japan / Cedar & Moss','Burundi / Sisal & Sweetgrass').replace('Yakushima cedar. Mossed granite. Quiet brass.','Coiled sweetgrass. Woven sisal. Satin brass.').replace('inspired by the original Japan concept','inspired by Burundi’s basketry traditions').replace('JAPAN ·','BURUNDI ·')
  (R/name).write_text(s,encoding='utf8')
 else: shutil.copyfile(p,R/name)
(R/'lineage.json').write_text(json.dumps({'base_commit':'ff5d78f1e0d486af5c882c184fc08049996ebdc8','source':'preview/japan-cedar-v1','sha256':record},indent=2))
# Reuse only general construction and studio code, never Japan tree/terrain.
s=(J/'author.py').read_text()
helpers=s[s.index('def select'):s.index('wood=mat')]
cubes=s[s.index('def uv'):s.index('for o in bpy.data.objects:')]
tubes=s[s.index('def tube'):s.index('trunk=')]
disks=s[s.index('def disk'):s.index('# Clean obsolete')]
finish=s[s.index('# Clean obsolete'):].replace('japan','burundi').replace('JAPAN AUTHORED','BURUNDI AUTHORED')
(R/'helpers.py').write_text(helpers+cubes+tubes+disks[:disks.index("disk('Medallion")])
(R/'finish.py').write_text(finish)
print('LINEAGE_COPIED',len(files))
