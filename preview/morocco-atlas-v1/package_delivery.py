from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,shutil
R=Path(__file__).resolve().parent;repo=R.parents[1];D=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-morocco-atlas-v1')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((R/'preserved-inputs.json').read_text());changed=[n for n,h in old.items() if not (repo/n).is_file() or sha(repo/n)!=h];assert not changed,changed
(R/'preservation-check.json').write_text(json.dumps({'checked_inputs':len(old),'changed':changed,'all_prior_inputs_preserved':True},indent=2))
assert (R/'morocco-atlas-v1.html').stat().st_size<4_500_000
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'source-check.json').read_text())['bearing_and_ridge_attachment_samples']==81
assert json.loads((R/'extended-check.json').read_text())['noJS_poster']
# Explicit extension and filename policy; no hidden files, secrets or dependency trees.
allowed={'.py','.js','.mjs','.html','.json','.md','.txt','.png','.jpg','.blend'}
exclude={'inventory.json','delivery-check.json'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.suffix in allowed and p.name not in exclude and not any(x.startswith('.') or x in ['node_modules','__pycache__'] for x in p.relative_to(R).parts))
files.append(R/'.gitattributes')
assert not any(any(s in p.name.lower() for s in ['secret','credential','.env','blend1']) for p in files)
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in files};(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'morocco-atlas-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as f:
 for p in files:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert len(f.namelist())==len(files) and f.testzip() is None
 for p in files:
  n=p.relative_to(R).as_posix();assert not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts
  assert hashlib.sha256(f.read(n)).hexdigest()==sha(p)
D.mkdir(parents=True,exist_ok=True)
for p in files+[z]:
 t=D/p.relative_to(R);t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,t);assert sha(t)==sha(p)
report={'archive':z.name,'archive_bytes':z.stat().st_size,'zip_entries':len(files),'zip_safe_inventory_readback':True,'delivery':str(D),'copied_hashes_verified':len(files)+1,'html_bytes':(R/'morocco-atlas-v1.html').stat().st_size,'glb_bytes':(R/'morocco.glb').stat().st_size,'blend_bytes':(R/'morocco.blend').stat().st_size,'prior_inputs_verified':len(old)}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));shutil.copy2(R/'delivery-check.json',D/'delivery-check.json');assert sha(R/'delivery-check.json')==sha(D/'delivery-check.json');print(json.dumps(report,indent=2))
