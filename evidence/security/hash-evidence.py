import hashlib,json,pathlib,subprocess
root=pathlib.Path(__file__).resolve().parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=root)
results={}
for name in ['evidence/contracts/hashes.json','evidence/contracts/recovery-run/hashes.json']:
 data=json.loads(git('show','6dbcd54:'+name))
 bad=[p for p,h in data.items() if sha(git('show','6dbcd54:'+p))!=h]
 results[name]={'entries':len(data),'mismatches':bad}
 assert not bad,results
(root/'evidence/security/parent-hashes.json').write_text(json.dumps(results,indent=2)+'\n')
paths=list((root/'evidence/security').glob('*'))
paths += [root/p for p in ['mint/transfer.js','mint/recovery.js','vault/src/launch-record.js','vault/src/contracts/ordinalPair.ts','vault/artifacts/ordinalPair.json','vault/package-lock.json','evidence/contracts/proof.json']]
hashes={p.relative_to(root).as_posix():sha(p.read_bytes()) for p in paths if p.is_file() and p.name!='hashes.json'}
(root/'evidence/security/hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
print(json.dumps(results));print('packet entries',len(hashes))
