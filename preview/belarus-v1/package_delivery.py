from pathlib import Path
import hashlib,json,zipfile
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent
checks={}
s=json.loads((R/'source-check.json').read_text());assert s['saved_source_reopened'] and s['collision_samples']==81 and not s['collisions'] and s['moving_meshes']>34;checks['source_motion']='PASS'
p=json.loads((R/'parity-check.json').read_text());assert max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5;checks['parity']='PASS'
t=json.loads((R/'theme-check.json').read_text());assert t['status']=='PASS' and t['warp']==21 and t['weft']==13 and t['pivots_preserved'];checks['theme']='PASS'
b=json.loads((R/'browser-check.json').read_text());assert [r['case'] for r in b]==['desktop','mobile','corrupted GLB']
for r in b[:2]:
 assert r['offline_file'] and not r['errors'] and not r['external_requests'] and r['open_close'] and r['reset_mid_motion'] and r['reduced_motion'] and not r['overflow']
 assert r['asset']['nonfinite']==r['asset']['degenerate']==0 and r['asset']['open_projection_max_abs_ndc']<1
assert b[1]['touch_rotation'] and b[2]['fallback'];checks['browser']='PASS'
e=json.loads((R/'extended-check.json').read_text());assert e['status']=='PASS' and e['noJS_poster'];checks['extended']='PASS'
assert '# fail 0' in (R/'motion-output.txt').read_text() and '# pass 2' in (R/'motion-output.txt').read_text();checks['motion_unit']='PASS'
assert 'AssertionError: Detached ribbon rejected' in (R/'theme-negative.txt').read_text();checks['negative_control']='PASS'
a=np.array(Image.open(R/'maps/cedar-color.png'));med=np.median(a,axis=(0,1));assert 185<=med[0]<=215 and 140<=med[1]<=180 and 65<=med[2]<=105
im=np.array(Image.open(R/'poster.png').convert('RGB'));assert im.max()>150 and np.mean(im)>10;checks['palette_poster']='PASS'
h=(R/'belarus-v1.html').stat().st_size;g=(R/'belarus.glb').stat().st_size;assert h<5_000_000;checks['size']='PASS'
(R/'acceptance-check.json').write_text(json.dumps({'status':'PASS','checks':checks,'palette_median':med.tolist()},indent=2))
exclude={'inventory.json','delivery-check.json','belarus-v1-source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix!='.blend1' and p.name not in exclude)
required={'belarus-v1.html','belarus.glb','belarus.blend','mechanism.blend','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','poster.png'}
assert required<={p.relative_to(R).as_posix() for p in files}
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json');z=R/'belarus-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as f:
 for p in files:f.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as f:
 assert set(f.namelist())=={p.relative_to(R).as_posix() for p in files} and f.testzip() is None
 for p in files:assert f.read(p.relative_to(R).as_posix())==p.read_bytes()
report={'status':'PASS','HTML_BYTES':h,'GLB_BYTES':g,'ZIP_BYTES':z.stat().st_size,'ZIP_ENTRIES':len(files),'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'archive_readback_verified':True,'required_artifacts_present':True,'checks':checks}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
