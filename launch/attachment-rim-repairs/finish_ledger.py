from pathlib import Path
import json,hashlib,copy
R=Path(__file__).resolve().parents[2];D=R/'launch/attachment-rim-repairs/finish';old=json.loads((D.parent/'continuation-ledger-v2.json').read_text());ledger=copy.deepcopy(old)
progress={r['id']:r for r in json.loads((D/'progress.json').read_text())['records']};packages={r['id']:r for r in json.loads((D/'packages/package-check.json').read_text())};checks={r['id']:r for r in json.loads((D/'acceptance/checks.json').read_text())};recovery=json.loads((D/'acceptance/recovery-check.json').read_text())
expected='afghanistan algeria chile croatia ghana guyana iceland lithuania malta mozambique panama saint-kitts-and-nevis tonga venezuela'.split();assert sorted(ledger['scope_ids'])==sorted(expected) and len(ledger['records'])==14
limitations={
'afghanistan':'Stepped rim and broad reveal remain; bright veined lapis and angular mountains remain stylized.',
'croatia':'Contrasting stepped corners, regular bowl pools and opaque/angular spillways remain; dropped zero-user images disclosed, used materials retained.',
'iceland':'Sampled basalt fractures/interior walls supported; unchanged art. Graphic moss, thin river, ice depth and mobile title wrap remain. Optional historical v9 screenshot comparison unavailable; failure preserved.',
'lithuania':'Pale model corners versus black promotional accents remain a substantive fidelity hold; angular dune and regular wood-like ripples remain.',
'malta':'Linear versus broader promotional bastion footprint remains a substantive landmark hold; smooth limestone and flat harbour remain.',
'mozambique':'Pre-existing channel texture offsets visible before/final remain a disclosed finish/mapping concern, not proven broken geometry. No claim of repaired realistic water or geology.',
'panama':'Camera raised on second/final pass; three trees discernible with overlap. Sparse foliage, planar banks, streaky jade and pre-existing texture transition remain.',
'saint-kitts-and-nevis':'Faceted islands, opaque water, brushed body and suspended-lid impression remain; rear/contact evidence does not demonstrate detached hinges.',
 'tonga':'Layered stepped trim connected, not seamless. Dark closed seam, clay-like brown and weak barkcloth/diamond relief remain.',
 'venezuela':'Soft sandstone, limited plateau contrast, cord-like cascade and flat pool remain; released front clasp is not a rear hinge defect.'}
for r in ledger['records']:
 s=r['id']
 if s not in progress:continue
 p=progress[s];root=(R/p['candidate']).parent;v=R/p['candidate'];assert v.stat().st_size<5000000
 source=json.loads((root/'source-check.json').read_text());parity=json.loads((root/'parity-check.json').read_text())
 assert source['saved_source_reopened'] and not source['collisions'] and parity['source_and_export_geometry_match']
 recovered=[a for a in recovery if a['id']==s];assert len(recovered)==2 and all(a['native_open_reset'] and a['only_endpoints'] for a in recovered)
 immutable=json.loads((D/s/'immutable-source.json').read_text())
 # Verify canonical original HTML/GLB/BLEND remain exact ledger-source bytes.
 original=D/s/'original';original_selected=[]
 for f in immutable['files']:
  if f['path'] in [f'{s}.blend',f'{s}.glb'] or f['path'].endswith('.html') and f['path']!='template.html':
   fp=original/f['path'];assert hashlib.sha256(fp.read_bytes()).hexdigest()==f['sha256'];original_selected.append(f)
 r['status']='repaired-candidate-with-retained-art-holds' if s!='iceland' else 'supported-original-retained-no-demonstrated-trim-defect'
 r['fresh_original_scale_browser']=True;r['final_art_approved']=False;r['correction_passes']=p['geometry_passes']+p['presentation_passes']
 r['final_acceptance']={'candidate':v.relative_to(R).as_posix(),'html_bytes':v.stat().st_size,'html_sha256':hashlib.sha256(v.read_bytes()).hexdigest(),'source_export':{ext:hashlib.sha256((root/f'{s}.{ext}').read_bytes()).hexdigest() for ext in ['blend','glb']},'immutable_selected':original_selected,'source_report':str((root/'source-check.json').relative_to(R)),'collision_samples':source['collision_samples'],'parity_report':str((root/'parity-check.json').relative_to(R)),'point_set_max_error':max(parity['source_to_glb_max'],parity['glb_to_source_max']),'comparison_motion_checks':checks[s],'recovered_browser':recovered,'source_package':{k:v for k,v in packages[s].items() if k not in ['inventory','recovered_viewer']},'independent_review':'launch/attachment-rim-repairs/finish/INDEPENDENT-REVIEW.md','limitations':limitations[s]}
ledger.update({'scope_complete':True,'implementation_scope_complete':True,'collection_complete':False,'final_art_approved':False,'remaining_ids':[],'repaired_ids':[s for s in expected if s!='iceland'],'unchanged_supported_ids':['iceland'],'independent_review_id':'deleg_08914d66','previous_four_checkpoint_evidence_retained_not_rerun':True,'source_artifact_head':'06df57e38f1307524fc2570b34e28c5e79ec733e','owner_packet':'launch/attachment-rim-repairs/finish/OWNER-PACKET.md','review_state':'Ready for bounded final delivery review; no collection or release approval.'})
ledger['delivery_limits']=['Exact source artifact recovery verified; clean dependency-pinned Iceland JavaScript rebuild not established (immutable build.py expects sibling node_modules; no package manifest).','Source ZIPs precede final ledger and recovered-browser evidence; preserved progress.json and RESUME.md remain historical partial checkpoints.','Mobile is touch emulation; parity is point-set, contacts are surface intersections, collision is sampled.']
for a,b in zip(old['records'],ledger['records']):assert a['original_record']==b['original_record']
(D/'final-ledger.json').write_text(json.dumps(ledger,indent=2))
print(json.dumps({'ids':len(expected),'repaired_candidates':len(ledger['repaired_ids']),'unchanged_supported':ledger['unchanged_supported_ids'],'fresh_motion_suites':len(checks),'recovered_browser_cases':len(recovery),'archived_payloads':sum(p['payloads_hash_checked'] for p in packages.values()),'html_bytes':{s:p['html_bytes'] for s,p in progress.items()},'max_point_set_error':max(r.get('final_acceptance',{}).get('point_set_max_error',0) for r in ledger['records'])},indent=2))
