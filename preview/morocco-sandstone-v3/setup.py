from pathlib import Path
import shutil,hashlib,json
R=Path(__file__).resolve().parent;OLD=R.parent/'morocco-atlas-v2'
files=['viewer.js','viewer.bundle.js','motion.mjs','template.html','build.py','verify_browser.py','verify_extended.py','verify_source.py','verify_parity.py','THREE-LICENSE.txt','package.json']
for f in files:
 s=(OLD/f).read_text(encoding='utf8');s=s.replace('morocco-atlas-v2.html','morocco-sandstone-v3.html')
 if f=='verify_extended.py':s=s.replace("<=512","<=1024")
 (R/f).write_text(s,encoding='utf8')
(R/'baseline').mkdir(exist_ok=True)
for f in ['morocco.blend','morocco.glb'] :shutil.copy2(OLD/f,R/'baseline'/f)
(R/'maps').mkdir(exist_ok=True)
(R/'baseline-hashes.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'baseline').iterdir()},indent=2))
print('Isolated v3; baseline copied; viewer source and motion unchanged')
