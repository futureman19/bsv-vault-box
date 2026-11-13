from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,zipfile
R=Path(__file__).resolve().parent
checks={}
def load(n):return json.loads((R/n).read_text())
s=load('source-check.json');assert s['saved_source_reopened'] and s['collision_samples']==81 and not s['collisions'];checks['source']='PASS'
p=load('parity-check.json');assert p['source_and_export_geometry_match'] and max(p['source_to_glb_max'],p['glb_to_source_max'])<1e-5;checks['parity']='PASS'
assert load('theme-check.json')['status']=='PASS';checks['theme']='PASS'
assert load('motion-check.json')['status']=='PASS';checks['motion']='PASS'
b=load('browser-check.json');assert len(b)==3
for x in b[:2]:
 assert x['offline_file'] and x['open_close'] and x['rotation'] and x['reduced_motion'] and not x['errors'] and not x['external_requests'] and not x['overflow']
assert b[2]['fallback'];checks['browser']='PASS'
e=load('extended-check.json');assert e['status']=='PASS' and e['noJS_poster'];checks['extended']='PASS'
a=np.array(Image.open(R/'poster.png').convert('RGBA'));assert a[:,:,:3].max()>100 and (a[:,:,:3]>30).mean()>.05 and (a[:,:,3]>0).mean()>.1
color=np.array(Image.open(R/'maps/stone-color.png'));mean=color.mean(axis=(0,1));assert np.max(np.abs(mean-np.array([204,190,162])))<8
(R/'poster-check.json').write_text(json.dumps({'status':'PASS','width':a.shape[1],'height':a.shape[0],'nonblack_fraction':float((a[:,:,:3]>30).mean()),'alpha_coverage':float((a[:,:,3]>0).mean()),'stone_color_mean':mean.tolist()},indent=2));checks['poster']='PASS'
html=R/'monaco-v1.html';glb=R/'monaco.glb';assert html.stat().st_size<5000000;checks['budget']='PASS'
required={'monaco-v1.html','monaco.glb','monaco.blend','mechanism.blend','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','motion-check.json','theme-check.json','extended-check.json','maps/stone-color.png','maps/stone-normal.png','maps/stone-roughness.png','author.py','helpers.py','build.py','THREE-LICENSE.txt','.gitattributes'}
exclude={'inventory.json','delivery-check.json','monaco-v1-source.zip','package-output.txt','setup.py','lane-prompt.md'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in exclude and not any(x in p.relative_to(R).parts for x in ['node_modules','__pycache__']) and p.suffix!='.blend1')
manifest={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
assert required<=manifest.keys(),required-manifest.keys()
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'monaco-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
 for f in files:archive.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert set(archive.namelist())==set(manifest)|{'inventory.json'} and archive.testzip() is None
 for f in files:assert archive.read(f.relative_to(R).as_posix())==f.read_bytes()
checks['archive_readback']='PASS'
report={'status':'PASS','HTML_BYTES':html.stat().st_size,'GLB_BYTES':glb.stat().st_size,'ZIP_BYTES':z.stat().st_size,'ZIP_entries':len(files),'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'inventory_entries':len(manifest),'checks':checks,'inventory_self_exclusions':['inventory.json','delivery-check.json','monaco-v1-source.zip','package-output.txt'],'delivery':'in-folder standalone HTML and source ZIP; no external copy'}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
