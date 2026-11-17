import pathlib,json,hashlib,subprocess,zipfile,io,base64
R=pathlib.Path(__file__).resolve().parent
P=R/'parent'; REF='0a99711872c208041b6602f0462675cd1b1a0d0c'
def sha(b):return hashlib.sha256(b).hexdigest()
def check(b,x):
 assert len(b)==x['bytes'] and sha(b)==x['sha256'],x
 return b
def blob(x):return check(subprocess.check_output(['git','show',x['commit']+':'+x['path']]),x)
def safe(names):
 assert len(names)==len(set(names))
 assert all(not n.startswith(('/','\\')) and ':' not in n and '\\' not in n and '..' not in pathlib.PurePosixPath(n).parts for n in names)
ledger=json.loads((P/'review-ledger.json').read_text()); ids=json.loads((P/'assigned.json').read_text()); assert len(ids)==len(set(ids))==25
assert {e['id'] for e in ledger['entries']}==set(ids)
assert sha((P/'review-ledger.json').read_bytes())=='baf49accb3d67684735f0e4d9561decb2bc1fd33bc6b97a6919a7cc1ae46f68f'
inv=json.loads((P/'evidence-inventory.json').read_text())
for n,x in inv.items():
 check((P/n).read_bytes(),x);check(subprocess.check_output(['git','show',REF+':launch/art-07/'+n]),x)
zips=[]
for p in P.glob('*.zip'):
 with zipfile.ZipFile(p) as z:
  safe(z.namelist());assert z.testzip() is None
  for n in z.namelist():assert z.read(n)==(P/n).read_bytes(),(p,n)
  zips.append({'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'members':len(z.namelist()),'all_members_match':True})
original={e['id']:e for e in json.loads((P/'parent-ledger.json').read_text())['entries']};rows=[]
for e in ledger['entries']:
 s=original[e['id']]; html=blob(s['viewer']);assert len(html)<5000000
 check(pathlib.Path(s['delivered_viewer']['path']).read_bytes(),s['viewer'])
 for m in s['model_sources']:
  b=blob(m)
  if m['path'].endswith('.glb'):assert base64.b64encode(b) in html
 blob(s['marketing'])
 for c in e['captures']:
  check((P/c['path']).read_bytes(),c);assert c['viewer_sha256']==s['viewer']['sha256']
 archives=[]
 for a in s['source_archives']:
  b=blob(a) if a['kind']=='git' else check(pathlib.Path(a['path']).read_bytes(),a)
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   names=z.namelist();safe(names);assert z.testzip() is None
   required=[]
   for m in [s['viewer']]+s['model_sources']:
    leaf=pathlib.PurePosixPath(m['path']).name
    candidates=[n for n in names if n==leaf] or [n for n in names if n.endswith('/'+leaf)]
    match=[n for n in candidates if sha(z.read(n))==m['sha256']]
    assert match,(s['id'],m['path']);required.append({'path':m['path'],'member':match[0],'sha256':m['sha256']})
   archives.append({**a,'fresh_crc_safe_unique':True,'fresh_required_payloads':required,'full_inner_inventory_fresh':False})
 rows.append({'id':s['id'],'viewer':s['viewer'],'models':s['model_sources'],'archives':archives,'captures_bound_to_viewer':True,'delivered_viewer_exact':True,'marketing':s['marketing'],'result':'pass'})
 print(s['id'],'source/archive/capture hash pass',flush=True)
result={'parent_commit':REF,'parent_evidence_hashes':len(inv),'parent_zips':zips,'source_checks':rows,'fresh_runtime':False,'fresh_source_reopen':False,'full_inner_inventories_fresh':False}
(R/'audit-results.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS',len(rows),len(inv),len(zips))
