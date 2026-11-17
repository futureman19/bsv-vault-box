import pathlib,json,hashlib,base64,html,zipfile
R=pathlib.Path(__file__).resolve().parent
ids=json.loads((R/'assigned.json').read_text());parent={e['id']:e for e in json.loads((R/'parent-ledger.json').read_text())['entries']}
visual={}
for p in sorted(R.glob('visual-*.json')):
 d=json.loads(p.read_text())
 for v in d.get('findings',d.get('results',[])):
  assert v['id'] not in visual
  visual[v['id']]={'report':p.name,'finding':v}
assert set(visual)==set(ids)
pack={e['id']:e for e in json.loads((R/'packaging-results.json').read_text())}
smoke=json.loads((R/'smoke-results.json').read_text());motion=json.loads((R/'motion-results.json').read_text());extended=json.loads((R/'extended-results.json').read_text())
assert len(smoke)==50 and all(e['result']=='pass' for e in smoke)
assert len(motion)==25 and all(e['passed'] for e in motion)
assert len(extended)==25
rows=[]
for s in ids:
 rows.append({'id':s,'status':'pass' if s=='cyprus' else 'needs-decision','review_complete':s=='cyprus','decision_reason': 'Bounded candidate only; independent next reviewer still required' if s=='cyprus' else 'Original-image visual review incomplete: vision provider HTTP 402 insufficient balance. Not an art defect verdict.','user_final_approved':False,'art_changed':False,'visual':visual[s],'packaging':pack[s],'source_record':parent[s],'captures':[f'smoke/{s}/{mode}-{pose}.png' for mode in ['desktop','mobile'] for pose in ['closed','open']],'historical_inventory_hold':s in ['iceland','new-zealand']})
report={'task':'t_f9d4b7e3','complete':False,'blocker':'Vision provider HTTP 402 insufficient_balance_error, confirmed directly by lead after delegate failures. No paid generation or funding action taken.','assigned':ids,'uncompleted_ids':[s for s in ids if s!='cyprus'],'tests':{'offline_desktop_mobile':50,'motion_suites':25,'no_js_fallback':25,'finite_loaded_geometry':25},'limitations':['No fresh Blender reopening/source parity/collision sampling','No corrupt-GLB fallback rerun','Full historical archive inventories not rerun; Iceland exact-byte discrepancy and Iceland/New Zealand historical holds retained','Emulated mobile, not physical phone','No new user approvals or release authorization'],'entries':rows}
(R/'partial-ledger.json').write_text(json.dumps(report,indent=2)+'\n')
parts=['<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>ART-05 partial review</title><style>body{background:#15161b;color:#eee;font:16px system-ui;margin:24px}img{width:100%;height:auto}section{margin:40px 0}p{max-width:900px}</style><h1>ART-05 — review incomplete</h1><p>25 candidates technically exercised; visual review interrupted by unavailable vision-provider credits. No artwork modified or approved. Comparisons distinguish promotional art from actual-model captures. This is an evidence report, not an interactive model.</p>']
for e in rows:
 parts.append('<section><h2>'+html.escape(e['id'])+'</h2><p>'+html.escape(e['decision_reason'])+'</p><img alt="Promotional versus desktop and mobile closed and open model comparison" src="data:image/jpeg;base64,'+base64.b64encode((R/'boards'/(e['id']+'.jpg')).read_bytes()).decode()+'"></section>')
(R/'partial-review.html').write_text(''.join(parts))
files=[p for p in R.rglob('*') if p.is_file() and p.name not in ['evidence-inventory.json','partial-evidence.zip'] and '__pycache__' not in p.parts]
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(files)}
(R/'evidence-inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
with zipfile.ZipFile(R/'partial-evidence.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[R/'evidence-inventory.json']:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(R/'partial-evidence.zip') as z:
 assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
 for n,m in inv.items():
  b=z.read(n);assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
print(json.dumps({'review_complete':False,'uncompleted':report['uncompleted_ids'],'inventory_files':len(inv),'zip_bytes':(R/'partial-evidence.zip').stat().st_size,'zip_sha256':hashlib.sha256((R/'partial-evidence.zip').read_bytes()).hexdigest()},indent=2))
