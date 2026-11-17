"""Read-only integration pins and nonsecret package integrity checks."""
from pathlib import Path
import subprocess,json,hashlib,re
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'evidence/rehearsal'
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT)
pins={'mint':'edcdd5954439ba3b183b157bd52777a17b722b41','security':'10acb9dfa127862b20172f4ce12f1dee32901b88','collection':'f0a54d9b3e80338fbe34c869987a45d6d23ae25c','web':'e5003341b4d503ac1d04f0a852e0570939e68bac'}
for sha in pins.values():subprocess.run(['git','merge-base','--is-ancestor',sha,'HEAD'],cwd=ROOT,check=True)
for name,paths in [('security',['mint','vault/src','vault/artifacts']),('mint',['launch/mint','launch/assets']),('collection',['launch/collection']),('web',['docs'])]:
 assert not git('diff','--name-only',pins[name],'--',*paths).strip(),name
ledger=ROOT/'launch/collection/ledger.json'
assert hashlib.sha256(ledger.read_bytes()).hexdigest()=='ea68d8c34af0e4158fd4f6b9c5ef77727f34ca5c34d66c317303ecf7b21ee796'
p=json.loads((ROOT/'evidence/contracts/proof.json').read_text())
artifact=ROOT/'vault/artifacts/ordinalPair.json'
assert hashlib.sha256(artifact.read_bytes()).hexdigest()==p['artifact']['fileSha256']
assert hashlib.sha256((ROOT/'vault/src/contracts/ordinalPair.ts').read_bytes()).hexdigest()==p['artifact']['sourceSha256']
# No serialized private keys, cookies or credentials may enter the packet.
pattern=re.compile(rb'(?:^|[^A-Za-z0-9])(?:[KLc][1-9A-HJ-NP-Za-km-z]{51}|5[1-9A-HJ-NP-Za-km-z]{50}|[xt]prv[1-9A-HJ-NP-Za-km-z]{100,})(?![A-Za-z0-9])|^-----BEGIN .*PRIVATE KEY-----|^rpcpassword\s*=',re.M)
for file in OUT.rglob('*'):
 if not file.is_file():continue
 assert file.suffix not in ['.wif','.key'] and file.name not in ['.cookie','wallet.dat'],file
 if file.suffix not in ['.png','.sqlite']:assert not pattern.search(file.read_bytes()),file
value={'status':'PASS','integratedHead':git('rev-parse','HEAD').decode().strip(),'pins':pins,'unchangedReviewedTrees':True,'ledgerSha256':hashlib.sha256(ledger.read_bytes()).hexdigest(),'artifact':p['artifact'],'secretScan':'No serialized keys/credentials detected; public deterministic fixtures only','compilerRebuilt':False}
print(json.dumps(value,indent=2))
