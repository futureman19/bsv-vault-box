from pathlib import Path
import hashlib,json,zipfile,struct
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
required={'README.md','design-brief.md','kuwait.blend','kuwait.glb','kuwait-v1.html','mechanism.blend','poster.png','poster.jpg','author.py','author-helpers.txt','author-studio.txt','maps.py','build.py','run_checks.py','package_delivery.py','source-check.json','parity-check.json','theme-source-check.json','theme-check.json','browser-check.json','extended-check.json','checks.json','THREE-LICENSE.txt','desktop-closed.png','desktop-open.png','mobile-closed.png','mobile-open.png','maps/sadu-color.png','maps/sadu-roughness.png','maps/sand-color.png','maps/wood-color.png'}
def sha(b):return hashlib.sha256(b).hexdigest()
checks=json.loads((R/'checks.json').read_text());assert len(checks)==8 and all(x['status']=='PASS' for x in checks)
assert (R/'kuwait-v1.html').stat().st_size<5_000_000
glb=(R/'kuwait.glb').read_bytes();size=struct.unpack_from('<I',glb,12)[0];doc=json.loads(glb[20:20+size]);assert all('uri' not in x for x in doc.get('buffers',[])+doc.get('images',[]))
exclude={'inventory.json','delivery-check.json','kuwait-v1-source.zip'}
files={p.relative_to(R).as_posix():p for p in R.rglob('*') if p.is_file() and p.name not in exclude and p.suffix not in ['.blend1','.pyc'] and '__pycache__' not in p.parts and 'node_modules' not in p.parts}
assert required<=files.keys(),required-files.keys()
inv={k:{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for k,p in sorted(files.items())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
zpath=R/'kuwait-v1-source.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for name,p in sorted(files.items()):z.write(p,name)
 z.write(R/'inventory.json','inventory.json')
with zipfile.ZipFile(zpath) as z:
 assert set(z.namelist())==set(files)|{'inventory.json'}
 for name,m in inv.items():
  raw=z.read(name);assert len(raw)==m['bytes'] and sha(raw)==m['sha256'],name
 assert z.testzip() is None
# Test the exact packaged HTML bytes via its already-tested delivery path, without copies outside folder.
with zipfile.ZipFile(zpath) as z:assert z.read('kuwait-v1.html')==(R/'kuwait-v1.html').read_bytes()
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files']);c=b.new_context(offline=True,viewport={'width':390,'height':844},is_mobile=True,has_touch=True);p=c.new_page();errors=[];requests=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None);p.goto((R/'kuwait-v1.html').as_uri());p.wait_for_function('pilot.ready');p.locator('#open').tap();p.wait_for_function('pilot.progress===1');assert not errors and not requests;b.close()
out={'status':'PASS','html_bytes':(R/'kuwait-v1.html').stat().st_size,'glb_bytes':len(glb),'required_artifacts':sorted(required),'payload_file_count':len(inv),'all_archive_bytes_verified':True,'glb_no_external_uris':True,'exact_packaged_html_offline_mobile_open':True,'external_requests':requests,'page_errors':errors,'zip_bytes':zpath.stat().st_size,'zip_sha256':sha(zpath.read_bytes()),'inventory_sha256':sha((R/'inventory.json').read_bytes()),'self_hash_exclusions':sorted(exclude)}
(R/'delivery-check.json').write_text(json.dumps(out,indent=2)+'\n');print('DELIVERY PASS',json.dumps(out))
