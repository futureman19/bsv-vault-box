from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'portugal-v1.html','portugal.glb','portugal.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json'}
def budget(n):assert n<5_000_000
budget((R/'portugal-v1.html').stat().st_size)
try:budget(5_000_000)
except AssertionError:negative=True
else:raise AssertionError('Budget negative accepted')
def digest(b):return hashlib.sha256(b).hexdigest()
files=[p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json','verification.log','codex-lane.log','lane-prompt.md']]
assert required <= {p.relative_to(R).as_posix() for p in files}
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in sorted(files)}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'portugal-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for name,d in inv.items():assert digest(z.read(name))==d['sha256'] and len(z.read(name))==d['bytes']
out={'status':'PASS','html_bytes':(R/'portugal-v1.html').stat().st_size,'glb_bytes':(R/'portugal.glb').stat().st_size,'zip_bytes':zpath.stat().st_size,'zip_sha256':digest(zpath.read_bytes()),'inventory_entries':len(inv),'required_artifact_subset':True,'zip_readback':True,'oversize_negative_rejected':negative}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print('DELIVERY PASS',json.dumps(out))
