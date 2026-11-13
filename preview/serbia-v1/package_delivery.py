from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
skip={'node_modules','__pycache__','.git'};envelopes={'inventory.json','delivery-check.json','serbia-v1-source.zip','verification-output.txt','package-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in skip for x in p.relative_to(R).parts) and p.name not in envelopes and not p.name.endswith(('.blend1','.pyc')))
h=lambda b:hashlib.sha256(b).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':h(p.read_bytes())} for p in files}
required={'serbia-v1.html','serbia.glb','serbia.blend','mechanism.blend','design-brief.md','README.md','poster.png','poster.jpg','.gitattributes','source-check.json','parity-check.json','browser-check.json','theme-check.json','extended-check.json','maps/weave-color.png','maps/weave-normal.png','maps/weave-roughness.png'}
assert required<=set(inv),required-set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'serbia-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert len(z.read(n))==v['bytes'] and h(z.read(n))==v['sha256'],n
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
html=(R/'serbia-v1.html').stat().st_size;glb=(R/'serbia.glb').stat().st_size;assert html<5000000
out={'status':'PASS','HTML_BYTES':html,'GLB_BYTES':glb,'ZIP_BYTES':zpath.stat().st_size,'ZIP_SHA256':h(zpath.read_bytes()),'inventory_sha256':h((R/'inventory.json').read_bytes()),'inventory_entries':len(inv),'required_files_included':True,'archive_readback_verified':True,'scope':'folder-local delivery; no external copy or upload'}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
