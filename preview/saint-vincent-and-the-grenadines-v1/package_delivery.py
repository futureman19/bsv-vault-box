from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
excluded={'inventory.json','delivery-check.json','delivery-output.txt','source.zip'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in excluded and p.suffix not in ['.blend1','.pyc'])
required={'saint-vincent-and-the-grenadines-v1.html','saint-vincent-and-the-grenadines.glb','saint-vincent-and-the-grenadines.blend','poster.png','design-brief.md','README.md','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','motion-check.json','.gitattributes'}
assert required.issubset({p.name for p in files})
def sha(data):return hashlib.sha256(data).hexdigest()
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2),encoding='utf8')
with zipfile.ZipFile(R/'source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(R/'source.zip') as z:
 assert set(z.namelist())==set(inv)|{'inventory.json'}
 for n,v in inv.items():assert len(z.read(n))==v['bytes'] and sha(z.read(n))==v['sha256'],n
html=R/'saint-vincent-and-the-grenadines-v1.html';glb=R/'saint-vincent-and-the-grenadines.glb';assert html.stat().st_size<5_000_000
out={'status':'PASS','html_bytes':html.stat().st_size,'glb_bytes':glb.stat().st_size,'html_sha256':sha(html.read_bytes()),'glb_sha256':sha(glb.read_bytes()),'zip_bytes':(R/'source.zip').stat().st_size,'zip_sha256':sha((R/'source.zip').read_bytes()),'inventory_entries':len(inv),'required_artifacts_present':True,'every_zip_entry_hash_verified':True,'inventory_sha256':sha((R/'inventory.json').read_bytes()),'inventory_exclusions':sorted(excluded),'note':'Packaging envelopes excluded to avoid recursive hashes; node_modules/cache/backups excluded.'}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2),encoding='utf8');print('DELIVERY PASS',json.dumps(out,indent=2))
