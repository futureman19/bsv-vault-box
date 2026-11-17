import base64,hashlib,html,json,pathlib,zipfile
R=pathlib.Path(__file__).resolve().parent; P=R.parent/'art-05'
def sha(b):return hashlib.sha256(b).hexdigest()
p=json.loads((P/'review-ledger.json').read_text()); v=json.loads((R/'verification.json').read_text())
visual={e['id']:e for f in sorted(R.glob('visual-*.json')) for e in json.loads(f.read_text())['entries']}
assert len(visual)==25 and set(visual)==set(p['assigned'])
rows=[]
for e in p['entries']:
 a=visual[e['id']]; paths=a.get('images_inspected',a.get('inspected_paths'))
 assert len(paths)==5 and len(set(paths))==5
 captures=[]
 for name in paths:
  f=pathlib.Path(name)
  if not f.exists(): f=P/name
  assert f.exists(),name
  captures.append({'path':f.resolve().relative_to(P).as_posix(),'sha256':sha(f.read_bytes()),'parent_commit':v['parent_commit']})
 held=e['status']!='pass' or a['verdict']=='needs-user-review'
 rows.append({'id':e['id'],'verdict':'needs-user-review' if held else 'candidate-with-limitations','review_complete':True,'user_final_approved':False,'launch_ready':False,'art_changed':False,'visual_review':a,'parent_reason':e['decision_reason'],'package_holds':e['package_holds'],'source_record':e['source_record'],'inspected_images':captures,'fresh_checks':next(x for x in v['source_results'] if x['id']==e['id']),'historical_runtime_only':True,'missing_gates':e['source_record']['missing_gates']})
held=[e['id'] for e in rows if e['verdict']=='needs-user-review']
assert held==['azerbaijan','chile','iceland','lithuania','new-zealand','pacific-ocean','saint-kitts-and-nevis','venezuela']
d={'task':'t_aac80afa','parent_task':'t_f9d4b7e3','parent_commit':v['parent_commit'],'assigned':p['assigned'],'unreviewed_ids':[],'reviewed':len(rows),'candidate_with_limitations':len(rows)-len(held),'needs_user_review':held,'final_approvals':0,'critical_reproducible_defects':[],'art_changed':False,'limitations':v['limitations']+['All original desktop/mobile closed/open images inspected by five independent visual workers; lead Venezuela spot check','No new browser, motion, Blender or fallback execution in QA; immutable prior evidence hash verified','Static hinge readability is unresolved, not proven mechanical failure','All final user approval, storage and release gates remain'],'entries':rows}
(R/'reviewed-ledger.json').write_text(json.dumps(d,indent=2)+'\n')
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BoxSV batch 5 independent review</title><style>body{background:#17191b;color:#eee;font:16px system-ui;max-width:1400px;margin:auto;padding:20px}img{width:100%;height:auto}article{border-top:1px solid #666;padding:20px 0}p{max-width:90ch}h2{color:#e2bd78}</style><h1>Batch 5 — independent candidate review</h1><p>25 designs reviewed. 17 candidates with limitations; eight unresolved user/package holds. Zero final approvals. No art edited.</p><p>Comparison boards: promotional illustration, desktop closed/open, mobile closed/open. Original images independently inspected and bound to immutable parent hashes; boards are scaled evidence, not calibrated material comparisons. No fresh runtime or source-mechanism tests in this QA pass.</p>']
for e in rows:
 b=(P/'boards'/f"{e['id']}.jpg").read_bytes()
 parts.append('<article><h2>'+html.escape(e['id']+' — '+e['verdict'])+'</h2><p>'+html.escape(e['parent_reason'])+'</p><p>'+html.escape('; '.join(e['package_holds']))+'</p><img alt="'+html.escape(e['id'])+' promotional and actual-model comparison" src="data:image/jpeg;base64,'+base64.b64encode(b).decode()+'"></article>')
parts.append('</html>');(R/'review.html').write_text(''.join(parts),encoding='utf-8')
(R/'.gitattributes').write_text('* -text\n')
(R/'README.md').write_text('# QA-ART-05\n\nIndependent bounded review of all 25 unchanged candidates. See reviewed-ledger.json for exact refs, SHA-256, per-ID findings and holds. 17 candidates with limitations; eight needs-user-review; zero final approvals.\n\nFresh: 125 original image inspections, 317 parent inventory files checked locally and against committed blobs; 25 viewer/model/source/marketing records and ZIP CRC/safe-path/required-payload checks; all three parent review ZIPs checked. Iceland selected archive mismatch and Iceland/New Zealand full historical inventory holds preserved. Full inner source inventories were not rerun. Runtime, motion, source parity and collision evidence remains historical, not fresh QA. No art changed, no deployment, paid generation, minting or funds.\n\nParent: feature/art-05 at '+v['parent_commit']+'. Immutable original captures and source reports remain there under launch/art-05. This report ZIP carries the new QA ledger and self-contained comparison HTML, not the original art payloads or full-resolution captures.\n\nNext: consolidation must preserve all eight holds and final user approval/storage/release gates.\n')
files=[f for f in R.iterdir() if f.is_file() and f.name not in ['inventory.json','qa-art-05-report.zip','package.json']]
inv={f.name:{'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in files}
(R/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
with zipfile.ZipFile(R/'qa-art-05-report.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in files+[R/'inventory.json']:z.write(f,f.name)
with zipfile.ZipFile(R/'qa-art-05-report.zip') as z:
 assert len(z.namelist())==len(set(z.namelist()))==len(files)+1 and z.testzip() is None
 for name,r in inv.items():assert len(z.read(name))==r['bytes'] and sha(z.read(name))==r['sha256']
report={'ledger_sha256':sha((R/'reviewed-ledger.json').read_bytes()),'html_bytes':(R/'review.html').stat().st_size,'zip_bytes':(R/'qa-art-05-report.zip').stat().st_size,'zip_sha256':sha((R/'qa-art-05-report.zip').read_bytes()),'inventory_entries':len(inv),'reviewed':len(rows),'held':held}
(R/'package.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
