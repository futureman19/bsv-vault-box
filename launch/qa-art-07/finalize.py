import pathlib,json,hashlib,base64,html,collections,zipfile
R=pathlib.Path(__file__).resolve().parent
P=R/'parent'
def dump(n,x):(R/n).write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
parent=json.loads((P/'review-ledger.json').read_text());audit=json.loads((R/'audit-results.json').read_text());visual={}
for p in sorted(R.glob('visual-*.json')):
 d=json.loads(p.read_text());v=d.get('reviews',d.get('results',d.get('assets')))
 if isinstance(v,dict):v=[dict(x,id=k) for k,x in v.items()]
 for x in v:
  assert x['id'] not in visual;visual[x['id']]={'report':p.name,'assessment':x}
assert set(visual)=={e['id'] for e in parent['entries']}
rows=[]
for e in parent['entries']:
 hold=e['verdict']=='needs-decision'
 s=next(x for x in audit['source_checks'] if x['id']==e['id'])
 missing=[x for x in e['inherited_missing_gates'] if x!='independent-current-model-visual-review']
 row={'id':e['id'],'verdict':'needs-user-review' if hold else 'candidate-with-limitations','art_changed':False,'final_approval':False,'launch_ready':False,'parent_verdict':e['verdict'],'parent_visual_hold_preserved':hold,'selection':e['selection'],'viewer':e['viewer'],'source_models':s['models'],'source_archives':s['archives'],'marketing':e['marketing'],'captures':e['captures'],'capture_base':'parent/','independent_visual':visual[e['id']],'parent_visual':e['visual'],'approval':e['inherited_approval'],'missing_gates':missing,'inherited_missing_gates':e['inherited_missing_gates'],'fresh_checks':{'source_archive_crc_safe_paths_required_payloads':True,'source_and_delivered_viewer_hashes':True,'original_captures_and_marketing_inspected':True,'runtime':False,'motion':False,'blender_parity_collision':False,'fallback':False,'full_inner_archive_inventories':False},'historical_runtime':{'parent_commit':audit['parent_commit'],'browser':e['browser'],'motion':e['motion'],'extended':e['extended']},'critical_reproducible_failures':[]}
 if e['id']=='indian-ocean':row['lead_adjudication']='Full original desktop-open reinspection: lid-rim gap visible; small gold bearings partly hidden. Connection unresolved, not definitively detached. Preserve visual hinge-readability and palette/lagoon hold; no mechanism failure asserted.'
 rows.append(row)
counts=dict(collections.Counter(x['verdict'] for x in rows))
ledger={'task':'t_5f97a270','parent_task':'t_95c2129e','parent_commit':audit['parent_commit'],'scope':'Independent unchanged-candidate QA; original images and exact package bytes checked. No art approval or changes.','counts':counts,'unreviewed_ids':[],'final_approvals':0,'launch_ready':False,'entries':rows,'limitations':['Runtime, motion, no-JS, Blender parity/collision and corrupt-GLB gates not rerun by QA; parent runtime evidence retained as historical.','Full inner source archive inventories not rerun; required selected HTML/GLB/blend payload hashes freshly checked.','Static hinge contact remains unresolved; mobile captures are emulation, not physical-phone tests.','All final user approval, storage and release gates remain.']}
dump('reviewed-ledger.json',ledger)
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>QA ART-07 independent review</title><style>body{margin:0;background:#15191b;color:#eee;font:16px system-ui}main{max-width:1050px;margin:auto;padding:20px}article{margin:24px 0;border-top:1px solid #777;padding-top:12px}img{width:100%;height:auto}p{line-height:1.5}code{overflow-wrap:anywhere}</style><main><h1>Batch 7 · Independent candidate review</h1><p>25 reviewed · 18 candidates with limitations · 7 user-decision holds · 0 final approvals. No artwork changed.</p><p>Boards compare promotional illustration to actual desktop/mobile model captures. Not new collectible viewers or art approval. Exact source/archive payloads checked; runtime and full source geometry evidence is historical.</p>']
for e in rows:
 parts.append('<article><h2>'+html.escape(e['id'])+' — '+e['verdict']+'</h2><img alt="Promotional and actual desktop/mobile comparison: '+e['id']+'" src="data:image/jpeg;base64,'+base64.b64encode((P/'boards'/ (e['id']+'.jpg')).read_bytes()).decode()+'"><p>'+html.escape(e['parent_visual'].get('decision_needed') or e['parent_visual'].get('promotional_finish_vs_geometry','Disclosed stylization; no final approval.'))+'</p><p>Viewer '+str(e['viewer']['bytes'])+' bytes · <code>'+e['viewer']['sha256']+'</code></p></article>')
parts.append('<p>Next: consolidate candidates while preserving every visual, final-approval, storage and release hold.</p></main></html>')
(R/'review.html').write_text(''.join(parts),encoding='utf-8')
(R/'.gitattributes').write_text('* -text\n')
(R/'README.md').write_text('# Independent QA ART-07\n\n'+json.dumps(counts)+'\n\nAll 25 IDs accounted for, 125 original images independently inspected; no art edits or approvals. Parent capture bytes remain immutable. Exact selected HTML/GLB/editable source and required ZIP payloads verified for all 25; 302 parent inventoried files and three delivery ZIPs verified. Gabon marketing required a lossless full-resolution PNG decode for vision after WebP failures. Indian Ocean apparent hinge spacing reinspected; attachment remains unresolved, not proven detached.\n\nSeven holds remain: arctic-ocean, bolivia, cabo-verde, indian-ocean, mozambique, saint-vincent-and-the-grenadines, sierra-leone. All other entries are candidates with limitations.\n\nNo fresh art runtime/motion, Blender reopen/parity/collision, corrupt-GLB/no-JS or full inner source inventory run. These gates are historical, not fresh QA certification. No changed art needing rerun. Full capture/source evidence retained at exact parent ref in ledger; small report archive excludes original capture PNGs and source ZIPs, which are separately referenced. Local report HTML is not a collectible viewer. No production/keys/funds/mint/deploy.\n\nNext: downstream collection consolidation retains these holds and all final approval/storage/release gates.\n',encoding='utf-8')
print(counts,'report bytes',(R/'review.html').stat().st_size)
