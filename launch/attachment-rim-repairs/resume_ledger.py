from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[2];out=R/'launch/attachment-rim-repairs'
d=json.loads((out/'continuation-ledger.json').read_text());original={r['id']:r['original_record'] for r in d['records']}
d['previous_checkpoint']='54537619992f88428ab4325b460d0a2bcbb50f12';d['scope_complete']=False
for slug in ['algeria','guyana']:
 root=R/'preview'/f'{slug}-repair-v2';r=next(r for r in d['records'] if r['id']==slug)
 r.update(status='bounded-repair-candidate-not-final-art-approval',fresh_original_scale_browser=True,final_art_approved=False,correction_passes=1)
 r['candidate']={'path':f'preview/{slug}-repair-v2/{slug}-repair-v2.html','bytes':(root/f'{slug}-repair-v2.html').stat().st_size,'sha256':hashlib.sha256((root/f'{slug}-repair-v2.html').read_bytes()).hexdigest(),'independent_review':'deleg_91796db3','repair':json.loads((root/'repair-check.json').read_text()),'point_set_parity':json.loads((root/'parity-check.json').read_text()),'clearance':json.loads((root/'source-check.json').read_text())}
 if slug not in d['repaired_ids']:d['repaired_ids'].append(slug)
d['remaining_ids']=[s for s in d['scope_ids'] if s not in d['repaired_ids']]
assert len(d['scope_ids'])==14 and len(d['repaired_ids'])==4 and len(d['remaining_ids'])==10
assert original=={r['id']:r['original_record'] for r in d['records']}
(out/'continuation-ledger-v2.json').write_text(json.dumps(d,indent=2))
print('original review records preserved; repaired',d['repaired_ids'],'remaining',d['remaining_ids'])
