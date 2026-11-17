import base64, collections, hashlib, html, io, json, pathlib
from PIL import Image
R=pathlib.Path(__file__).resolve().parent; P=R/'launch/art-01'
parent=json.loads((P/'review-results.json').read_text()); verification=json.loads((R/'verification-results.json').read_text())
visual={}
for f in sorted(R.glob('visual-*.json')):
 for e in json.loads(f.read_text())['entries']:
  assert e['id'] not in visual
  visual[e['id']]={'file':f.name,**e}
assert sorted(visual)==sorted(parent['assigned'])
smoke=json.loads((R/'smoke-results.json').read_text()); assert len(smoke)==6 and all(e['result']=='pass' for e in smoke)
entries=[]
for e in parent['entries']:
 s=e['id']; v=visual[s]; assert not v['critical_visible_faults']
 status='needs-user-review' if e['status']=='needs-decision' else 'bounded-candidate-pass'
 entries.append({'id':s,'verdict':status,'parent_status':e['status'],'user_final_approved':False,'launch_ready':False,'model_changed':False,'selection':e['selection'],'viewer':e['viewer'],'model_sources':next(x['sources'] for x in verification['entries'] if x['id']==s),'source_archives':next(x['archives'] for x in verification['entries'] if x['id']==s),'visual_review':v,'all_four_original_captures_inspected':True,'marketing_inspected':True,'captures':['launch/art-01/'+x for x in e['captures']],'fresh_qa_runtime':[x for x in smoke if x['id']==s],'parent_runtime':{'cases':e['browser'],'motion':e['motion'],'independently_rerun':False},'remaining_gates':[g for g in e['inherited_missing_gates'] if g!='independent-current-model-visual-review']+(['art-direction-decision'] if status=='needs-user-review' else [])+['hinge-attachment-clarity-not-proven-by-stills'],'critical_defects':[]})
counts=dict(collections.Counter(e['verdict'] for e in entries))
result={'schema':'boxsv-independent-art-review/1','task':'t_8267b59b','parent_task':'t_e669e48c','parent_commit':verification['parent_commit'],'parent_inventory_files_verified':verification['parent_inventory_files_verified'],'reviewed':len(entries),'assigned':parent['assigned'],'unreviewed':[],'counts':counts,'changed_designs':[],'critical_reproducible_defects':[],'approval_policy':'Review completion only; no user art approval or launch authorization. Preserve all 17 artistic decisions and Namibia full-archive-inventory hold.','limitations':['104 inherited exact-hashed original screenshots and 26 marketing images inspected by four independent read-only visual agents; lead spot-checked Lesotho, Panama and Malaysia.','Fresh QA runtime is six cases across Lesotho/Panama/Malaysia only; other 46 parent cases and all 26 motion runs remain inherited evidence, not claimed fresh.','No Blender reopen/parity, sampled collisions, complete ZIP internal inventory, corrupt-GLB/no-JS fallback rerun.','Emulated mobile is not physical-phone performance.','Apparent hinge gaps need mechanical contact evidence before realistic-attachment claims; no definite detached part proven.'],'entries':entries}
(R/'reviewed-ledger.json').write_text(json.dumps(result,indent=2)+'\n')
parts=['<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BoxSV batch 1 independent QA</title><style>body{background:#141922;color:#eee;font:16px system-ui;max-width:1100px;margin:auto;padding:20px}img{width:100%;height:auto}article{border-top:1px solid #667;margin-top:32px}p{line-height:1.6}code{overflow-wrap:anywhere}</style><h1>Batch 1 · independent QA</h1><p>26 reviewed; 9 bounded candidate passes; 17 need user art decisions. None approved for launch. Poster comparison report only—not interactive models. No art changed.</p><p>All original desktop/mobile closed/open screenshots inspected; six independent offline interaction cases passed. Exact source/archive payload bytes verified for every ID. Namibia full internal archive inventory remains unresolved. Hinge contact is not proven by stills.</p>']
for e in entries:
 im=Image.open(P/'boards'/f"{e['id']}.jpg"); im.thumbnail((1000,1000)); out=io.BytesIO(); im.save(out,format='JPEG',quality=75)
 v=e['visual_review']; notes=v.get('marketing_comparison') or v.get('observations',{}).get('marketing','')
 parts.append(f'<article><h2>{html.escape(e["id"])} · {e["verdict"]}</h2><img alt="{e["id"]}: marketing, desktop and mobile states" src="data:image/jpeg;base64,{base64.b64encode(out.getvalue()).decode()}"><p>{html.escape(notes)}</p><p>{html.escape(v.get("qualification", ""))}</p><p>Viewer: {e["viewer"]["bytes"]:,} bytes. Candidate only.</p></article>')
(R/'review.html').write_text(''.join(parts),encoding='utf-8')
print(counts, 'HTML bytes', (R/'review.html').stat().st_size)
