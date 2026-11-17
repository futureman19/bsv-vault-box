import pathlib,json,hashlib
R=pathlib.Path(__file__).resolve().parent
rows=[]
for p in sorted(R.glob('visual-group-*.json')):
 for e in json.loads(p.read_text()):
  if 'status' not in e:
   assert e['decision'] in ('pass','needs-decision')
   e['status']=e['decision']
  e['delegated_recommendation']=e['status']
  if e['status']=='pass bounded candidate':e['status']='pass'
  assert e['status'] in ('pass','needs-decision')
  assert len(e['inspected_paths'])==5
  hashes=[]
  for name in e['inspected_paths']:
   q=pathlib.Path(name)
   if not q.is_absolute():
    q=R.parents[1]/q if name.startswith('launch/') else R/q
   assert q.is_file(),q
   hashes.append({'path':q.relative_to(R).as_posix(),'sha256':hashlib.sha256(q.read_bytes()).hexdigest(),'bytes':q.stat().st_size})
  e['reviewed_image_hashes']=hashes
  e['bounded_candidate_disposition']=e['status']
  e['user_final_approved']=False
  rows.append(e)
assert len(rows)==len({e['id'] for e in rows})==25
(R/'visual-findings.json').write_text(json.dumps(rows,indent=2)+'\n')
print('25 records, 125 original inspected paths bound to current frozen hashes; group 1 decision field normalized to status')
