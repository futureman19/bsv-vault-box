"""Exact-byte local archive, required artifact coverage, and ZIP readback."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','kiribati-v1-source.zip','delivery-output.txt','git-output.txt'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in excluded and not any(x in p.parts for x in ['node_modules','__pycache__','delivery-verify']) and p.suffix not in ['.blend1','.pyc'])
required={'kiribati.blend','kiribati.glb','kiribati-v1.html','mechanism.blend','design-brief.md','README.md','poster.png','poster.jpg','source-check.json','parity-check.json','browser-check.json','theme-source-check.json','extended-check.json','motion-check.json','visual-check.json','maps/pandanus-color.png','maps/pandanus-roughness.png','maps/pandanus-normal.png','maps/sand-color.png','.gitattributes'}
relative={p.relative_to(R).as_posix():p for p in files};assert required<=relative.keys(),required-relative.keys()
sha=lambda data:hashlib.sha256(data).hexdigest()
inv={n:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for n,p in relative.items()}
(R/'inventory.json').write_text(json.dumps(inv,indent=2),encoding='utf8')
zpath=R/'kiribati-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in relative.items():z.write(p,n)
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,d in inv.items():data=z.read(n);assert len(data)==d['bytes'] and sha(data)==d['sha256'],n
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
html=(R/'kiribati-v1.html').stat().st_size;glb=(R/'kiribati.glb').stat().st_size;assert html<5_000_000
out={'status':'PASS','HTML_BYTES':html,'GLB_BYTES':glb,'required_artifacts':sorted(required),'payload_file_count':len(inv),'zip_entries':len(inv)+1,'zip_readback_all_hashes':True,'html_sha256':inv['kiribati-v1.html']['sha256'],'glb_sha256':inv['kiribati.glb']['sha256'],'inventory_sha256':sha((R/'inventory.json').read_bytes()),'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath.read_bytes()),'excluded_self_references':sorted(excluded),'limitations':'Local archive, not hosted, minted, signed or permanently stored.'}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
