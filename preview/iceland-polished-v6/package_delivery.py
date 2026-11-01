from pathlib import Path
import json,hashlib,zipfile,shutil
R=Path(__file__).resolve().parent
D=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-iceland-polished-v6');D.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
before=json.loads((R/'preserved-inputs.json').read_text());changed=[p for p,h in before.items() if sha(Path(p).read_bytes())!=h];assert not changed,changed
assert (R/'motion.mjs').read_bytes()==(R.parent/'iceland-painted-v4/motion.mjs').read_bytes()
(R/'preservation-check.json').write_text(json.dumps({'checked_paths':len(before),'changed_paths':changed,'motion_module_byte_identical_to_v4':True},indent=2))
allowed={'.py','.js','.mjs','.html','.blend','.glb','.png','.jpg','.json','.txt','.md'}
files=sorted(p for p in R.rglob('*') if p.is_file() and p.suffix in allowed and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.name not in ['inventory.json','delivery-check.json'])
assert all('..' not in p.relative_to(R).parts for p in files)
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files}
z=R/'iceland-polished-v6-source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as archive:
 for p in files:archive.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(z) as archive:
 assert set(archive.namelist())==set(inv)
 for name,info in inv.items():assert sha(archive.read(name))==info['sha256']
inv[z.name]={'bytes':z.stat().st_size,'sha256':sha(z.read_bytes())}
(R/'inventory.json').write_text(json.dumps(inv,indent=2))
for p in files+[z,R/'inventory.json']:shutil.copy2(p,D/p.name) if p.parent==R else (D/p.relative_to(R)).parent.mkdir(parents=True,exist_ok=True) or shutil.copy2(p,D/p.relative_to(R))
for name,info in inv.items():assert sha((D/name).read_bytes())==info['sha256']
html=inv['iceland-polished-v6.html']['bytes'];assert html<5_000_000
result={'html_bytes':html,'glb_bytes':inv['iceland.glb']['bytes'],'blend_bytes':inv['iceland.blend']['bytes'],'source_zip_bytes':inv[z.name]['bytes'],'zip_members':len(files),'zip_readback_hashes':True,'delivery_readback_hashes':True,'html_budget_remaining':5_000_000-html,'delivery_directory':str(D),'primary_hashes':{n:inv[n] for n in ['iceland-polished-v6.html','iceland.glb','iceland.blend',z.name]}}
(R/'delivery-check.json').write_text(json.dumps(result,indent=2));shutil.copy2(R/'delivery-check.json',D/'delivery-check.json');assert (R/'delivery-check.json').read_bytes()==(D/'delivery-check.json').read_bytes();print(json.dumps(result,indent=2))
