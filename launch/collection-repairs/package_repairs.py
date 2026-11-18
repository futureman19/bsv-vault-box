"""New exact-byte source packages. Never rewrite historical archives or approvals."""
from pathlib import Path, PurePosixPath
import hashlib,io,json,re,subprocess,zipfile,argparse
ROOT=Path(__file__).resolve().parent
IDS=('iceland','morocco','rwanda','namibia','new-zealand','paraguay')
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(src):
 return subprocess.check_output(['git','show',src['commit']+':'+src['path']])
def safe_names(names):
 seen=set()
 for n in names:
  p=PurePosixPath(n)
  assert n and '\\' not in n and not p.is_absolute() and str(p)==n and all(x not in ('.','..') and x.rstrip(' .')==x and ':' not in x and not re.match(r'(?i)^(con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)',x) for x in p.parts),('unsafe path',n)
  assert n.casefold() not in seen,('duplicate/alias',n)
  seen.add(n.casefold())
def manifest(files):return {n:{'bytes':len(b),'sha256':sha(b)} for n,b in sorted(files.items())}
def encode(obj):return (json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()
def archive(files,path):
 safe_names(files)
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for n,b in sorted(files.items()):
   i=zipfile.ZipInfo(n,(2026,1,1,0,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o100644<<16;z.writestr(i,b)
def recover(path,expected,out):
 assert not out.exists(),'fresh destination required'
 with zipfile.ZipFile(path) as z:
  safe_names(z.namelist());raw=z.read('inventory.json');assert sha(raw)==expected,'untrusted inventory'
  inv=json.loads(raw);assert set(z.namelist())==set(inv['files'])|{'inventory.json'},'exact member set'
  assert inv['required'] and set(inv['required'])<=set(inv['files']),'mandatory roles'
  assert all(any(n.endswith(ext) for n in inv['required']) for ext in ('.html','.blend','.glb')),'required payload types'
  files={n:z.read(n) for n in inv['files']}
  for n,b in files.items():assert inv['files'][n]=={'bytes':len(b),'sha256':sha(b)},('hash/size',n)
 out.mkdir(parents=True)
 for n,b in {**files,'inventory.json':raw}.items():
  p=out/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);assert p.read_bytes()==b
 return {'members':len(files)+1,'readback':True}
def old_inventory(files):
 inv=files.get('inventory.json')
 if inv is None:return {'status':'absent-historical-inventory','all_members_freshly_inventoried':len(files)}
 d=json.loads(inv);rows=d.get('files',d)
 if isinstance(rows,list):rows={r.get('path',r.get('name')):r for r in rows}
 checked=[]
 for n,r in rows.items():
  if not isinstance(r,dict) or 'sha256' not in r:continue
  assert n in files and sha(files[n])==r['sha256'],('old inventory',n)
  size=r.get('bytes',r.get('size'))
  if size is not None:assert len(files[n])==size
  checked.append(n)
 assert checked,'unsupported/empty old inventory'
 return {'status':'pass','entries_checked':len(checked),'uninventoried_members':sorted(set(files)-set(checked))}
def build(out):
 assert not out.exists(),'fresh output directory required';out.mkdir(parents=True)
 ledger_bytes=(ROOT/'baseline-ledger.json').read_bytes();ledger=json.loads(ledger_bytes)
 assert len(ledger['entries'])==201 and len({e['id'] for e in ledger['entries']})==201
 results=[]
 for ident in IDS:
  e=next(x for x in ledger['entries'] if x['id']==ident)
  ar=next(f for f in e['files'] if f['role']=='historical-source-archive');raw=blob(ar['source']);assert sha(raw)==ar['sha256'] and len(raw)==ar['bytes']
  with zipfile.ZipFile(io.BytesIO(raw)) as z:
   safe_names(z.namelist());assert z.testzip() is None
   files={n:z.read(n) for n in z.namelist()}
  original_files=dict(files)
  oldcheck=old_inventory(files);changes=[];required=[]
  if 'inventory.json' in files:files['historical/original-inventory.json']=files.pop('inventory.json')
  sourcefolder=PurePosixPath(ar['source']['path']).parent
  for f in e['files']:
   if f['role'] not in ('viewer','model','editable-source','historical-editable-source','source-notice'):continue
   b=blob(f['source']);assert sha(b)==f['sha256'] and len(b)==f['bytes']
   n=str(PurePosixPath(f['source']['path']).relative_to(sourcefolder))
   if n in files and files[n]!=b:
    prior=files[n];files['historical/replaced/'+n]=prior
    changes.append({'path':n,'before':manifest({n:prior})[n],'after':manifest({n:b})[n],'newline_only':prior.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n')})
   files[n]=b;required.append(n)
  if ident in ('iceland','morocco','rwanda'):assert len(changes)==1 and changes[0]['path'].endswith('.html') and changes[0]['newline_only']
  else:assert not changes
  notice={'id':ident,'historical_archive':ar,'baseline_ledger_sha256':sha(ledger_bytes),'historical_inventory_check':oldcheck,'canonical_replacements':changes,'art_changed':False,'final_approved':False,'limits':'New complete inventory and canonical selected payloads. Historical evidence unchanged under historical/; not fresh art/mechanical acceptance, rights clearance, permanent availability or launch approval.'}
  files['PACKAGE-REPAIR.json']=encode(notice);files.setdefault('.gitattributes',b'* -text\n')
  for old_name,old_bytes in original_files.items():
   preserved_name='historical/original-inventory.json' if old_name=='inventory.json' else ('historical/replaced/'+old_name if files.get(old_name)!=old_bytes else old_name)
   assert files[preserved_name]==old_bytes,('original member lost',old_name)
  inv=encode({'version':1,'id':ident,'required':required,'files':manifest(files)})
  files['inventory.json']=inv
  path=out/(ident+'-canonical-source-v1.zip');archive(files,path)
  check=recover(path,sha(inv),out/(ident+'-recovered'))
  for n in required:assert (out/(ident+'-recovered')/n).read_bytes()==files[n]
  results.append({**notice,'archive':path.name,'archive_bytes':path.stat().st_size,'archive_sha256':sha(path.read_bytes()),'inventory_sha256':sha(inv),'recovery':check})
 report={'ids':list(IDS),'packages':results,'approved':0,'originals_modified':False}
 (out/'report.json').write_bytes(encode(report));print(json.dumps(report,indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('output',type=Path);p.add_argument('--recover',type=Path);p.add_argument('--expected-inventory-sha256');a=p.parse_args()
 if a.recover:
  if not a.expected_inventory_sha256:p.error('--expected-inventory-sha256 is required for recovery')
  print(json.dumps(recover(a.recover,a.expected_inventory_sha256,a.output)))
 else:build(a.output)
