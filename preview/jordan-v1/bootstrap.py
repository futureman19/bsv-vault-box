"""Reproduce the explicitly inherited mechanism/viewer harness from repository Japan v1.
Run once before authoring; no predecessor files are written.
"""
from pathlib import Path
import shutil,hashlib,json
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
files=['mechanism.blend','build.py','viewer.js','motion.mjs','template.html','verify_source.py','verify_parity.py','verify_browser.py','package.json','THREE-LICENSE.txt']
provenance={}
for name in files:
 data=(S/name).read_bytes();provenance[name]=hashlib.sha256(data).hexdigest()
 if name.endswith(('.py','.js','.html')):
  text=data.decode().replace('japan-cedar-v1','jordan-v1').replace('japan.blend','jordan.blend').replace('japan.glb','jordan.glb').replace('Japan / Cedar & Moss','Jordan / Rose & Ochre').replace('Japan Cedar and Moss','Jordan Wadi Rum').replace('Yakushima cedar. Mossed granite. Quiet brass.','Rose sandstone. A winding siq. Desert brass.').replace('inspired by the original Japan concept','inspired by the sandstone landforms of Wadi Rum, Jordan').replace('JAPAN ·','JORDAN ·')
  (R/name).write_text(text,encoding='utf8')
 else:shutil.copyfile(S/name,R/name)
(R/'lineage.json').write_text(json.dumps({'base_commit':'ff5d78f1e0d486af5c882c184fc08049996ebdc8','source_directory':'preview/japan-cedar-v1','input_sha256':provenance},indent=2))
print('Inherited',len(files),'files into Jordan only')
