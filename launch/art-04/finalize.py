import pathlib,json,collections
R=pathlib.Path(__file__).resolve().parent
IDS='andorra austria belize bulgaria chad cuba ecuador fiji greece hungary israel kuwait liechtenstein malta mongolia netherlands oman peru rwanda senegal somalia suriname timor-leste uganda vatican-city'.split()
def load(n):return json.loads((R/n).read_text())
def indexed(rows):
 assert len(rows)==25 and len({e['id'] for e in rows})==25 and {e['id'] for e in rows}==set(IDS)
 return {e['id']:e for e in rows}
P=indexed(load('packaging-results.json'));V=indexed(load('visual-findings.json'));M=indexed(load('motion-results.json'));X=indexed(load('extended-results.json'));A=indexed(load('archive-results.json'));B=load('smoke-results.json');L={e['id']:e for e in load('parent-ledger.json')['entries']}
assert len(B)==50 and all(b['result']=='pass' for b in B)
assert all(m['exit_code']==0 for m in M.values())
rows=[]
for s in IDS:
 p=P[s];v=V[s];modes=[b for b in B if b['id']==s];assert len(modes)==2 and {b['mode'] for b in modes}=={'desktop','mobile'}
 captures=[f'smoke/{s}/{mode}-{pose}.png' for mode in ['desktop','mobile'] for pose in ['closed','open']]
 for path in captures:assert (R/path).is_file()
 assert p['viewer']['bytes']<5000000 and all(b['sha256']==p['viewer']['sha256'] for b in modes)
 holds=list(L[s]['missing_gates'])
 if v['status']=='needs-decision':holds.append('user fidelity decision before substantial redesign')
 if p['packaging']=='hold':assert 'source-archive-integrity-or-required-payload-mismatch' in holds
 rows.append({**p,**v,'visual_status':v['status'],'status':'needs-decision' if p['packaging']=='hold' or v['status']=='needs-decision' else 'pass','captures':captures,'comparison':f'boards/{s}.jpg','browser':modes,'motion':M[s],'extended':X[s],'archive_check':A[s],'parent_missing_gates_preserved':L[s]['missing_gates'],'parent_source_archives':L[s]['source_archives'],'remaining_gates':holds+['independent QA-ART-04 review'],'polish_iterations':0,'art_changed':False,'independent_qa_pending':True,'user_final_approved':False,'launch_ready':False,'fresh_blender_reopen':False,'fresh_collision_sampling':False,'fresh_corrupt_glb_fallback':False,'visual_review_scope':'Delegated reviewers inspected comparison plus original four captures and exact marketing; parent reinspected Malta footprint. No final user approval.'})
summary={'task':'t_5369a83b','parent_ledger_commit':'6db6388d04fee0da8e0324a640d5880a5813a39c','reviewed':len(rows),'counts':dict(collections.Counter(r['status'] for r in rows)),'visual_counts':dict(collections.Counter(r['visual_status'] for r in rows)),'changed_designs':0,'unreviewed_ids':[],'needs_decision':[r['id'] for r in rows if r['status']=='needs-decision'],'visual_holds':[r['id'] for r in rows if r['visual_status']=='needs-decision'],'packaging_holds':[r['id'] for r in rows if r['packaging']=='hold'],'html_byte_range':[min(r['viewer']['bytes'] for r in rows),max(r['viewer']['bytes'] for r in rows)],'browser_cases':len(B),'motion_modules':len(M),'nojs_and_geometry_cases':len(X),'archive_inventory_entries':sum(a['inventory_entries_checked'] for a in A.values()),'launch_ready':False,'entries':rows}
(R/'review-results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='entries'},indent=2))
