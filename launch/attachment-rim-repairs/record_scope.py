from pathlib import Path
import json,subprocess,hashlib
R=Path(__file__).resolve().parents[2];out=R/'launch/attachment-rim-repairs';d=json.loads((R/'launch/collection-repairs/dispositions.json').read_text());ids=d['remaining_mechanical_queue']
def viewers(x):
 if isinstance(x,dict):
  if str(x.get('path','')).endswith('.html') and x.get('commit'):yield x
  for v in x.values():yield from viewers(v)
 elif isinstance(x,list):
  for v in x:yield from viewers(v)
rows=[]
for ident in ids:
 r=next(r for r in d['records'] if r['id']==ident);vs=list(viewers(r));assert vs,ident;v=vs[0];folder=str(Path(v['path']).parent).replace('\\','/');sha=v['commit']
 names=subprocess.check_output(['git','ls-tree','-r','--name-only',sha,'--',folder],cwd=R,text=True).splitlines();authors=[p for p in names if Path(p).name.startswith('author') and p.endswith('.py')]
 src=[]
 for p in authors:
  b=subprocess.check_output(['git','show',sha+':'+p],cwd=R);dest=out/'source-inspection'/ident/Path(p).name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);src.append({'path':p,'sha256':hashlib.sha256(b).hexdigest(),'snapshot':str(dest.relative_to(R)).replace('\\','/')})
 rows.append({'id':ident,'source_commit':sha,'viewer':v,'source_scripts':src,'original_record':r,'status':'bounded-repair-candidate' if ident in ['ghana','chile'] else 'remaining-uncompleted','fresh_original_scale_browser':ident in ['ghana','chile'],'final_art_approved':False})
report={'parent_commit':'3952a4eb1c57ca921c21d0aa774ab8b8752e3df7','collection_complete':False,'scope_ids':ids,'repaired_ids':['ghana','chile'],'remaining_ids':[i for i in ids if i not in ['ghana','chile']],'records':rows}
(out/'continuation-ledger.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='records'},indent=2))
