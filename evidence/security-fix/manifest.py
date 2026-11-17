"""Create from the index, or verify against an exact commit; no checkout-byte assumptions."""
import hashlib, json, pathlib, subprocess, sys
root = pathlib.Path(__file__).resolve().parents[2]
manifest = root / 'evidence/security-fix/sha256.json'
source = ['mint/recovery.js','mint/transfer.js','vault/src/launch-record.js',
          'mint/test/recovery.test.js','mint/test/finality.test.js','mint/test/security-fix.test.js',
          'vault/artifacts/ordinalPair.json']
def blob(ref, p):
    return subprocess.check_output(['git','show',ref+':'+p],cwd=root)
if sys.argv[1] == 'create':
    files = sorted(set(source + [p.relative_to(root).as_posix() for p in manifest.parent.iterdir()
                                if p.is_file() and p.name != 'sha256.json']))
    # Discover artifact spelling from tracked paths instead of assuming it.
    tracked = subprocess.check_output(['git','ls-files','vault/artifacts'],cwd=root,text=True).splitlines()
    files = [p for p in files if p != 'vault/artifacts/ordinalPair.json'] + tracked
    rows = [{'path':p,'sha256':hashlib.sha256(blob('',p)).hexdigest()} for p in files]
    manifest.write_text(json.dumps({'basis':'staged Git blobs; raw evidence -text','files':rows},indent=2)+'\n')
    print('created',len(rows),'entries')
else:
    ref = sys.argv[1]
    data = json.loads(blob(ref,'evidence/security-fix/sha256.json'))
    for row in data['files']:
        assert hashlib.sha256(blob(ref,row['path'])).hexdigest() == row['sha256'], row['path']
    print('verified',len(data['files']),'committed blobs at',ref)
