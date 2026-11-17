import pathlib,json,hashlib,subprocess,zipfile,io,base64
R=pathlib.Path(__file__).resolve().parent;P=R/'parent';REF='431e51ffb5a8704b5f8f8b11694d28befae18402'
def sha(b):return hashlib.sha256(b).hexdigest()
def check(b,x):
 assert len(b)==x['bytes'] and sha(b)==x['sha256'],x
 return b
def blob(x):return check(subprocess.check_output(['git','show',x['commit']+':'+x['path']]),x)
def safe(names):
 assert len(names)==len(set(names))
 assert all(not n.startswith(('/','\\')) and ':' not in n and '\\' not in n and '..' not in pathlib.PurePosixPath(n).parts for n in names)
ledger=json.loads((P/'review-results.json').read_text());ids=[e['id'] for e in ledger['entries']];assert len(ids)==len(set(ids))==25
assert sha((P/'review-results.json').read_bytes())=='aa405e3726554049a6dcb73b8a23d24f7b0d759d8cad3235ed40c1494846a979'
inv=json.loads((P/'evidence-inventory.json').read_text())
for n,x in inv.items():
 check((P/n).read_bytes(),x);check(subprocess.check_output(['git','show',REF+':launch/art-08/'+n]),x)
delivery=json.loads((P/'delivery.json').read_text());zips=[]
for d in [delivery]+delivery['delivery_parts']:
 b=check(pathlib.Path(d['path']).read_bytes(),d)
 with zipfile.ZipFile(io.BytesIO(b)) as z:
  safe(z.namelist());assert z.testzip() is None
  for n in z.namelist():assert z.read(n)==(P/n).read_bytes(),n
  zips.append({**d,'members_verified':len(z.namelist())})
original={e['id']:e for e in json.loads((P/'parent-ledger.json').read_text())['entries']};rows=[]
for e in ledger['entries']:
 s=original[e['id']];html=blob(s['viewer']);assert len(html)<5000000
 check(pathlib.Path(s['delivered_viewer']['path']).read_bytes(),s['viewer'])
 for m in s['model_sources']:
  b=blob(m)
  if m['path'].endswith('.glb') and m['role']=='selected-model':assert base64.b64encode(b) in html
 blob(s['marketing'])
 for c in e['reviewed_image_hashes']:check((P/c['path']).read_bytes(),c)
 assert len(e['browser'])==2 and all(c['sha256']==s['viewer']['sha256'] for c in e['browser'])
 archives=[]
 for a in s['source_archives']:
  b=blob(a) if a['kind']=='git' else check(pathlib.Path(a['path']).read_bytes(),a)
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   names=z.namelist();safe(names);assert z.testzip() is None;required=[]
   for m in [s['viewer']]+s['model_sources']:
    leaf=pathlib.PurePosixPath(m['path']).name
    candidates=[n for n in names if n==leaf] or [n for n in names if n.endswith('/'+leaf)]
    match=[n for n in candidates if sha(z.read(n))==m['sha256']];assert match,(s['id'],m['path'])
    required.append({'path':m['path'],'member':match[0],'sha256':m['sha256']})
   ni=min([n for n in names if pathlib.PurePosixPath(n).name=='inventory.json'],key=len)
   prefix=str(pathlib.PurePosixPath(ni).parent);prefix='' if prefix=='.' else prefix+'/'
   records=json.loads(z.read(ni));records=records.get('files',records)
   if isinstance(records,list):
    assert len({r.get('path',r.get('name')) for r in records})==len(records)
    records={r.get('path',r.get('name')):r for r in records}
   for n,x in records.items():check(z.read(prefix+n),x)
   archives.append({**a,'fresh_required_payloads':required,'fresh_inner_inventory_entries':len(records),'fresh_crc_safe_unique':True})
 rows.append({'id':s['id'],'viewer':s['viewer'],'models':s['model_sources'],'archives':archives,'captures_bound_to_viewer':True,'delivered_viewer_exact':True,'marketing':s['marketing'],'result':'pass'})
 print(s['id'],'PASS',flush=True)
result={'parent_commit':REF,'parent_evidence_hashes':len(inv),'parent_zips':zips,'source_checks':rows,'fresh_runtime':False,'fresh_source_reopen':False,'full_inner_inventories_fresh':True,'inner_inventory_entries':sum(a['fresh_inner_inventory_entries'] for r in rows for a in r['archives'])}
(R/'audit-results.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS',len(rows),len(inv),len(zips),result['inner_inventory_entries'])
