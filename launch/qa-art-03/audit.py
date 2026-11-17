import pathlib,json,hashlib,subprocess,zipfile,io,base64
R=pathlib.Path(__file__).resolve().parent
P=R/'parent'
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(d):
 b=subprocess.check_output(['git','show',d['commit']+':'+d['path']]);assert sha(b)==d['sha256'] and len(b)==d['bytes'],d['path'];return b
parent=json.loads((P/'review-results.json').read_text());ids=json.loads((R/'assigned.json').read_text())
assert len(ids)==len(set(ids))==25 and parent['assigned']==ids
assert sha((P/'review-results.json').read_bytes())=='a4ef1d02b466c53cbc57c73655e67cf4097286740bf14964a394114744540c66'
inv=json.loads((P/'evidence-inventory.json').read_text())['files']
for f in inv:
 b=(P/f['path']).read_bytes();assert sha(b)==f['sha256'] and len(b)==f['bytes']
rows=[]
for e in json.loads((R/'launch-candidates.json').read_text())['entries']:
 if e['id'] not in ids:continue
 v=blob(e['viewer']);assert len(v)<5000000
 assert pathlib.Path(e['delivered_viewer']['path']).read_bytes()==v
 blob(e['marketing']);blob(e['provenance']['source_readme'])
 sources=[(m,blob(m)) for m in e['model_sources']]
 for m,b in sources:
  if m.get('role')=='selected-model' and m['path'].endswith('.glb'):assert base64.b64encode(b) in v
 row={'id':e['id'],'viewer':e['viewer'],'source_hashes':e['model_sources'],'archives':[]}
 for a in e['source_archives']:
  b=blob(a) if a['kind']=='git' else pathlib.Path(a['path']).read_bytes();assert sha(b)==a['sha256']
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   names=z.namelist();assert len(names)==len(set(names));assert z.testzip() is None
   assert all(not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts and '\\' not in n and ':' not in n for n in names)
   checks=[]
   for m,raw in [(e['viewer'],v)]+[(m,b) for m,b in sources if m.get('role')=='selected-model']:
    leaf=pathlib.PurePosixPath(m['path']).name
    matches=[n for n in names if n==leaf] or [n for n in names if pathlib.PurePosixPath(n).name==leaf]
    assert len(matches)==1,(e['id'],leaf,matches)
    got=z.read(matches[0]);checks.append({'path':matches[0],'sha256':sha(got),'matches_selected_bytes':got==raw,'newline_only_difference':got!=raw and got.replace(b'\r\n',b'\n')==raw.replace(b'\r\n',b'\n')})
   row['archives'].append({'path':a['path'],'kind':a['kind'],'sha256':sha(b),'bytes':len(b),'entries':len(names),'crc_and_safe_unique_paths':True,'selected_payload_checks':checks,'full_historical_inventory_freshly_checked':False,'inherited_inventory_checked':a.get('inventory_checked',False)})
 rows.append(row)
(R/'packaging-audit.json').write_text(json.dumps({'parent_inventory_verified':len(inv),'entries':rows},indent=2)+'\n')
print('Verified parent evidence:',len(inv),'designs:',len(rows))
print('Payload discrepancies:',[(r['id'],c) for r in rows for a in r['archives'] for c in a['selected_payload_checks'] if not c['matches_selected_bytes']])
