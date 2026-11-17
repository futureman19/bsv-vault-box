"""Complete immutable review; preserve interrupted evidence verbatim."""
import pathlib,json,hashlib,base64,html,zipfile,collections
R=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
old=json.loads((R/'evidence-inventory.json').read_text())
for n,m in old.items():
 b=(R/n).read_bytes();assert len(b)==m['bytes'] and sha(b)==m['sha256'],n
report=json.loads((R/'partial-ledger.json').read_text());ids=report['assigned'];visual={}
for p in sorted(R.glob('resume-visual-*.json')):
 d=json.loads(p.read_text())
 for v in d.get('findings',d.get('results',[])):
  assert v['id'] not in visual
  assert v['review_complete']
  names=[n.removeprefix('launch/art-05/') for n in v['images_inspected']]
  required={f'smoke/{v["id"]}/{mode}-{pose}.png' for mode in ['desktop','mobile'] for pose in ['closed','open']}|{f'sources/{v["id"]}/marketing.webp'}
  assert required<=set(names),(v['id'],names)
  assert all((R/n).is_file() for n in required)
  visual[v['id']]={'report':p.name,'finding':v}
assert set(visual)==set(ids) and len(ids)==len(set(ids))==25
runtime={r['id']:r for r in json.loads((R/'resume-runtime.json').read_text())}
for e in report['entries']:
 s=e['id'];v=visual[s]['finding'];e.update(review_complete=True,visual=visual[s],status=v['status'],decision_reason=v.get('reason',v.get('disposition_reason','See visual finding')),user_final_approved=False,art_changed=False)
 e['visual_status']=v.get('visual_status',v['status'])
 e['package_holds']=['Full historical source inventory not verified'] if s in ['iceland','new-zealand'] else []
 if s=='iceland':e['package_holds'].append('Selected archive/Git exact-byte mismatch retained; newline-only is not exact identity')
 if e['package_holds']:e['status']='needs-decision'
 if s in runtime:
  e['runtime_followup']={'result':runtime[s]['open_reset'],'report':'resume-runtime.json','captures':[f'resume-runtime/{s}/open.png',f'resume-runtime/{s}/rotated-open.png'],'assessment':'Fresh rotated view does not demonstrate broken geometry. Projecting free-edge tab is consistent with released front clasp, not rear hinge. Hidden contact and physical clearances remain unproven.'}
  if s=='chile':e['runtime_followup']['assessment']='Fresh rotated view shows repeated stepped rim/corner joints, not an unequivocal hole or torn mesh. Original finish/joint decision hold retained; no automatic redesign.'
 e['decision_reason']=('Package holds: '+'; '.join(e['package_holds'])+'. ' if e['package_holds'] else '')+e['decision_reason']
 # Rebind unchanged viewer to exact immutable hash rather than assume saved success.
 b=pathlib.Path(e['source_record']['delivered_viewer']['path']).read_bytes();assert sha(b)==e['packaging']['viewer']['sha256'] and len(b)<5000000
for file,count,key in [('smoke-results.json',50,'result'),('motion-results.json',25,'passed'),('extended-results.json',25,None)]:
 rows=json.loads((R/file).read_text());assert len(rows)==count
 if key:assert all(r[key] in [True,'pass'] for r in rows)
 else:assert all(r['no_js_poster'] and r['geometry']['nonfinite']==0 for r in rows)
report.update(complete=True,blocker=None,uncompleted_ids=[],review_status='Bounded author review complete; independent QA and user decisions remain',historical_evidence_verified=len(old),technical_evidence='Prior attempt outputs retained and hash-verified, not rerun unchanged suites',fresh_checks={'original_images_inspected':125,'immutable_viewer_hashes':25,'runtime_open_reset_rotated_views':3},counts=dict(collections.Counter(e['status'] for e in report['entries'])))
(R/'review-ledger.json').write_text(json.dumps(report,indent=2)+'\n')
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>ART-05 candidate review</title><style>body{background:#15161b;color:#eee;font:16px system-ui;margin:24px}img{width:100%;height:auto}section{margin:40px 0}p{max-width:1000px}h2{color:#e5c887}</style><h1>ART-05 — 25 candidate reviews</h1><p>All desktop/mobile closed/open originals and matching promotional art inspected. No art changed or finally approved. Pass means bounded candidate suitability, not release clearance. Iceland and New Zealand package holds remain. Original technical evidence is preserved, not represented as a fresh rerun. This is a poster comparison report, not an interactive model.</p><p>'+html.escape(str(report['counts']))+'</p>']
for e in report['entries']:
 v=e['visual']['finding'];text=e['decision_reason']+' '+ ' '.join(v.get('finish_and_fidelity_differences',[]))
 parts.append('<section><h2>'+html.escape(e['id']+' — '+e['status'])+'</h2><p>'+html.escape(text)+'</p><p>Offline viewer: '+str(e['packaging']['viewer']['bytes'])+' bytes. Final user approval: no.</p><img alt="'+html.escape(e['id'])+' promotional versus desktop/mobile actual model closed and open" src="data:image/jpeg;base64,'+base64.b64encode((R/'boards'/(e['id']+'.jpg')).read_bytes()).decode()+'"></section>')
(R/'review.html').write_text(''.join(parts)+'</html>')
files=[p for p in R.rglob('*') if p.is_file() and p.suffix!='.zip' and p.name not in ['resume-inventory.json','resume-package-report.json'] and '__pycache__' not in p.parts]
inv={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(files)}
(R/'resume-inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
groups={'review-evidence.zip':[],'review-desktop-captures.zip':[],'review-mobile-captures.zip':[]}
for p in files:
 n=p.relative_to(R).as_posix(); group='review-evidence.zip'
 if n.startswith('smoke/') and p.suffix=='.png':group='review-mobile-captures.zip' if p.name.startswith('mobile') else 'review-desktop-captures.zip'
 groups[group].append(p)
packages=[]
for name,ps in groups.items():
 with zipfile.ZipFile(R/name,'w',zipfile.ZIP_DEFLATED) as z:
  for p in ps+[R/'resume-inventory.json']:z.write(p,p.relative_to(R).as_posix())
 with zipfile.ZipFile(R/name) as z:
  assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))
  for n in z.namelist():
   assert not n.startswith('/') and '..' not in pathlib.PurePosixPath(n).parts
   if n in inv:assert sha(z.read(n))==inv[n]['sha256'] and len(z.read(n))==inv[n]['bytes']
 b=(R/name).read_bytes();assert len(b)<25000000;packages.append({'file':name,'bytes':len(b),'sha256':sha(b),'entries':len(ps)+1})
summary={'counts':report['counts'],'held_ids':[e['id'] for e in report['entries'] if e['status']=='needs-decision'],'reviewed':25,'unreviewed':[],'historical_hashes':len(old),'inventory_entries':len(inv),'report_html_bytes':(R/'review.html').stat().st_size,'ledger_sha256':sha((R/'review-ledger.json').read_bytes()),'packages':packages}
(R/'resume-package-report.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
