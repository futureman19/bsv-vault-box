import pathlib,json,hashlib,collections,zipfile,subprocess
R=pathlib.Path(__file__).resolve().parent
read=lambda n:json.loads((R/n).read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
p=read('parent/review-results.json'); v=read('independent-visual.json'); b=read('byte-verification.json'); smoke=read('smoke-results.json'); motion=read('motion-results.json')
ids=[e['id'] for e in p['entries']]
assert len(ids)==25 and len(set(ids))==25
assert {e['id'] for e in v['entries']}==set(ids)=={e['id'] for e in b['rows']}
assert len(smoke)==50 and {(e['id'],e['mode']) for e in smoke}=={(i,m) for i in ids for m in ['desktop','mobile']}
assert all(e['result']=='pass' and e['asset']['nonfinite']==0 and e['asset']['degenerate']==0 for e in smoke)
assert len(motion)==25 and {e['id'] for e in motion}==set(ids) and all(e['exit_code']==0 for e in motion)
byvisual={e['id']:e for e in v['entries']}
assert all(byvisual[i]['disposition']=='needs-user-review' for i in p['needs_decision'])
rows=[]
for e in p['entries']:
    i=e['id']; view=byvisual[i]
    rows.append({'id':i,'selection':e['selection'],'viewer':e['viewer'],'models':e['models'],'archives':next(x['archives'] for x in b['rows'] if x['id']==i),'marketing':e['marketing'],'approval':e['approval'],'technical_verdict':'pass-bounded-review','visual_verdict':view['disposition'],'independent_reviewer_recommendation':view['reviewer_recommendation'],'visual_findings':view['finding'],'parent_hold_preserved':i in p['needs_decision'],'inspected_parent_images':['parent/'+e['comparison']]+['parent/'+c for c in e['captures']],'fresh_runtime_captures':['smoke/'+i+'/'+m+'-'+s+'.png' for m in ['desktop','mobile'] for s in ['closed','open']],'fresh_browser_cases':[x for x in smoke if x['id']==i],'fresh_motion_suite':next(x for x in motion if x['id']==i),'missing_gates':['explicit-final-user-art-approval','fresh-full-Blender-reopen-parity-and-sampled-collisions','fresh-corrupt-GLB-fallback','storage-and-preservation-policy','mint-and-release-authorization'],'launch_ready':False})
report={'task':'t_5c96269b','parent_task':'t_d76eb48d','parent_ref':'feature/art-02-review','parent_commit':b['parent_commit'],'parent_ledger_sha256':sha((R/'parent/review-results.json').read_bytes()),'reviewed':len(rows),'unreviewed_ids':[],'changed_art':0,'technical_passes':25,'visual_counts':dict(collections.Counter(e['visual_verdict'] for e in rows)),'needs_user_review':[e['id'] for e in rows if e['visual_verdict']=='needs-user-review'],'final_user_approvals_granted':0,'launch_ready':False,'fresh_checks':{'archive_inventory_entries':b['archive_inventory_entries_verified'],'parent_evidence_hashes':b['parent_evidence_files_verified'],'offline_browser_cases':len(smoke),'shared_motion_module_suites':len(motion)},'historical_only':['Blender parity and packed-source reopen','sampled mechanism collisions','no-JS fallback checked by parent, not rerun here'],'visual_adjudication':v['adjudication'],'critical_reproducible_failures':[],'entries':rows}
(R/'reviewed-ledger.json').write_text(json.dumps(report,indent=2)+'\n')
# Parent evidence ZIP is external input, never modified.
zp=pathlib.Path('C:/Users/futur/Desktop/bsv-vault-box/.worktrees/t_d76eb48d/launch/art-02/art-02-review.zip')
zb=zp.read_bytes();assert len(zb)==2394983 and sha(zb)=='59cf79244cbde6d8ae4da5dd817f5fc74ada4795d2c22dfbf73a48691e219576'
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    for n in z.namelist():
        assert not n.startswith(('/','\\')) and '..' not in pathlib.PurePosixPath(n).parts
        assert z.read(n)==(R/'parent'/n).read_bytes()
(R/'parent-zip-verification.json').write_text(json.dumps({'path':str(zp),'bytes':len(zb),'sha256':sha(zb),'entries':len(z.namelist()),'exact_members_match_committed_parent':True},indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['reviewed','visual_counts','fresh_checks','needs_user_review']},indent=2))
