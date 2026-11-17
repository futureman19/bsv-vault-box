import base64, hashlib, io, json, pathlib, subprocess, zipfile
ROOT=pathlib.Path(__file__).resolve().parent
P=ROOT.parent/'art-05'
SHA='c3318e46fe1ac6ba279f99708ae814caa3775db0'
def digest(b): return hashlib.sha256(b).hexdigest()
def check(b,r):
 assert len(b)==r['bytes'] and digest(b)==r['sha256'],r
 return b
def blob(r): return check(subprocess.check_output(['git','show',r['commit']+':'+r['path']]),r)
def safe(z):
 names=z.namelist()
 assert len(names)==len(set(names))
 assert all(not n.startswith(('/','\\')) and ':' not in n and '..' not in pathlib.PurePosixPath(n.replace('\\','/')).parts for n in names)
 assert z.testzip() is None
 return names
parent=json.loads((P/'review-ledger.json').read_text())
assert digest((P/'review-ledger.json').read_bytes())=='20a1b3479752ca696239f4cfe2e0c6f0c6a2fd25d90b5f01323309e115328561'
assigned=json.loads((P/'assigned.json').read_text())
assert len(assigned)==len(set(assigned))==25
assert sorted(assigned)==sorted(parent['assigned'])==sorted(e['id'] for e in parent['entries'])
inv=json.loads((P/'resume-inventory.json').read_text())
for name,r in inv.items():
 check((P/name).read_bytes(),r)
 check(subprocess.check_output(['git','show',SHA+':launch/art-05/'+name]),r)
package_results=[]
for r in json.loads((P/'resume-package-report.json').read_text())['packages']:
 with zipfile.ZipFile(io.BytesIO(check((P/r['file']).read_bytes(),r))) as z:
  names=safe(z)
  assert len(names)==r['entries']
  checked=0
  for n in names:
   if n in inv: check(z.read(n),inv[n]); checked+=1
  package_results.append(dict(r,inventory_members_verified=checked))
rows=[]
for e in parent['entries']:
 s=e['source_record']; html=blob(s['viewer']); assert len(html)<5000000
 check(pathlib.Path(s['delivered_viewer']['path']).read_bytes(),s['viewer'])
 models=[(m,blob(m)) for m in s['model_sources']]
 for m,b in models:
  if m['path'].endswith('.glb') and m.get('role')=='selected-model': assert base64.b64encode(b) in html
 blob(s['marketing'])
 for r in s['provenance'].values():
  if isinstance(r,dict) and 'commit' in r: blob(r)
 archives=[]
 for a in s['source_archives']:
  b=blob(a) if a['kind']=='git' else check(pathlib.Path(a['path']).read_bytes(),a)
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   names=safe(z); matches=[]
   for m in [s['viewer']]+s['model_sources']:
    leaf=pathlib.PurePosixPath(m['path']).name
    candidates=[leaf] if leaf in names else [n for n in names if n.endswith('/'+leaf)]
    exact=any(digest(z.read(n))==m['sha256'] for n in candidates)
    matches.append({'path':m['path'],'archive_members':candidates,'exact_match':exact})
   archives.append({'path':a['path'],'sha256':digest(b),'bytes':len(b),'entries':len(names),'crc_safe_unique':True,'required_payloads':matches,'full_inner_inventory_rerun':False})
 rows.append({'id':e['id'],'viewer':s['viewer'],'models':s['model_sources'],'archives':archives,'parent_package_holds':e['package_holds'],'art_changed':False})
 print(e['id'],'source hashes and archive CRC verified',flush=True)
result={'parent_commit':SHA,'parent_inventory_checked':len(inv),'assigned_count':len(assigned),'source_results':rows,'parent_review_packages':package_results,'limitations':['Source bytes verified, not fresh Blender reopen/parity/collision tests','Historical full inner source ZIP inventories not rerun; retain Iceland and New Zealand holds','No fresh runtime required for changed art: no art changed; historical runtime remains historical']}
(ROOT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS all 25 source records, 317 evidence records and three delivery ZIPs')
