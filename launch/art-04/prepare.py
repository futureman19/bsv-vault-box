import pathlib,json,subprocess,hashlib,io,zipfile,base64,struct
ROOT=pathlib.Path(__file__).resolve().parent
IDS='andorra austria belize bulgaria chad cuba ecuador fiji greece hungary israel kuwait liechtenstein malta mongolia netherlands oman peru rwanda senegal somalia suriname timor-leste uganda vatican-city'.split()
def blob(x):
 b=subprocess.check_output(['git','show',x['commit']+':'+x['path']]); assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'];return b
ledger=json.loads((ROOT/'parent-ledger.json').read_text());rows=[]
for e in ledger['entries']:
 if e['id'] not in IDS:continue
 dest=ROOT/'sources'/e['id'];dest.mkdir(parents=True,exist_ok=True)
 html=blob(e['viewer']); assert len(html)<5000000
 (dest/'marketing.webp').write_bytes(blob(e['marketing']))
 for key in ['source_readme','research_brief']:
  x=e['provenance'].get(key)
  if x:(dest/(key+'.md')).write_bytes(blob(x))
 models=[]
 for m in e['model_sources']:
  b=blob(m);models.append({'path':m['path'],'bytes':len(b),'sha256':m['sha256']})
  if m['path'].endswith('.glb'):
   assert base64.b64encode(b) in html
   assert struct.unpack_from('<I',b,8)[0]==len(b)
 archives=[]
 for a in e['source_archives']:
  b=blob(a) if a['kind']=='git' else pathlib.Path(a['path']).read_bytes()
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   assert z.testzip() is None
   names=z.namelist();assert len(names)==len(set(names)) and all(not n.startswith(('/', '\\')) and '..' not in pathlib.PurePosixPath(n).parts for n in names)
   mismatches=[]
   for m in [e['viewer']]+e['model_sources']:
    candidates=[n for n in names if n==pathlib.PurePosixPath(m['path']).name]
    if not candidates:candidates=[n for n in names if n.endswith('/'+pathlib.PurePosixPath(m['path']).name)]
    if not any(hashlib.sha256(z.read(n)).hexdigest()==m['sha256'] for n in candidates):
     mismatches.append({'path':m['path'],'candidate_members':candidates,'exact_byte_match':False})
   assert hashlib.sha256(b).hexdigest()==a['sha256']
   archives.append({'path':a['path'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'crc':'pass','required_payload_hashes':'hold' if mismatches else 'pass','mismatches':mismatches,'entries':len(names)})
 rows.append({'id':e['id'],'selection':e['selection'],'viewer':e['viewer'],'models':models,'archives':archives,'marketing':e['marketing'],'approval':e['approval'],'packaging':'hold' if any(a['mismatches'] for a in archives) else 'pass','status':'pending-visual-review'})
 print(e['id'],'packaging',rows[-1]['packaging'],flush=True)
assert len(rows)==25 and set(r['id'] for r in rows)==set(IDS)
(ROOT/'packaging-results.json').write_text(json.dumps(rows,indent=2)+'\n')
