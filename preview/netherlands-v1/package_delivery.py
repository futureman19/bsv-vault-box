from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
required={'netherlands.blend','netherlands.glb','netherlands-v1.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','author.py','helpers.py','maps.py','build.py','run_checks.py','motion.mjs','viewer.js','template.html','THREE-LICENSE.txt','.gitattributes'}
exclude={'inventory.json','delivery-check.json','netherlands-v1-source.zip','package-output.txt','git-output.txt'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and not any(s in p.parts for s in ['node_modules','__pycache__']) and p.name not in exclude and p.suffix not in ['.blend1','.pyc']}
assert required<=files.keys(),required-files.keys()
assert files['netherlands-v1.html'].stat().st_size<5000000
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']>=81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for name in ['theme','extended']:assert json.loads((R/(name+'-check.json')).read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in browser}=={'desktop','mobile','corrupted GLB'}
inv={n:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for n,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2),encoding='utf8')
zip_path=R/'netherlands-v1-source.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
 for n,p in sorted(files.items()):z.write(p,n)
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(zip_path) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 for n,v in inv.items():assert sha(z.read(n))==v['sha256'] and len(z.read(n))==v['bytes']
result={'status':'PASS','html_bytes':inv['netherlands-v1.html']['bytes'],'glb_bytes':inv['netherlands.glb']['bytes'],'inventory_files':len(inv),'all_archive_bytes_read_back':True,'required_artifacts_present':sorted(required),'zip_bytes':zip_path.stat().st_size,'zip_sha256':sha(zip_path.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'exclusions':'inventory excludes itself, delivery report, archive and volatile package/git logs; no external copies'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
