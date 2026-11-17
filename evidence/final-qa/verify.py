from pathlib import Path
import json,hashlib,subprocess,collections
R=Path(__file__).resolve().parents[2]; O=R/'evidence/final-qa'
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def sha(b):return hashlib.sha256(b).hexdigest()
base='f8efc957a2cef7767f45b6e65d5f0f8f0d71be37'
pins={'ops':base,'rehearsal':'01225c6aa893122525116dcfa793ac1f3d6885ae','collection':'f0a54d9b3e80338fbe34c869987a45d6d23ae25c','security':'10acb9dfa127862b20172f4ce12f1dee32901b88','allocation':'edcdd5954439ba3b183b157bd52777a17b722b41','web':'e5003341b4d503ac1d04f0a852e0570939e68bac','production':'606147d6a1521adf635d79a70785ba7f82dbbf77'}
for k,p in pins.items():
 if k!='production':subprocess.run(['git','merge-base','--is-ancestor',p,base],cwd=R,check=True)
unchanged={}
for p in ['vault/src','vault/artifacts','mint','launch/mint','launch/collection','docs']:
 assert not git('diff',base,'--',p)
 unchanged[p]=git('rev-parse',base+':'+p).decode().strip()
l=json.loads((R/'launch/collection/ledger.json').read_bytes()); e=l['entries']
print('entry keys',e[0].keys());print('counts',l['counts']);print('coverage',l['coverage'])
assert len(e)==201 and len({x['id'] for x in e})==201
assert dict(collections.Counter(x['verdict'] for x in e))==l['counts']
assert collections.Counter(x['category'] for x in e)=={'Country':195,'Ocean':5,'Moon':1}
assert sum(x['approval']['user_final_approved'] for x in e)==0
boards=[]
for b in l['comparison_boards']:
 raw=git('show',b['commit']+':'+b['path']);assert len(raw)==b['bytes'] and sha(raw)==b['sha256'];boards.append(b['id'])
result={'pins':pins,'unchangedTrees':unchanged,'ledgerSha256':sha((R/'launch/collection/ledger.json').read_bytes()),'counts':l['counts'],'categories':dict(collections.Counter(x['category'] for x in e)),'finalApprovals':0,'comparisonBoardHashesVerified':len(boards),'claimAuditSourceHashes':{p:sha((R/p).read_bytes()) for p in ['README.md','docs/index.html','docs/check.html','docs/vaultcheck.js']},'freshNodeRun':False,'launchReady':False}
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
