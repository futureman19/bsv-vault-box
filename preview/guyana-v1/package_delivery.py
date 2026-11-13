from pathlib import Path
import json,hashlib,zipfile,base64,re
R=Path(__file__).resolve().parent
required={'design-brief.md','README.md','guyana.blend','guyana.glb','guyana-v1.html','poster.png','poster.jpg','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','maps/sandstone-color.png','maps/sandstone-roughness.png','maps/sandstone-normal.png'}
def sha(b):return hashlib.sha256(b).hexdigest()
html=(R/'guyana-v1.html').read_bytes();glb=(R/'guyana.glb').read_bytes();assert len(html)<5000000
embedded=re.search(rb'<script id="asset" type="application/octet-stream">(.*?)</script>',html,re.S).group(1);assert base64.b64decode(embedded)==glb
poster=re.search(rb'data:image/jpeg;base64,([^"\s]+)',html).group(1);assert base64.b64decode(poster)==(R/'poster.jpg').read_bytes()
exclude={'inventory.json','delivery-check.json','guyana-v1-source.zip','delivery-log.txt','verification-log.txt','git-check.json'}
files=[p for p in R.rglob('*') if p.is_file() and not set(p.relative_to(R).parts)&{'node_modules','__pycache__'} and p.name not in exclude and not p.name.endswith('.blend1')]
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(files)}
assert required<=set(inventory),required-set(inventory)
(R/'inventory.json').write_text(json.dumps(inventory,indent=2))
z=R/'guyana-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in files:f.write(p,p.relative_to(R).as_posix())
 f.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())==set(inventory)|{'inventory.json'}
 for n,v in inventory.items():
  b=f.read(n);assert len(b)==v['bytes'] and sha(b)==v['sha256'],n
out={'PASS':True,'html_bytes':len(html),'glb_bytes':len(glb),'html_sha256':sha(html),'glb_sha256':sha(glb),'archive_bytes':z.stat().st_size,'archive_sha256':sha(z.read_bytes()),'inventory_entries':len(inventory),'required_artifacts_present':True,'archive_readback_all_hashes':True,'embedded_glb_and_poster_exact':True,'exclusions':'dependencies, caches, backups, inventory/envelopes and actively written logs; no circular hashes'}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print('DELIVERY_PASS',json.dumps(out))
