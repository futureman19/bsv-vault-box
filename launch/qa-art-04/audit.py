import pathlib,json,hashlib,subprocess,zipfile,io,base64
R=pathlib.Path(__file__).resolve().parent;P=R/'parent'
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(d):
 b=subprocess.check_output(['git','show',d['commit']+':'+d['path']]);assert sha(b)==d['sha256'] and len(b)==d['bytes'];return b
parent=json.loads((P/'review-results.json').read_text()); ids=[e['id'] for e in parent['entries']]
assert len(ids)==len(set(ids))==25
assert sha((P/'review-results.json').read_bytes())=='7b9478928c8ba84ee6014132c2085dbad2e8ff44c4ae9b5197b593d6e3dd58cb'
inv=json.loads((P/'evidence-inventory.json').read_text())
inv=inv['files'] if 'files' in inv else [dict(path=k,**v) for k,v in inv.items()]
for f in inv:
 b=(P/f['path']).read_bytes();assert sha(b)==f['sha256'] and len(b)==f['bytes']
rows=[]
ledger=json.loads((P/'parent-ledger.json').read_text())
for e in ledger['entries']:
 if e['id'] not in ids:continue
 v=blob(e['viewer']);assert len(v)<5000000 and pathlib.Path(e['delivered_viewer']['path']).read_bytes()==v
 blob(e['marketing']); sources=[(m,blob(m)) for m in e['model_sources']]
 for m,b in sources:
  if m['path'].endswith('.glb'):assert base64.b64encode(b) in v
 row={'id':e['id'],'viewer':e['viewer'],'sources':e['model_sources'],'archives':[]}
 for a in e['source_archives']:
  b=blob(a) if a['kind']=='git' else pathlib.Path(a['path']).read_bytes();assert sha(b)==a['sha256'] and len(b)==a['bytes']
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
   assert all(not n.startswith(('/','\\')) and ':' not in n and '..' not in pathlib.PurePosixPath(n.replace('\\','/')).parts for n in names)
   checks=[]
   for m,raw in [(e['viewer'],v)]+sources:
    leaf=pathlib.PurePosixPath(m['path']).name;matches=[n for n in names if n==leaf] or [n for n in names if pathlib.PurePosixPath(n).name==leaf];assert len(matches)==1
    got=z.read(matches[0]);checks.append({'path':matches[0],'sha256':sha(got),'matches_selected_bytes':got==raw,'newline_only_difference':got!=raw and got.replace(b'\r\n',b'\n')==raw.replace(b'\r\n',b'\n')})
   name=min([n for n in names if pathlib.PurePosixPath(n).name=='inventory.json'],key=len); iv=json.loads(z.read(name)); prefix=str(pathlib.PurePosixPath(name).parent);prefix='' if prefix=='.' else prefix+'/'
   records=iv.get('files',iv)
   if isinstance(records,list):
    assert len({r.get('path',r.get('name')) for r in records})==len(records);records={r.get('path',r.get('name')):r for r in records}
   for n,m in records.items():
    raw=z.read(prefix+n);assert sha(raw)==m['sha256'] and len(raw)==m['bytes']
   row['archives'].append({'provenance':a,'safe_unique_crc':True,'selected_payload_checks':checks,'internal_inventory_checked':len(records)})
 rows.append(row)
assert len(rows)==25
out={'parent_evidence_hashes':len(inv),'entries':rows,'archive_inventory_members':sum(a['internal_inventory_checked'] for r in rows for a in r['archives'])}
(R/'packaging-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print('Verified',len(rows),'designs;',len(inv),'parent evidence hashes;',out['archive_inventory_members'],'archive members')
print('Mismatches',[(r['id'],c) for r in rows for a in r['archives'] for c in a['selected_payload_checks'] if not c['matches_selected_bytes']])
