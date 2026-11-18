from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,tempfile
R=Path(__file__).resolve().parents[2];out=R/'launch/attachment-rim-repairs';reports=[]
helpers=['resume_repair.py','resume_preservation.py','resume_contacts.py','resume_capture_before.py','resume_supplemental.py','resume_package.py','resume_recovery_browser.py']
for slug in ['algeria','guyana']:
 root=R/'preview'/f'{slug}-repair-v2'
 if not root.exists():continue
 files=[p for p in root.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.zip']]
 files += [out/n for n in helpers+['.gitattributes','CONTINUATION-2.md','resume-independent-review.md','OWNER-DECISIONS.md','continuation-ledger-v2.json','resume-supplemental-check.json']]
 required={root/f'{slug}.blend',root/f'{slug}.glb',root/f'{slug}-repair-v2.html',root/'historical-v1'/f'{slug}.blend',root/'THREE-LICENSE.txt',root/'tests.mjs'}
 assert required.issubset(files)
 inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
 assert len(inv)==len(files)
 for n in inv:
  p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and '\\' not in n and ':' not in n and '.env' not in p.parts
  assert all(c==c.rstrip(' .') for c in p.parts)
 zpath=out/f'{slug}-repair-v2-source.zip'
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(files):z.write(p,p.relative_to(R).as_posix())
  z.writestr('INVENTORY.json',json.dumps(inv,indent=2))
 parent=out/'resume-recovered';parent.mkdir(exist_ok=True);dest=Path(tempfile.mkdtemp(prefix=slug+'-',dir=parent))
 with zipfile.ZipFile(zpath) as z:
  names=z.namelist();assert len(names)==len(set(n.casefold() for n in names))==len(inv)+1;assert z.testzip() is None
  for n,v in inv.items():
   b=z.read(n);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'];p=dest/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
  (dest/'INVENTORY.json').write_bytes(z.read('INVENTORY.json'))
 for n,v in inv.items():assert hashlib.sha256((dest/n).read_bytes()).hexdigest()==v['sha256']
 reports.append({'id':slug,'zip':zpath.name,'zip_bytes':zpath.stat().st_size,'zip_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'payloads_hash_checked':len(inv),'required_artifacts_present':True,'exact_recovery':True,'recovered_viewer':str((dest/root.relative_to(R)/f'{slug}-repair-v2.html').resolve()),'inventory':inv})
(out/'resume-package-check.json').write_text(json.dumps(reports,indent=2));print([{k:v for k,v in r.items() if k!='inventory'} for r in reports])
