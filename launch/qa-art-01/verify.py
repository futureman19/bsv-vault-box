"""Independent read-only verification of pinned parent bytes and selected archives."""
import base64, hashlib, io, json, pathlib, struct, subprocess, zipfile
R=pathlib.Path(__file__).resolve().parent
P=R/'launch/art-01'
COMMIT='6f59f7c47540284a1470f8451db90b6d070d6171'
def sha(b): return hashlib.sha256(b).hexdigest()
def git(c,p): return subprocess.check_output(['git','show',c+':'+p])
def check(d):
 b=git(d['commit'],d['path']) if d.get('kind','git')=='git' else pathlib.Path(d['path']).read_bytes()
 assert len(b)==d['bytes'] and sha(b)==d['sha256'], d['path']
 return b
parent=json.loads((P/'review-results.json').read_text())
assigned=json.loads((P/'assigned.json').read_text())
assert len(assigned)==len(set(assigned))==26
assert sorted(assigned)==sorted(e['id'] for e in parent['entries'])
assert not parent['changed_designs'] and not parent['unreviewed']
inventory=json.loads((P/'evidence-inventory.json').read_text())['files']
for item in inventory:
 b=git(COMMIT,'launch/art-01/'+item['path'])
 assert sha(b)==item['sha256'] and len(b)==item['bytes'],item['path']
 assert (P/item['path']).read_bytes()==b
ledger=json.loads((P/'launch-candidates.json').read_text())
rows=[]
for e in ledger['entries']:
 if e['id'] not in assigned: continue
 row={'id':e['id'],'selection':e['selection'],'viewer':e['viewer'],'sources':e['model_sources'],'archives':[]}
 v=check(e['viewer']); assert len(v)<5000000
 assert pathlib.Path(e['delivered_viewer']['path']).read_bytes()==v
 check(e['marketing']); check(e['provenance']['source_readme'])
 required={pathlib.PurePosixPath(e['viewer']['path']).name:v}
 for d in e['model_sources']:
  b=check(d)
  if d.get('role')=='selected-model': required[pathlib.PurePosixPath(d['path']).name]=b
  if d['path'].endswith('.glb') and d.get('role')=='selected-model':
   assert b[:4]==b'glTF' and struct.unpack_from('<II',b,4)==(2,len(b))
   n=struct.unpack_from('<I',b,12)[0]; g=json.loads(b[20:20+n])
   assert all('uri' not in x for x in g.get('buffers',[]))
   assert base64.b64encode(b) in v
 for a in e['source_archives']:
  b=check(a)
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   names=z.namelist(); assert len(names)==len(set(names))
   for name in names:
    p=pathlib.PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts and '\\' not in name and ':' not in name
   assert z.testzip() is None
   matches={}
   for name,data in required.items():
    options=[x for x in names if x==name] or [x for x in names if pathlib.PurePosixPath(x).name==name]
    exact=[x for x in options if z.read(x)==data]
    assert exact,(e['id'],name,'missing exact selected payload')
    matches[name]=exact
   row['archives'].append({'path':a['path'],'commit':a.get('commit'),'sha256':sha(b),'bytes':len(b),'members':len(names),'crc_safe_unique':True,'exact_selected_payloads':matches,'full_inventory_rerun':False,'inherited_full_inventory_checked':a.get('inventory_checked',False)})
 row.update(passed=True,delivered_viewer_exact=True,embedded_glb_exact=True)
 rows.append(row)
 print(e['id'],'PASS',flush=True)
result={'parent_commit':COMMIT,'parent_remote_sha':subprocess.check_output(['git','ls-remote','--heads','origin','feature/art-01-review'],text=True).split()[0],'parent_inventory_files_verified':len(inventory),'assigned':assigned,'reviewed':len(rows),'entries':rows,'scope':'Fresh hash/size, exact selected HTML/GLB/BLEND archive member bytes, ZIP CRC/path, embedded GLB; not full internal ZIP inventory or Blender geometry parity.'}
assert result['parent_remote_sha']==COMMIT
(R/'verification-results.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS',len(rows),'designs;',len(inventory),'parent evidence files')
