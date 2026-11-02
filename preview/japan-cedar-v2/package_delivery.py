from pathlib import Path
import argparse,hashlib,json,zipfile,shutil
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--delivery',default='C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-japan-cedar-v2');args=p.parse_args();D=Path(args.delivery);D.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['source-check.json','parity-check.json','browser-check.json','extended-check.json','reexport-check.json','placement-check.json','preservation-source-check.json','coverage-check.json']:
 assert (R/name).exists(),name
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert (R/'japan-cedar-v2.html').stat().st_size<4_700_000
assert all(v>=(1.65 if 'foliage' in k else 1.8) for k,v in json.loads((R/'coverage-check.json').read_text())['ratios'].items())
old=json.loads((R/'frozen-inputs.json').read_text());prior=R.parent/'japan-cedar-v1/preserved-inputs.json'
if prior.exists():old.update(json.loads(prior.read_text()))
preserved={}
for name,digest in old.items():
 f=Path(name)
 if f.exists():assert sha(f)==digest,name;preserved[name]='unchanged'
 else:preserved[name]='original unavailable in this extracted workspace'
(R/'preservation-check.json').write_text(json.dumps(preserved,indent=2))
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(f for f in R.rglob('*') if f.is_file() and (f.suffix in allowed or f.name=='.gitattributes') and f.name not in {'inventory.json','delivery-check.json'} and (f.parent==R or f.parent.name in {'maps','references','initial'}))
assert all(not any(x in f.parts for x in ['node_modules','.git','__pycache__']) for f in files)
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f)} for f in files}
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'japan-cedar-v2-source.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for f in files:archive.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert len(archive.namelist())==len(files);assert archive.testzip() is None
 for f in files:
  name=f.relative_to(R).as_posix();assert archive.read(name)==f.read_bytes();assert not name.startswith('/') and '..' not in Path(name).parts
copied=[]
for f in files+[z]:
 dest=D/f.relative_to(R);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest);assert sha(dest)==sha(f);copied.append(f.relative_to(R).as_posix())
report={'HTML_bytes':(R/'japan-cedar-v2.html').stat().st_size,'GLB_bytes':(R/'japan.glb').stat().st_size,'ZIP_bytes':z.stat().st_size,'ZIP_entries':len(files),'archive_readback_verified':True,'delivery_files_readback_verified':len(copied),'delivery':str(D),'copied':copied,'zip_sha256':sha(z),'html_sha256':sha(R/'japan-cedar-v2.html'),'glb_sha256':sha(R/'japan.glb'),'frozen_files_checked':sum(x=='unchanged' for x in preserved.values())}
s=json.dumps(report,indent=2);(R/'delivery-check.json').write_text(s);(D/'delivery-check.json').write_text(s);assert sha(R/'delivery-check.json')==sha(D/'delivery-check.json');print(s)
