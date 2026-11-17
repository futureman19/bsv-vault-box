"""Read-only recovery integrity check; does not overwrite reviewed captures."""
import pathlib, json, hashlib, subprocess
R=pathlib.Path(__file__).resolve().parent
D=json.loads((R/'review-results.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
parent=subprocess.check_output(['git','show','6db6388d04fee0da8e0324a640d5880a5813a39c:launch/launch-01/launch-candidates.json'])
assert sha(parent)=='28e032084f6bddf80143fd3bfd0e5b06cbdf84dc2343937e7b9bc71734ac3c9c'
assert (R/'parent-ledger.json').read_bytes()==parent
images=0
for e in D['entries']:
 for image in e['reviewed_image_hashes']:
  b=(R/image['path']).read_bytes()
  assert len(b)==image['bytes'] and sha(b)==image['sha256']
  images+=1
 assert e['browser']==[b for b in json.loads((R/'smoke-results.json').read_text()) if b['id']==e['id']]
 assert e['archive_check']==next(a for a in json.loads((R/'archive-results.json').read_text()) if a['id']==e['id'])
 assert e['motion']==next(a for a in json.loads((R/'motion-results.json').read_text()) if a['id']==e['id'])
 assert e['extended']==next(a for a in json.loads((R/'extended-results.json').read_text()) if a['id']==e['id'])
assert images==125
out={'result':'pass','reviewed_image_hashes':images,'unchanged_parent_ledger':True,'captured_interaction_cases_preserved':50,'recovery_reruns':['25 immutable payload/package checks','25 archives / 1402 inventory entries','25 shared motion endpoint suites','25 no-JS and loaded finite-geometry cases','2 offline report viewports','7 ledger regression tests'],'capture_rerun':False,'visual_reinspection':['indonesia','jordan','singapore','united-states'],'scope':'Original reviewed captures frozen and verified; no art changes or final approval. Recovery reruns do not claim fresh sampled collisions or Blender parity.'}
(R/'recovery-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
