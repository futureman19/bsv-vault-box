from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
required={'singapore-v1.html','singapore.glb','singapore.blend','mechanism.blend','design-brief.md','README.md','poster.png','source-check.json','parity-check.json','browser-check.json','theme-check.json','motion-check.json','extended-check.json'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json']}
assert required<=files.keys()
assert files['singapore-v1.html'].stat().st_size<5_000_000
inv={n:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for n,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
z=R/'singapore-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as out:
 for n,p in files.items():out.write(p,n)
 out.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as inp:
 assert set(inp.namelist())==set(files)|{'inventory.json'}
 for n,v in inv.items():assert sha(inp.read(n))==v['sha256'] and len(inp.read(n))==v['bytes']
r={'status':'PASS','html_bytes':files['singapore-v1.html'].stat().st_size,'glb_bytes':files['singapore.glb'].stat().st_size,'inventory_files':len(inv),'required_files_present':True,'archive_readback':True,'zip_bytes':z.stat().st_size,'zip_sha256':sha(z.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'scope':'Local archive only; excludes dependencies and backups; no recursive self-hashes'}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
