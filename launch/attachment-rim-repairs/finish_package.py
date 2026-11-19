"""Exact source packages with safe inventory readback; excludes dependencies/backups."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile,tempfile
R=Path(__file__).resolve().parents[2];D=R/'launch/attachment-rim-repairs/finish';O=D/'packages';O.mkdir(exist_ok=True)
rows=json.loads((D/'progress.json').read_text())['records'];results=[]
for row in rows:
 s=row['id'];root=(R/row['candidate']).parent
 folders=[D/s,D/'acceptance'/s]+([] if s=='iceland' else [root])
 files=set(p for folder in folders for p in folder.rglob('*') if p.is_file() and not any(v in p.parts for v in ['node_modules','__pycache__']) and p.suffix not in ['.blend1','.zip'])
 files.update((D.parent).glob('finish*.py'));files.update([D/'INDEPENDENT-REVIEW.md',D/'OWNER-PACKET.md',D/'targets.json',D/'progress.json',D/'acceptance/checks.json',D/'.gitattributes',D/'.gitignore'])
 required={R/row['candidate'],root/f'{s}.blend',root/f'{s}.glb',root/'motion.mjs',(D/s/'original/THREE-LICENSE.txt' if s=='iceland' else root/'THREE-LICENSE.txt'),D/s/'immutable-source.json',D/s/'original-review.json'}
 assert required<=files,(s,required-files)
 inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)}
 assert len(inv)==len(files)
 for n in inv:
  p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and '\\' not in n and ':' not in n
  assert all(c==c.rstrip(' .') and c.split('.')[0].upper() not in {'CON','PRN','AUX','NUL',*[f'COM{i}' for i in range(1,10)],*[f'LPT{i}' for i in range(1,10)]} for c in p.parts)
 zpath=O/f'{s}-final-source.zip';assert not zpath.exists()
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n in inv:z.write(R/n,n)
  z.writestr('INVENTORY.json',json.dumps(inv,indent=2))
 dest=Path(tempfile.mkdtemp(prefix=s+'-',dir=D/'recovered'))
 with zipfile.ZipFile(zpath) as z:
  assert len(z.namelist())==len(set(n.casefold() for n in z.namelist()))==len(inv)+1;assert z.testzip() is None
  for n,v in inv.items():
   b=z.read(n);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'];p=dest/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 for n,v in inv.items():assert hashlib.sha256((dest/n).read_bytes()).hexdigest()==v['sha256']
 record={'id':s,'zip':str(zpath.relative_to(R)),'zip_bytes':zpath.stat().st_size,'zip_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'payloads_hash_checked':len(inv),'exact_recovery':True,'recovered_viewer':str((dest/row['candidate']).resolve()),'inventory':inv}
 results.append(record);print(s,len(inv),zpath.stat().st_size,flush=True)
(O/'package-check.json').write_text(json.dumps(results,indent=2))
