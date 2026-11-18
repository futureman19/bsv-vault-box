from pathlib import Path
import os,json,hashlib,zipfile,shutil
R=Path(__file__).resolve().parent
OUT=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-usa-flag-v9')
OUT.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
files=[]
for root,dirs,names in os.walk(R):
 dirs[:]=[d for d in dirs if d not in ['node_modules','__pycache__','.git']]
 for n in names:
  p=Path(root)/n
  if p.suffix in ['.zip','.blend1','.pyc'] or n in ['inventory.json','delivery-check.json','packaging-output.txt','git-check.json']:continue
  files.append(p)
files.sort();required={'united-states-flag-v9.html','united-states.blend','united-states.glb','hero-fireworks.png','primary-v8-v9-comparison.jpg','maps/flag-lid.png','maps/flag-wall.png','README.md','source-check.json','palette-check.json','browser-check.json','final-copied-browser-output.txt'}
records=[dict(path=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=sha(p.read_bytes())) for p in files]
assert required<=set(x['path'] for x in records)
inv=dict(files=records,required=sorted(required),exclusions=['node_modules','.blend1','ZIP itself','inventory/report self references'])
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'united-states-flag-v9-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 names=z.namelist();assert len(names)==len(set(names));assert required<=set(names)
 for name in names:assert not name.startswith(('/','\\')) and '..' not in Path(name).parts
 for rec in records:
  data=z.read(rec['path']);assert len(data)==rec['bytes'] and sha(data)==rec['sha256']
 assert json.loads(z.read('inventory.json'))==inv
selected=['united-states-flag-v9.html','united-states.blend','united-states.glb','united-states-flag-v9-source.zip','hero-fireworks.png','primary-v8-v9-comparison.jpg','mobile-closed.png','mobile-open.png','README.md','inventory.json']
copied=[]
for name in selected:
 p=R/name;q=OUT/name;shutil.copy2(p,q);assert p.read_bytes()==q.read_bytes();copied.append(dict(path=str(q),bytes=q.stat().st_size,sha256=sha(q.read_bytes())))
assert (OUT/'united-states-flag-v9.html').stat().st_size<5_000_000
with zipfile.ZipFile(OUT/zpath.name) as z:
 for rec in records:assert sha(z.read(rec['path']))==rec['sha256']
report=dict(PASS=True,zip_entries=len(records)+1,required_subset_verified=True,copied_html_offline_full_browser_test='final-copied-browser-output.txt',copied_zip_readback=True,artifacts=copied)
for folder in [R,OUT]:(folder/'delivery-check.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
