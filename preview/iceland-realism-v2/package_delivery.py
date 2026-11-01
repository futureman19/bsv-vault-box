"""Allowlisted source delivery, verified ZIP and local output readback. No publication."""
from pathlib import Path
import hashlib,json,zipfile,shutil
R=Path(__file__).resolve().parent
OUT=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-iceland-realism-v2')
def info(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
names='README.md .gitattributes .gitignore author.py upgrade.py generate_textures.py test_textures.py build.py motion.mjs tests.mjs verify_source.py verify_browser.py verify_pbr.py verify_preservation.py package_delivery.py viewer.js viewer.bundle.js template.html package.json package-lock.json THREE-LICENSE.txt iceland.blend iceland.glb poster.png iceland-realism-v2.html desktop-closed.png desktop-open.png mobile-closed.png mobile-open.png mobile-fallback.png detail-basalt-brass.png detail-lid.png detail-hinge.png comparison-closed.jpg comparison-open.jpg before-closed-stage.png before-open-stage.png after-closed-stage.png after-open-stage.png before-desktop-closed.png before-desktop-open.png baseline-hashes.json browser-check.json pbr-check.json texture-check.json source-check.json preservation-check.json visual-review.json texture-red.txt texture-first-failure.txt texture-green.txt author-output.txt source-output.txt browser-output.txt pbr-output.txt pbr-camera-float-failure.txt motion-green.txt'.split()
names += ['diff-check-crlf-failure.txt']
names += [f'textures/{family}-{kind}.png' for family in ['basalt','lid','brass','interior'] for kind in ['color','normal','rough']]
names += ['first-browser-check/'+n for n in ['desktop-closed.png','desktop-open.png','browser-check.json','browser-output.txt','source-check.json']]
assert len(names)==len(set(names))
assert all((R/n).is_file() for n in names)
assert all(not any(s in n.lower() for s in ['.blend1','node_modules','.env','secret','wallet']) for n in names)
asset=json.loads((R/'browser-check.json').read_text())[0]['asset'];assert asset['bytes']==(R/'iceland.glb').stat().st_size
manifest={'schema':'boxsv-local-pbr-study/2','self_exclusion':'Manifest and archive/delivery envelopes excluded to avoid circular hashes.','provenance':'Procedurally authored real geometry and image maps; no scan, photo or AI image substitution. Local only.','model_metrics':asset,'files':{n:info(R/n) for n in sorted(names)}}
(R/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
zpath=R/'iceland-realism-v2-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n in sorted(names+['manifest.json']):z.write(R/n,n)
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(names+['manifest.json']) and z.testzip() is None
 for n,v in manifest['files'].items():
  b=z.read(n);assert hashlib.sha256(b).hexdigest()==v['sha256'] and len(b)==v['bytes']
 assert z.read('manifest.json')==(R/'manifest.json').read_bytes()
OUT.mkdir(parents=True,exist_ok=True)
for n in names+['manifest.json',zpath.name]:
 dest=OUT/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/n,dest);assert info(dest)==info(R/n)
report={'destination':str(OUT),'payload_files':len(names),'zip_entries':len(names)+1,'zip':info(zpath),'manifest':info(R/'manifest.json'),'all_archive_hashes_verified':True,'all_output_copies_readback_verified':True,'excluded':['.blend1','node_modules','secrets','__pycache__'],'published':False}
(R/'delivery-check.json').write_text(json.dumps(report,indent=2));shutil.copyfile(R/'delivery-check.json',OUT/'delivery-check.json');assert info(R/'delivery-check.json')==info(OUT/'delivery-check.json')
print(json.dumps(report,indent=2))
