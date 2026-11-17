import pathlib,json,hashlib,zipfile,subprocess
R=pathlib.Path(__file__).resolve().parent
files=[p for p in R.rglob('*') if p.is_file() and p.name not in ['evidence-inventory.json','qa-art-03-report.zip'] and '__pycache__' not in p.parts]
inv=[{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)]
(R/'evidence-inventory.json').write_text(json.dumps({'files':inv},indent=2)+'\n')
names=['README.md','review.html','reviewed-ledger.json','packaging-audit.json','smoke-results.json','motion-results.json','audit.py','finalize.py','verify.py','package.py','evidence-inventory.json']
with zipfile.ZipFile(R/'qa-art-03-report.zip','w',zipfile.ZIP_DEFLATED) as z:
 for n in names:z.write(R/n,n)
with zipfile.ZipFile(R/'qa-art-03-report.zip') as z:
 assert set(z.namelist())==set(names) and len(z.namelist())==len(names) and z.testzip() is None
 assert all(z.read(n)==(R/n).read_bytes() for n in names)
subprocess.run(['git','add','launch/qa-art-03'],check=True)
for e in inv:
 b=subprocess.check_output(['git','show',':launch/qa-art-03/'+e['path']]);assert hashlib.sha256(b).hexdigest()==e['sha256']
print('staged inventory',len(inv))
for n in ['reviewed-ledger.json','review.html','qa-art-03-report.zip']:
 b=(R/n).read_bytes();print(n,len(b),hashlib.sha256(b).hexdigest())
