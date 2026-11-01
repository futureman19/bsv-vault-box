"""Allowlisted local-only packaging; never touches other delivery versions."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,shutil
R=Path(__file__).resolve().parent
D=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-iceland-painted-v4')
def sha(b):return hashlib.sha256(b).hexdigest()
allowed={'.py','.mjs','.js','.html','.md','.txt','.json','.jpg','.png','.glb','.blend'}
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.suffix in allowed or p.name=='.gitattributes') and '__pycache__' not in p.parts and p.name not in {'inventory.json','delivery-check.json'})
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
zpath=R/'iceland-painted-v4-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 names=z.namelist();assert len(names)==len(set(names))==len(files)
 for name in names:
  p=PurePosixPath(name);assert not p.is_absolute() and '..' not in p.parts and ':' not in name and '\\' not in name
  assert sha(z.read(name))==sha((R/name).read_bytes())
D.mkdir(exist_ok=True,parents=True)
for p in files+[zpath]:
 dest=D/p.relative_to(R);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest);assert dest.read_bytes()==p.read_bytes()
result={'html_bytes':(R/'iceland-painted-v4.html').stat().st_size,'glb_bytes':(R/'iceland.glb').stat().st_size,'blend_bytes':(R/'iceland.blend').stat().st_size,'source_zip_bytes':zpath.stat().st_size,'source_zip_sha256':sha(zpath.read_bytes()),'zip_safe_unique_entries':len(files),'zip_every_entry_hash_verified':True,'delivery_every_file_readback_verified':True,'delivery':str(D)}
for base in [R,D]:(base/'delivery-check.json').write_text(json.dumps(result,indent=2))
assert (D/'delivery-check.json').read_bytes()==(R/'delivery-check.json').read_bytes()
print(json.dumps(result,indent=2))
