from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
skip={'inventory.json','delivery-check.json','kenya-v1-source.zip'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and not {'node_modules','__pycache__'}.intersection(p.relative_to(R).parts) and p.suffix!='.blend1' and p.name not in skip}
required={'kenya-v1.html','kenya.glb','kenya.blend','mechanism.blend','poster.png','README.md','design-brief.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','acceptance-check.json','motion-output.txt'}
assert required<=files.keys(),required-files.keys()
assert files['kenya-v1.html'].stat().st_size<5000000
assert json.loads(files['acceptance-check.json'].read_text())['status']=='PASS'
def record(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
inv={n:record(p.read_bytes()) for n,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'kenya-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for n,p in sorted(files.items()):out.write(p,n)
 out.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as src:
 assert set(src.namelist())==set(files)|{'inventory.json'}
 for n,r in inv.items():assert record(src.read(n))==r,n
 assert src.read('inventory.json')==(R/'inventory.json').read_bytes()
result={'status':'PASS','required_artifacts':sorted(required),'payload_file_count':len(files),'html_bytes':inv['kenya-v1.html']['bytes'],'glb_bytes':inv['kenya.glb']['bytes'],'inventory':record((R/'inventory.json').read_bytes()),'archive':record(z.read_bytes()),'zip_readback_verified':True}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
