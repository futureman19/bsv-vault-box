from pathlib import Path
import hashlib,json,zipfile,shutil
R=Path(__file__).resolve().parent
O=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-iceland-lightweight-v3')
N='iceland-lightweight-v3-source.zip'
names='README.md build.py generate.py refine_source.py verify_browser.py verify_pbr.py verify_source.py verify_editable.py verify_preservation.py test_budget.py tests.mjs motion.mjs viewer.js viewer.bundle.js template.html package.json package-lock.json THREE-LICENSE.txt package_delivery.py iceland-lightweight-v3.html iceland.glb iceland.blend poster.png poster.jpg browser-check.json budget-red.txt budget-green.txt motion-green.txt pbr-check.json preservation-check.json editable-check.json source-check.json desktop-closed.png desktop-open.png mobile-closed.png mobile-open.png mobile-fallback.png comparison-closed.jpg comparison-open.jpg comparison-closeup.jpg original-closed-stage.png original-open-stage.png original-closeup.png v3-closed-stage.png v3-open-stage.png v3-closeup.png'.split()
names += ['original/'+n for n in ['iceland.glb','iceland.blend','author.py','viewer.js','viewer.bundle.js','motion.mjs','iceland-pilot.html']]
names += ['textures/'+n for n in ['basalt-color.jpg','basalt-orm.jpg','basalt-normal.png']]
def digest(b):return hashlib.sha256(b).hexdigest()
with zipfile.ZipFile(R/N,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in sorted(names):z.write(R/n,n)
with zipfile.ZipFile(R/N) as z:
 assert sorted(z.namelist())==sorted(names) and len(z.namelist())==len(set(names))
 for n in names:
  assert '..' not in Path(n).parts and not Path(n).is_absolute() and not n.endswith('.blend1') and 'node_modules' not in n
  assert z.read(n)==(R/n).read_bytes()
O.mkdir(parents=True,exist_ok=True);records={}
for n in names+[N]:
 dest=O/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/n,dest)
 a=(R/n).read_bytes();assert dest.read_bytes()==a
 records[n]={'bytes':len(a),'sha256':digest(a)}
result={'output_directory':str(O),'all_output_copies_hash_match':True,'zip_inventory_allowlisted_and_readback_verified':True,'zip_entries':len(names),'files':records}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));shutil.copyfile(R/'delivery-check.json',O/'delivery-check.json');assert (R/'delivery-check.json').read_bytes()==(O/'delivery-check.json').read_bytes()
print(json.dumps({'html':records['iceland-lightweight-v3.html'],'glb':records['iceland.glb'],'blend':records['iceland.blend'],'zip':records[N],'zip_entries':len(names),'output':str(O)},indent=2))
