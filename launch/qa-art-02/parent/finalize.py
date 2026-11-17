import pathlib,json,hashlib,collections
R=pathlib.Path(__file__).resolve().parent
P=json.loads((R/'packaging-results.json').read_text());V={v['id']:v for v in json.loads((R/'visual-findings.json').read_text())};B=json.loads((R/'smoke-results.json').read_text());M=json.loads((R/'motion-results.json').read_text());X=json.loads((R/'extended-results.json').read_text())
assert len(P)==25 and len(V)==25 and len(B)==50 and len(M)==25 and len(X)==25
assert set(V)=={p['id'] for p in P}=={m['id'] for m in M}=={x['id'] for x in X}
assert all(b['result']=='pass' for b in B) and all(m['exit_code']==0 for m in M)
rows=[]
for p in P:
 s=p['id'];modes=[b for b in B if b['id']==s];assert {b['mode'] for b in modes}=={'desktop','mobile'} and len(modes)==2
 captures=[f'smoke/{s}/{mode}-{pose}.png' for mode in ['desktop','mobile'] for pose in ['closed','open']]
 for path in captures:assert (R/path).is_file()
 rows.append({**p,**V[s],'captures':captures,'comparison':f'boards/{s}.jpg','browser':modes,'motion':next(m for m in M if m['id']==s),'extended':next(x for x in X if x['id']==s),'polish_iterations':0,'art_changed':False,'independent_qa_pending':True,'user_final_approved':False,'launch_ready':False,'remaining_gates':['independent QA-ART-02 review','explicit final user approval','storage preservation','mint/release authorization']+(['user fidelity decision before substantial redesign'] if V[s]['status']=='needs-decision' else [])})
counts=dict(collections.Counter(r['status'] for r in rows));summary={'task':'t_d76eb48d','parent_ledger_commit':'6db6388d04fee0da8e0324a640d5880a5813a39c','reviewed':len(rows),'counts':counts,'changed_designs':0,'unreviewed_ids':[],'needs_decision':[r['id'] for r in rows if r['status']=='needs-decision'],'html_byte_range':[min(r['viewer']['bytes'] for r in rows),max(r['viewer']['bytes'] for r in rows)],'browser_cases':len(B),'motion_modules':len(M),'nojs_and_geometry_cases':len(X),'launch_ready':False,'entries':rows}
(R/'review-results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='entries'},indent=2))
