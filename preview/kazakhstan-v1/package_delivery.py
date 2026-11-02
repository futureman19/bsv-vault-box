from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
required={'kazakhstan-v1.html','kazakhstan.glb','kazakhstan.blend','mechanism.blend','author.py','maps.py','build.py','viewer.js','viewer.bundle.js','motion.mjs','template.html','poster.png','poster.jpg','design-brief.md','README.md','source-check.json','parity-check.json','browser-check.json','theme-check.json','motion-output.txt','verify_source.py','verify_parity.py','verify_browser.py','verify_extended.py','tests.mjs','THREE-LICENSE.txt','package.json','maps/felt-color.png','maps/felt-roughness.png','maps/wood-color.png'}
assert (R/'kazakhstan-v1.html').stat().st_size<5_000_000
s=json.loads((R/'source-check.json').read_text());assert not s['collisions'] and s['collision_samples']==81
assert json.loads((R/'parity-check.json').read_text())['source_and_export_geometry_match']
assert json.loads((R/'contract-check.json').read_text())['status']=='PASS'
assert json.loads((R/'theme-check.json').read_text())['status']=='PASS'
required.update({'contract-check.json','verify_contract.py','hinge-attachment-check.json'})
b=json.loads((R/'browser-check.json').read_text());assert len(b)==3
for case in b[:2]:assert case['offline_file'] and not case['errors'] and not case['external_requests'] and case['asset']['degenerate']==0
assert b[2]['fallback']
allowed={'.py','.js','.mjs','.json','.md','.txt','.html','.png','.jpg','.blend','.glb'}
files=sorted(f for f in R.rglob('*') if f.is_file() and (f.suffix in allowed or f.name=='.gitattributes') and f.name not in {'inventory.json','delivery-check.json','lane-prompt.md'} and (f.parent==R or f.parent.name in {'maps','initial'}))
manifest={f.relative_to(R).as_posix():{'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files}
assert required<=set(manifest),required-set(manifest)
(R/'inventory.json').write_text(json.dumps(manifest,indent=2));files.append(R/'inventory.json')
z=R/'kazakhstan-v1-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in files:a.write(f,f.relative_to(R).as_posix())
with zipfile.ZipFile(z) as a:
 assert required<=set(a.namelist());assert len(a.namelist())==len(files);assert a.testzip() is None
 for f in files:assert a.read(f.relative_to(R).as_posix())==f.read_bytes()
out={'status':'PASS','HTML_BYTES':(R/'kazakhstan-v1.html').stat().st_size,'GLB_BYTES':(R/'kazakhstan.glb').stat().st_size,'ZIP_BYTES':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'inventory_entries':len(manifest),'archive_entries':len(files),'required_inventory_verified':True,'every_archived_byte_readback_verified':True,'delivery':'in-folder artifacts; HTML tested here over offline file://','manifest_sha256':hashlib.sha256((R/'inventory.json').read_bytes()).hexdigest()}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
