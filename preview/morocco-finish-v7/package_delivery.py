from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
required={'morocco-finish-v7.html','morocco.glb','morocco.blend','poster.jpg','poster.png','baseline/morocco.blend','baseline/morocco.glb','README.md','design-brief.md','reference-comparison.jpg','lid-comparison.jpg','source-check.json','parity-check.json','browser-check.json','fallback-check.json','extended-check.json','finish-check.json','delta-check.json','source-preservation-check.json','hinge-attachment-check.json','visual-review.json','delivery-check.json'}
html=(R/'morocco-finish-v7.html').stat().st_size;glb=(R/'morocco.glb').stat().st_size
assert html<5000000
report={'html_bytes':html,'glb_bytes':glb,'inventory_order':'generated after final HTML build and all acceptance evidence','html_sha256':hashlib.sha256((R/'morocco-finish-v7.html').read_bytes()).hexdigest(),'required_artifacts_present':True,'scope':'candidate only; no approval, mint, deployment or merge'}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2))
excluded={'inventory.json','morocco-finish-v7-source.zip','target-export.glb','adapt_v7.py','open_delivery.py'}
files=[p for p in R.rglob('*') if p.is_file() and p.name not in excluded and p.suffix not in {'.blend1','.pyc'} and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__','inherited-v6'])]
records={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)}
assert required<=records.keys(),required-records.keys()
manifest={'required_files':sorted(required),'files':records,'envelope_exclusions':['inventory.json (self-reference)','morocco-finish-v7-source.zip (contains inventory)'],'other_exclusions':sorted(excluded|{'node_modules','__pycache__','inherited-v6','blend backups'}),'final_html_bytes':html,'final_glb_bytes':glb}
(R/'inventory.json').write_text(json.dumps(manifest,indent=2))
zpath=R/'morocco-finish-v7-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert z.testzip() is None
 for rel,r in records.items():assert hashlib.sha256(z.read(rel)).hexdigest()==r['sha256']
print(json.dumps({**report,'source_zip_bytes':zpath.stat().st_size,'inventory_files':len(records),'zip_hash_mismatches':0},indent=2))
