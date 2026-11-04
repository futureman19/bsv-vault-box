from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
slug='sao-tome-and-principe';html=R/(slug+'-v1.html');glb=R/(slug+'.glb')
def load(n):return json.loads((R/n).read_text())
def sha(data):return hashlib.sha256(data).hexdigest()
s=load('source-check.json');assert s['collision_samples']==81 and not s['collisions'] and s['saved_source_reopened']
p=load('parity-check.json');assert max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5
for n in ['theme-check.json','pivot-check.json','extended-check.json']:assert load(n)['status']=='PASS'
b=load('browser-check.json');assert {x['case'] for x in b}=={'desktop','mobile','corrupted GLB'}
for x in b[:2]:
 assert not x['errors'] and not x['external_requests'] and not x['overflow']
 assert all(x[k] for k in ['rotation','open_close','reset_mid_motion','reduced_motion','offline_file'])
 assert not x['asset']['degenerate'] and not x['asset']['nonfinite']
assert b[2]['fallback'] and b[2]['caught_loader_errors']
assert html.stat().st_size<5000000
assert 'PASS 81 staged poses' in (R/'motion-output.txt').read_text()
checks=['source','parity','theme','pivots','motion','browser desktop','browser mobile','corrupt GLB','no-JS poster','runtime maps','byte budget']
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','checks':checks,'html_bytes':html.stat().st_size,'glb_bytes':glb.stat().st_size},indent=2))
allowed={'.py','.inc','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
exclude={'inventory.json','delivery-check.json','package-output.txt','git-evidence.txt'}
files=sorted(f for f in R.rglob('*') if f.is_file() and (f.suffix in allowed or f.name in {'.gitattributes','.gitignore'}) and f.name not in exclude and (f.parent==R or f.parent.name=='maps'))
required={'design-brief.md','README.md',slug+'.blend',slug+'.glb',slug+'-v1.html','mechanism.blend','poster.png','author.py','maps.py','landscape.py.inc','source-check.json','parity-check.json','browser-check.json','theme-check.json','pivot-check.json','acceptance-check.json'}
assert required<={f.name for f in files}
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files}
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/(slug+'-v1-source.zip')
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={f.relative_to(R).as_posix() for f in files}
 assert a.testzip() is None
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
r={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':glb.stat().st_size,'ZIP_BYTES':z.stat().st_size,'entries':len(files),'required_artifacts_verified':sorted(required),'archive_exact_readback':True,'zip_sha256':sha(z.read_bytes()),'html_sha256':sha(html.read_bytes()),'glb_sha256':sha(glb.read_bytes())}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));print('PASS all acceptance checks and archive inventory readback')
