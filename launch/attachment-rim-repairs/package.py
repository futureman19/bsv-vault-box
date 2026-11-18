from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,shutil,tempfile
R=Path(__file__).resolve().parents[2];out=R/'launch/attachment-rim-repairs';reports=[]
for slug in ['ghana','chile']:
 root=R/'preview'/f'{slug}-repair-v2'
 if not root.exists():continue
 files=[p for p in root.rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.zip']]
 files += list(out.glob('*.py'))+list(out.glob('*.md'))+[out/'continuation-ledger.json',out/'supplemental-check.json']
 required={root/f'{slug}.blend',root/f'{slug}.glb',root/f'{slug}-repair-v2.html',root/'historical-v1'/f'{slug}.blend',root/'THREE-LICENSE.txt'}
 assert required.issubset(files)
 inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files}
 assert all('.env' not in PurePosixPath(n).parts for n in inv)
 manifest=json.dumps(inv,indent=2).encode();zpath=out/f'{slug}-repair-v2-source.zip'
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in sorted(files):z.write(p,p.relative_to(R).as_posix())
  z.writestr('INVENTORY.json',manifest)
 parent=out/'recovered';parent.mkdir(exist_ok=True)
 dest=Path(tempfile.mkdtemp(prefix=slug+'-',dir=parent))
 with zipfile.ZipFile(zpath) as z:
  names=z.namelist();assert len(names)==len(set(n.casefold() for n in names)) and len(names)==len(inv)+1
  assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n and ':' not in n for n in names)
  assert z.testzip() is None
  for n,v in inv.items():
   b=z.read(n);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'];p=dest/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
  (dest/'INVENTORY.json').write_bytes(z.read('INVENTORY.json'))
 for n,v in inv.items():assert hashlib.sha256((dest/n).read_bytes()).hexdigest()==v['sha256']
 reports.append({'id':slug,'zip':zpath.name,'zip_bytes':zpath.stat().st_size,'zip_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'members':len(inv)+1,'payloads_hash_checked':len(inv),'required_artifacts_present':True,'exact_recovery':True,'recovered_viewer':str((dest/root.relative_to(R)/f'{slug}-repair-v2.html').resolve()),'inventory':inv})
(out/'package-check.json').write_text(json.dumps(reports,indent=2));print([{k:v for k,v in r.items() if k!='inventory'} for r in reports])
