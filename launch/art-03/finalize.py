import json,pathlib,hashlib,collections
R=pathlib.Path(__file__).resolve().parent
notes=json.loads((R/'visual-notes.json').read_text())
ids=json.loads((R/'assigned.json').read_text()); p=json.loads((R/'packaging-results.json').read_text()); smoke=json.loads((R/'smoke-results.json').read_text()); motion=json.loads((R/'motion-results.json').read_text())
assert set(notes)==set(ids) and len(ids)==len(set(ids))==25 and len(p)==25 and len(smoke)==50 and len(motion)==25
assert all(x['result']=='pass' for x in smoke) and all(x['passed'] for x in motion)
rows=[]
for e in p:
 s=e['id']; status,note=notes[s]; captures=[f'smoke/{s}/{m}-{pose}.png' for m in ['desktop','mobile'] for pose in ['closed','open']];assert all((R/c).exists() for c in captures)
 assert {(x['mode']) for x in smoke if x['id']==s}=={'desktop','mobile'}
 rows.append(dict(id=s,status=status,user_final_approved=False,launch_ready=False,polish_iterations=0,model_changed=False,selection=e['selection'],viewer=e['viewer'],glb_bytes=e['glb_bytes'],source_archives=e['archives'],captures=captures,comparison=f'boards/{s}.jpg',visual_findings=note,hardware='Principal fittings retained except noted promotional disparity. Open hinges visible; apparent spacing remains unproven contact, not demonstrated detached geometry.',decision='Resolve visual fidelity or hinge-clarity hold; no automatic substantial redesign.' if status=='needs-decision' else 'No demonstrated defect warrants regeneration; stylization and final approval holds remain.',technical_scope='Fresh committed/source byte checks, ZIP CRC/safe paths/required basenames, motion units and offline desktop/mobile controls. No fresh Blender parity, collision sampling, corrupt/no-JS fallback or full ZIP inventory rerun. Required basenames are not full internal archive hash verification.',browser=[x for x in smoke if x['id']==s],motion=[x for x in motion if x['id']==s][0],inherited_missing_gates=e['missing_gates']))
result={'schema':'boxsv-art-review/1','task':'t_83adc6b5','parent_commit':'6db6388d04fee0da8e0324a640d5880a5813a39c','parent_ledger_sha256':hashlib.sha256((R/'launch-candidates.json').read_bytes()).hexdigest(),'assigned':ids,'reviewed':len(rows),'unreviewed':[],'counts':dict(collections.Counter(x['status'] for x in rows)),'changed_designs':[],'inspection':'Four read-only visual inspectors covered each board/four states; original captures inspected for ambiguities. Lead checked Ghana and Brunei. Separate pre-created QA reviewer owns independent acceptance.','entries':rows}
(R/'review-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'counts':result['counts'],'html_min':min(x['viewer']['bytes'] for x in rows),'html_max':max(x['viewer']['bytes'] for x in rows),'reviewed':len(rows)},indent=2))
