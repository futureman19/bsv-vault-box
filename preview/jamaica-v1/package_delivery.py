from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def budget(n):assert n<5_000_000,'HTML exceeds strict byte budget'
budget((R/'jamaica-v1.html').stat().st_size)
try:budget(5_000_000)
except AssertionError:negative=True
else:raise AssertionError('Budget negative accepted')
source=json.loads((R/'source-check.json').read_text());assert source['collision_samples']==81 and not source['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
browser=json.loads((R/'browser-check.json').read_text());assert {x['case'] for x in browser}=={'desktop','mobile','corrupted GLB'}
for c in browser[:2]:assert not c['errors'] and not c['external_requests'] and c['open_close'] and c['reduced_motion']
assert 'PASS motion' in (R/'motion-output.txt').read_text()
required={'design-brief.md','README.md','jamaica-v1.html','jamaica.glb','jamaica.blend','mechanism.blend','author.py','maps.py','poster.png','poster.jpg','source-check.json','theme-check.json','parity-check.json','browser-check.json','extended-check.json','.gitattributes'}
files=[p for p in R.rglob('*') if p.is_file() and not set(p.relative_to(R).parts)&{'node_modules','__pycache__'} and p.suffix not in {'.zip','.blend1','.blend2'} and p.name not in {'inventory.json','delivery-check.json','package-output.txt','staged-check.json'}]
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(files)}
assert required<=set(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
zpath=R/'jamaica-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for n in [*inv,'inventory.json']:z.write(R/n,n)
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():
  b=z.read(n);assert len(b)==v['bytes'] and sha(b)==v['sha256'],n
 assert z.read('inventory.json')==(R/'inventory.json').read_bytes()
result={'status':'PASS','html_bytes':(R/'jamaica-v1.html').stat().st_size,'glb_bytes':(R/'jamaica.glb').stat().st_size,'payload_files':len(inv),'required_artifacts_present':True,'archive_readback_hashes_match':True,'oversize_negative_rejected':negative,'archive_bytes':zpath.stat().st_size,'archive_sha256':sha(zpath.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'excluded_envelopes':['inventory.json','delivery-check.json','source ZIP','package-output.txt','staged-check.json'],'scope':'Local art only; no chain, public deployment or production changes'}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
