from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'moldova-v1.html','moldova.glb','moldova.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-check.json','author.py','maps.py','build.py','verify_source.py','verify_parity.py','verify_browser.py','verify_extended.py','test_theme.py','motion.mjs','tests.mjs','.gitattributes'}
def digest(b):return hashlib.sha256(b).hexdigest()
files=[p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.zip'] and p.name not in ['inventory.json','delivery-check.json','package-output.txt','git-evidence.txt']]
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in sorted(files)}
assert required<=inv.keys();assert inv['moldova-v1.html']['bytes']<5000000
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'moldova-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for name,v in inv.items():
  data=z.read(name);assert len(data)==v['bytes'] and digest(data)==v['sha256']
result={'status':'PASS','html_bytes':inv['moldova-v1.html']['bytes'],'glb_bytes':inv['moldova.glb']['bytes'],'required_files_present':True,'zip_entries_verified':len(inv)+1,'zip_bytes':zpath.stat().st_size,'zip_sha256':digest(zpath.read_bytes()),'inventory_sha256':digest((R/'inventory.json').read_bytes()),'all_archive_hashes_match':True}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
