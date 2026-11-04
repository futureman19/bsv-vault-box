from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
required={'australia-v1.html','australia.glb','australia.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','extended-check.json','theme-source-check.json','motion-output.txt','visual-check.json'}
exclude={'inventory.json','delivery-check.json','australia-v1-source.zip','package-output.txt','git-evidence.txt','staged-check.json'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in exclude and not p.name.endswith('.blend1'))
assert required<={p.relative_to(R).as_posix() for p in files}
html=(R/'australia-v1.html').read_bytes();glb=(R/'australia.glb').read_bytes()
def size_gate(size):assert size<5_000_000
size_gate(len(html))
try:size_gate(5_000_000)
except AssertionError:negative=True
else:raise AssertionError('Size gate accepted its ceiling')
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
for case in json.loads((R/'browser-check.json').read_text()):
 if 'asset' in case:assert not case['errors'] and not case['external_requests'] and case['asset']['degenerate']==0
 else:assert case['fallback']
for file in ['theme-source-check.json','extended-check.json','visual-check.json']:assert json.loads((R/file).read_text())['status']=='PASS'
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'australia-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for name,v in inv.items():assert len(z.read(name))==v['bytes'] and sha(z.read(name))==v['sha256']
result={'status':'PASS','html_bytes':len(html),'glb_bytes':len(glb),'html_sha256':sha(html),'glb_sha256':sha(glb),'payload_files':len(inv),'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath.read_bytes()),'zip_readback_all_hashes':True,'required_artifact_subset':True,'size_ceiling_negative_control':'REJECTED','inventory_excludes':'itself, ZIP, delivery check and post-package Git/log envelopes (no circular hashes)'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));print('ALL ACCEPTANCE CHECKS PASS')
