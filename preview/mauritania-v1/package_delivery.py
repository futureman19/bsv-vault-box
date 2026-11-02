from pathlib import Path
import hashlib,json,zipfile,re,base64
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
required={'mauritania.blend','mauritania.glb','mauritania-v1.html','poster.png','poster.jpg','design-brief.md','README.md','author.py','maps.py','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-source-check.json','motion-check.json','acceptance-check.json'}
assert json.loads((R/'acceptance-check.json').read_text())['status']=='PASS'
html=(R/'mauritania-v1.html').read_bytes();assert len(html)<5_000_000
embedded=base64.b64decode(re.search(rb'<script id="asset"[^>]*>(.*?)</script>',html,re.S).group(1));assert embedded==(R/'mauritania.glb').read_bytes()
for name in ['lane-output.txt','lane-prompt.txt']:(R/name).unlink(missing_ok=True)
excluded={'inventory.json','delivery-check.json','mauritania-v1-source.zip'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and p.name not in excluded and p.suffix not in ['.pyc','.blend1'] and '__pycache__' not in p.parts and 'node_modules' not in p.parts}
assert required<=files.keys(),required-files.keys()
inv={n:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for n,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'mauritania-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for n,p in sorted(files.items()):z.write(p,n)
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 for n,item in inv.items():assert len(z.read(n))==item['bytes'] and sha(z.read(n))==item['sha256']
report={'status':'PASS','html_bytes':len(html),'glb_bytes':len(embedded),'embedded_glb_exact':True,'inventory_files':len(inv),'required_artifacts_verified':sorted(required),'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath.read_bytes()),'archive_readback_all_hashes_match':True,'self_referential_exclusions':sorted(excluded)}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
