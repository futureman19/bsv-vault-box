import pathlib,json,hashlib,base64,html,zipfile,collections
R=pathlib.Path(__file__).resolve().parent
def load(n):return json.loads((R/n).read_text())
def save(n,x):(R/n).write_text(json.dumps(x,indent=2)+'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
ids=load('assigned.json'); parent={e['id']:e for e in load('parent-ledger.json')['entries']}; visual={}
for p in sorted(R.glob('visual-*.json')):
 d=json.loads(p.read_text()); v=d.get('findings',d.get('reviews')); v=list(v.values()) if isinstance(v,dict) else v
 for e in v:
  assert e['id'] not in visual; visual[e['id']]=e
assert set(visual)==set(ids) and len(ids)==len(set(ids))==25
package={e['id']:e for e in load('packaging-results.json')}; motion={e['id']:e for e in load('motion-results.json')}; extended={e['id']:e for e in load('extended-results.json')}; smoke=load('smoke-results.json'); rows=[]
for s in ids:
 e=parent[s]; v=visual[s]; captures=[]
 for mode in ['desktop','mobile']:
  for pose in ['closed','open']:
   path=f'smoke/{s}/{mode}-{pose}.png';b=(R/path).read_bytes(); captures.append({'path':path,'bytes':len(b),'sha256':sha(b),'viewer_sha256':e['viewer']['sha256']})
 checks=[x for x in smoke if x['id']==s];assert len(checks)==2 and all(x['result']=='pass' for x in checks)
 assert motion[s]['passed'] and package[s]['packaging']=='pass' and e['viewer']['bytes']<5000000
 rows.append({'id':s,'verdict':v['verdict'],'final_approval':False,'art_changed':False,'polish_iterations':0,'selection':e['selection'],'viewer':e['viewer'],'models':package[s]['models'],'source_archives':package[s]['archives'],'marketing':e['marketing'],'captures':captures,'visual':v,'browser':checks,'motion':motion[s],'extended':extended[s],'inherited_approval':e['approval'],'inherited_visual_limitations':e['visual_limitations'],'inherited_missing_gates':e['missing_gates'],'fresh_source_reopen_parity_collision':False,'fresh_corrupt_glb_fallback':False,'launch_ready':False})
counts=dict(collections.Counter(x['verdict'] for x in rows))
save('review-ledger.json',{'task':'t_95c2129e','parent_commit':'6db6388d04fee0da8e0324a640d5880a5813a39c','scope':'Unchanged-candidate bounded review; no final art approvals. Promotional detail differs from runtime. No fresh Blender/collision or corrupt-GLB fallback assertions.','counts':counts,'unreviewed_ids':[],'entries':rows})
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>ART-07 review</title><style>body{background:#18191d;color:#eee;font:16px system-ui;margin:24px auto;max-width:1200px;padding:0 14px}img{width:100%;height:auto}section{margin:30px 0;border-top:1px solid #777;padding-top:15px}pre{white-space:pre-wrap;overflow-wrap:anywhere}small{color:#ccc}</style><h1>ART-07 · 25 candidate reviews</h1><p>'+html.escape(str(counts))+'</p><p>No art edits or final approval. Seven visual decisions remain; passing checks do not establish promotional equivalence. Images: promotional illustration, then actual desktop/mobile closed/open. Full originals and exact refs/hashes are in the evidence ZIPs.</p>']
for e in rows:
 s=e['id'];parts.append('<section><h2>'+html.escape(s)+' · '+e['verdict']+'</h2><small>Offline viewer '+str(e['viewer']['bytes'])+' bytes · '+e['selection']['commit']+'</small><img alt="'+s+' promotional versus actual model comparison" src="data:image/jpeg;base64,'+base64.b64encode((R/'boards'/f'{s}.jpg').read_bytes()).decode()+'"><pre>'+html.escape(json.dumps(e['visual'],indent=2))+'</pre></section>')
parts.append('</html>');(R/'review.html').write_text(''.join(parts))
(R/'README.md').write_text('# ART-07 bounded candidate review\n\n'+json.dumps(counts)+'\n\nAll 25 assigned IDs reviewed; no art changed or final approvals. Every unchanged viewer is below 5,000,000 bytes. Fresh gates: 50 offline desktop/mobile interaction cases, 25 motion suites, 25 no-JS poster/finite-loaded-geometry checks, 25 source-package CRC/required-payload comparisons. Original 125 images inspected by delegated visual reviewers; parent reinspected seven held comparison boards.\n\nSeven visual holds: '+', '.join(e['id'] for e in rows if e['verdict']=='needs-decision')+'. These are artistic fidelity/readability decisions, not demonstrated functional malfunctions. No scoped repair was justified without choosing a substantial artistic target. Preserve original candidates.\n\nSource ZIPs/model/viewer refs are recorded, not duplicated. Archive verification covers CRC, safe/unique entries, and required viewer/model payload hashes; full inner source inventories remain historical. Existing parent missing gates preserved per ID. No fresh Blender reopen/parity/collision, corrupt-GLB fallback, real-phone performance or release certification claimed.\n\nreview.html is a self-contained comparison report, not the collectible. review-ledger.json carries per-ID exact refs, hashes, sizes, captures and decisions. Desktop/mobile ZIPs retain original PNGs unchanged. review-evidence.zip includes ledger, scripts, boards, source notices, motion evidence and full inventory; excludes captures (separate ZIPs), source models, dependencies and ZIPs themselves. No docs/production/deployment/mint/funds changes. Next: pre-created QA-ART-07 independently checks final files and retains all holds.\n')
files=[p for p in R.rglob('*') if p.is_file() and p.suffix!='.zip' and p.name not in ['evidence-inventory.json','package-report.json'] and '__pycache__' not in p.parts]
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in files};save('evidence-inventory.json',inv)
reports=[]
for name,selection in [('review-evidence.zip',[p for p in files if 'smoke' not in p.relative_to(R).parts]+[R/'evidence-inventory.json']),('review-desktop-captures.zip',[p for p in files if 'smoke' in p.relative_to(R).parts and p.name.startswith('desktop-')]),('review-mobile-captures.zip',[p for p in files if 'smoke' in p.relative_to(R).parts and p.name.startswith('mobile-')])]:
 with zipfile.ZipFile(R/name,'w',zipfile.ZIP_DEFLATED) as z:
  for p in selection:z.write(p,p.relative_to(R).as_posix())
 with zipfile.ZipFile(R/name) as z:
  assert len(z.namelist())==len(set(z.namelist()))==len(selection) and z.testzip() is None
  for p in selection:assert z.read(p.relative_to(R).as_posix())==p.read_bytes()
 b=(R/name).read_bytes();reports.append({'path':name,'bytes':len(b),'sha256':sha(b),'entries':len(selection),'readback':'pass'})
save('package-report.json',reports)
print(json.dumps({'counts':counts,'report_bytes':(R/'review.html').stat().st_size,'viewer_min':min(e['viewer']['bytes'] for e in rows),'viewer_max':max(e['viewer']['bytes'] for e in rows),'packages':reports},indent=2))
