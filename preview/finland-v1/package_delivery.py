from pathlib import Path
import json,hashlib,zipfile
from PIL import Image
import numpy as np
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
required={'finland.blend','finland.glb','finland-v1.html','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','negative-control.txt','motion-output.txt'}
assert required.issubset({p.name for p in R.iterdir()})
assert not json.loads((R/'source-check.json').read_text())['collisions']
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
assert json.loads((R/'extended-check.json').read_text())['status']=='PASS'
assert '# fail 0' in (R/'motion-output.txt').read_text()
assert 'AssertionError: Ornament detached from lid' in (R/'negative-control.txt').read_text()
assert (R/'finland-v1.html').stat().st_size<5_000_000
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.5 and im[:,:,:3].max()>100
files=sorted(p for p in R.rglob('*') if p.is_file() and (p.parent==R or p.parent==R/'maps') and p.suffix not in ['.zip','.blend1'] and p.name not in ['inventory.json','delivery-check.json'])
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
assert required.issubset(inv)
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files.append(R/'inventory.json')
z=R/'finland-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for p in files:a.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert set(a.namelist())=={p.relative_to(R).as_posix() for p in files};assert a.testzip() is None
 for p in files:assert a.read(p.relative_to(R).as_posix())==p.read_bytes()
r=dict(status='PASS',HTML_BYTES=(R/'finland-v1.html').stat().st_size,GLB_BYTES=(R/'finland.glb').stat().st_size,ZIP_BYTES=z.stat().st_size,zip_sha256=sha(z.read_bytes()),inventory_entries=len(inv),archive_entries=len(files),archive_readback=True,required_artifacts=sorted(required),poster_nontransparent_fraction=float((im[:,:,3]>0).mean()))
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('DELIVERY PASS',json.dumps(r))
