"""Exact required-set inventory, embedded-payload verification and ZIP readback."""
from pathlib import Path
import hashlib,json,zipfile,base64,re
R=Path(__file__).resolve().parent
required={'benin-v1.html','benin.glb','benin.blend','mechanism.blend','poster.png','poster.jpg','README.md','design-brief.md','maps.py','author.py','build.py','verify_all.py','verify_source.py','verify_parity.py','verify_theme.py','verify_browser.py','verify_extended.py','package_delivery.py','viewer.js','viewer.bundle.js','template.html','motion.mjs','tests.mjs','package.json','THREE-LICENSE.txt','source-check.json','parity-check.json','theme-check.json','browser-check.json','extended-check.json','acceptance-check.json','hinge-attachment-check.json','desktop-closed.png','desktop-open.png','desktop-open-rear.png','mobile-closed.png','mobile-open.png','mobile-nojs.png','mobile-fallback.png','maps/earth-color.png','maps/earth-roughness.png','maps/straw-color.png'}
def digest(b):return hashlib.sha256(b).hexdigest()
html=(R/'benin-v1.html').read_bytes();glb=(R/'benin.glb').read_bytes();assert len(html)<5_000_000
text=html.decode();embedded=base64.b64decode(re.search(r'<script id="asset"[^>]*>(.*?)</script>',text,re.S).group(1));assert embedded==glb
poster=base64.b64decode(re.search(r'src="data:image/jpeg;base64,([^"]+)"',text).group(1));assert poster==(R/'poster.jpg').read_bytes()
assert not re.search(r'(?:src|href)=["\']https?://',text)
checks=json.loads((R/'acceptance-check.json').read_text());assert len(checks)==7 and all(x['status']=='PASS' and x['exit_code']==0 for x in checks)
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in ['inventory.json','delivery-check.json','benin-v1-source.zip'] and not p.name.endswith(('.blend1','.pyc'))}
assert required<=files.keys(),sorted(required-files.keys())
inv={n:{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for n,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2));files['inventory.json']=R/'inventory.json'
zpath=R/'benin-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,p in sorted(files.items()):z.write(p,n)
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(files)
 for n,p in files.items():assert z.read(n)==p.read_bytes(),n
 for n,v in inv.items():assert digest(z.read(n))==v['sha256'] and len(z.read(n))==v['bytes']
r={'status':'PASS','html_bytes':len(html),'glb_bytes':len(glb),'html_sha256':digest(html),'glb_sha256':digest(glb),'embedded_glb_exact':True,'embedded_poster_exact':True,'required_artifacts':sorted(required),'inventory_entries':len(inv),'zip_entries':len(files),'zip_bytes':zpath.stat().st_size,'zip_sha256':digest(zpath.read_bytes()),'inventory_sha256':digest((R/'inventory.json').read_bytes()),'zip_readback_all_bytes_match':True,'hash_exclusions':['inventory.json hashes payload but not itself','delivery-check.json and ZIP are envelopes excluded from inventory to avoid recursion']}
(R/'delivery-check.json').write_text(json.dumps(r,indent=2));print('DELIVERY PASS');print('HTML_BYTES',len(html),'GLB_BYTES',len(glb));print('ZIP_BYTES',r['zip_bytes'],'INVENTORY_ENTRIES',r['inventory_entries'])
