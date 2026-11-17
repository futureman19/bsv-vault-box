import pathlib,json,hashlib,zipfile,io,subprocess
R=pathlib.Path(__file__).resolve().parent
rows=json.loads((R/'packaging-results.json').read_text());out=[]
for e in rows:
 for a in e['archives']:
  b=pathlib.Path(a['path']).read_bytes() if pathlib.Path(a['path']).is_absolute() else subprocess.check_output(['git','show',e['selection']['commit']+':'+a['path']])
  assert hashlib.sha256(b).hexdigest()==a['sha256']
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   names=z.namelist();assert len(names)==len(set(names)) and z.testzip() is None
   assert all(not n.startswith(('/','\\')) and ':' not in n and '..' not in pathlib.PurePosixPath(n.replace('\\','/')).parts for n in names)
   candidates=[n for n in names if pathlib.PurePosixPath(n).name=='inventory.json'];assert candidates
   n=min(candidates,key=len); inv=json.loads(z.read(n)); prefix=str(pathlib.PurePosixPath(n).parent);prefix='' if prefix=='.' else prefix+'/'
   records=inv.get('files',inv)
   if isinstance(records,list):
    assert len({r.get('path',r.get('name')) for r in records})==len(records)
    records={r.get('path',r.get('name')):r for r in records}
   for name,m in records.items():
    payload=z.read(prefix+name);assert len(payload)==m['bytes'] and hashlib.sha256(payload).hexdigest()==m['sha256'],(e['id'],name)
   out.append({'id':e['id'],'archive':a,'inventory_entries_checked':len(records),'internal_inventory':'pass','selected_payload_match':a['required_payload_hashes']})
print('Checked',len(out),'archives;',sum(r['inventory_entries_checked'] for r in out),'inventory entries')
(R/'archive-results.json').write_text(json.dumps(out,indent=2)+'\n')
