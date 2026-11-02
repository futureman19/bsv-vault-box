"""Safe explicit-required-set package, archive readback, copied offline viewer proof."""
from pathlib import Path
import hashlib,json,zipfile,shutil
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent;D=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-morocco-reference-v5');D.mkdir(exist_ok=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks={name:json.loads((R/(name+'.json')).read_text()) for name in ['preservation-check','source-preservation-check','source-check','parity-check','browser-check','extended-check','runtime-material-check','reference-check','fallback-check']}
assert checks['source-check']['collision_samples']==81 and checks['source-check']['collisions']==[]
assert checks['parity-check']['source_and_export_geometry_match'] and checks['reference-check']['all_nonbody_buffer_views_byte_identical']
assert checks['source-preservation-check']['source_packed_maps_match_finalizer_inputs']
assert checks['browser-check'][0]['asset']['bytes']==(R/'morocco.glb').stat().st_size
assert len(checks['fallback-check'])==4
assert (R/'morocco-reference-v5.html').stat().st_size<5_000_000
# Read raw GLB maps back and ensure source/finalizer payload identity.
from glb_tools import load,view
j,bb=load(R/'morocco.glb')
for idx,name in [(3,'reference-normal.png'),(4,'reference-color.png'),(5,'reference-orm.png')]:assert view(j,bb,j['images'][idx]['bufferView'])==(R/'maps'/name).read_bytes()
audit={'technical_acceptance':'passed listed bounded checks','visual_acceptance':'Closer to original in dusty reddish palette and thin irregular strata; candidate awaiting user review, not exact match.','remaining_visual_differences':['Lighter/pinker and flatter than original under unchanged viewer lighting','Pale front-left corner and local patch joins remain','Some fine vein registration differs; hidden back/right mirrored extrapolation','Nonbody original-art discrepancies intentionally untouched'],'swatches':2,'selected':'B','post_model_corrections':1,'html_bytes':(R/'morocco-reference-v5.html').stat().st_size,'glb_bytes':(R/'morocco.glb').stat().st_size,'actual_gltf_map_bytes_match_source_inputs':True,'checks':list(checks),'source_export_max_error':checks['parity-check']['source_to_glb_max'],'prior_failure':'Inherited extended map dimension/normal range assumption failed. Corrected to bounded physical-aspect texel budget/nonzero subtle normal range; all actual geometry/render gates retained.'}
(R/'final-audit.json').write_text(json.dumps(audit,indent=2))
required={'.gitattributes','morocco-reference-v5.html','morocco.glb','morocco.blend','baseline/morocco.glb','baseline/morocco.blend','poster.png','poster.jpg','README.md','author.py','materials.py','finalize_glb.py','glb_tools.py','build.py','viewer.js','viewer.bundle.js','motion.mjs','template.html','package.json','THREE-LICENSE.txt','reference-comparison.jpg','body-closeup-comparison.jpg','texture-swatch-board.jpg','references/primary-morocco.png','references/hardware-shadow-mask.png','references/front-rectified-mask.png','references/left-rectified-mask.png','references/front-rectified-observed.png','references/left-rectified-observed.png','maps/reference-color.png','maps/reference-normal.png','maps/reference-orm.png','material-provenance.json','reference-check.json','source-check.json','source-preservation-check.json','parity-check.json','browser-check.json','fallback-check.json','final-audit.json','verify_reference.py','package_delivery.py'}
exclude={'inventory.json','delivery-check.json'}
files=[p for p in R.rglob('*') if p.is_file() and (p.suffix in {'.py','.js','.mjs','.json','.html','.glb','.blend','.png','.jpg','.md','.txt'} or p.name=='.gitattributes') and p.name not in exclude and '__pycache__' not in p.parts and 'node_modules' not in p.parts]
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p)} for p in sorted(files)}
assert required<=inventory.keys(),required-inventory.keys()
(R/'inventory.json').write_text(json.dumps(inventory,indent=2));files.append(R/'inventory.json');z=R/'morocco-reference-v5-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
 for p in files:archive.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert required<=set(archive.namelist())
 assert all(not n.startswith(('/','\\')) and '..' not in Path(n).parts and ':' not in n for n in archive.namelist())
 for name,entry in inventory.items():assert hashlib.sha256(archive.read(name)).hexdigest()==entry['sha256'] and len(archive.read(name))==entry['bytes']
files.append(z)
for p in files:
 target=D/p.relative_to(R);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);assert digest(target)==digest(p)
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files']);c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();requests=[];errors=[];p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None);p.on('pageerror',lambda e:errors.append(str(e)));p.goto((D/'morocco-reference-v5.html').as_uri());p.wait_for_function('pilot.ready');assert p.evaluate('pilot.asset.bytes')==(D/'morocco.glb').stat().st_size;p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.locator('#reset').click();p.wait_for_function('pilot.progress===0');p.screenshot(path=str(D/'delivery-opened-offline.png'));assert not requests and not errors;b.close()
result={'copied_files':len(files),'zip_inventory_entries_verified':len(inventory),'required_artifacts_verified':sorted(required),'delivery_html_offline_open_reset':True,'requests':requests,'errors':errors,'html_bytes':(D/'morocco-reference-v5.html').stat().st_size,'glb_bytes':(D/'morocco.glb').stat().st_size,'blend_bytes':(D/'morocco.blend').stat().st_size,'zip_bytes':z.stat().st_size,'sha256':{f:digest(D/f) for f in ['morocco-reference-v5.html','morocco.glb','morocco.blend',z.name]}}
for root in [R,D]:(root/'delivery-check.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
