from pathlib import Path
import hashlib,json,shutil,subprocess
R=Path(__file__).resolve().parent; repo=R.parents[1]; old=R.parent/'japan-cedar-v1'
files=subprocess.check_output(['git','-C',str(repo),'ls-files','-z']).decode().split('\0'); hashes={f:hashlib.sha256((repo/f).read_bytes()).hexdigest() for f in files if f and (repo/f).is_file()}
ref=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-concepts/morocco.png');hashes[str(ref)]=hashlib.sha256(ref.read_bytes()).hexdigest()
(R/'preserved-inputs.json').write_text(json.dumps(hashes,indent=2));(R/'references').mkdir(exist_ok=True);shutil.copy2(ref,R/'references/primary-morocco.png')
for n in ['mechanism.blend','motion.mjs','viewer.js','build.py','template.html','verify_browser.py','verify_source.py','verify_parity.py','THREE-LICENSE.txt','package.json']:
 if n.endswith(('.blend','.txt','.json')):shutil.copy2(old/n,R/n)
 else:
  s=(old/n).read_text(encoding='utf8').replace('japan-cedar-v1','morocco-atlas-v1').replace('japan.glb','morocco.glb').replace('japan.blend','morocco.blend').replace('Japan','Morocco').replace('JAPAN','MOROCCO').replace('Cedar & Moss','Atlas & Tile').replace('Cedar and Moss','Atlas and Tile').replace('Yakushima cedar. Mossed granite. Quiet brass.','Rose stone. Cedar. Geometric ceramic. Atlas ridges.')
  (R/n).write_text(s,encoding='utf8')
print('preserved',len(hashes))
