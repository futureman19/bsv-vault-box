import json, pathlib, subprocess, hashlib, io, zipfile, struct
R=pathlib.Path(__file__).resolve().parent
IDS='afghanistan armenia barbados botswana cameroon costa-rica dominica estonia georgia guyana iran kazakhstan lesotho malaysia micronesia namibia north-korea panama republic-of-the-congo san-marino slovakia spain tanzania turkey uruguay zimbabwe'.split()
ledger=json.loads((R/'launch-candidates.json').read_text()); entries=[e for e in ledger['entries'] if e['id'] in IDS]; assert len(entries)==len(set(IDS))==26
(R/'.gitattributes').write_text('* -text\n'); (R/'marketing').mkdir(exist_ok=True); (R/'source-notes').mkdir(exist_ok=True)
results=[]
def blob(d):
 b=subprocess.check_output(['git','show',d['commit']+':'+d['path']]); assert len(b)==d['bytes'] and hashlib.sha256(b).hexdigest()==d['sha256']; return b
for e in entries:
 s=e['id']; row={'id':s,'selection':e['selection'],'viewer':e['viewer'],'approval':e['approval'],'missing_gates':e['missing_gates'],'checks':[]}
 v=blob(e['viewer']); assert len(v)<5000000; row['checks'].append('viewer exact committed hash and strict size')
 (R/'marketing'/f'{s}.webp').write_bytes(blob(e['marketing']))
 (R/'source-notes'/f'{s}.md').write_bytes(blob(e['provenance']['source_readme']))
 for m in e['model_sources']:
  b=blob(m)
  if m['path'].endswith('.glb') and m.get('role')=='selected-model':
   n=struct.unpack_from('<I',b,12)[0]; g=json.loads(b[20:20+n]); assert struct.unpack_from('<I',b,8)[0]==len(b); assert all('uri' not in x for x in g.get('buffers',[])); row['glb_bytes']=len(b)
  row['checks'].append('exact source hash '+m['path'])
 row['archives']=[]
 for a in e['source_archives']:
  b=blob(a) if a['kind']=='git' else pathlib.Path(a['path']).read_bytes()
  assert hashlib.sha256(b).hexdigest()==a['sha256']
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   names=z.namelist(); assert len(names)==len(set(names)); assert all(not pathlib.PurePosixPath(n).is_absolute() and '..' not in pathlib.PurePosixPath(n).parts for n in names); assert z.testzip() is None
   required={pathlib.PurePosixPath(e['viewer']['path']).name}|{pathlib.PurePosixPath(m['path']).name for m in e['model_sources'] if m.get('role')=='selected-model'}
   assert required <= {pathlib.PurePosixPath(n).name for n in names}
  row['archives'].append({'path':a['path'],'sha256':a['sha256'],'bytes':len(b),'crc_safe_paths_required_payloads':True,'historical_full_inventory_checked':a.get('inventory_checked',False)})
 results.append(row); (R/'packaging-results.json').write_text(json.dumps(results,indent=2)+'\n'); print(s,'packaging pass',flush=True)
(R/'assigned.json').write_text(json.dumps(IDS,indent=2)+'\n')
