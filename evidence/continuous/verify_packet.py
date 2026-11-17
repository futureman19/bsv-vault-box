"""Verify source pins and delivered CLI/browser identity, then hash packet files."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=Path(__file__).resolve().parent

def sha(data):
    return hashlib.sha256(data).hexdigest()

sources=json.loads((BASE/'run-01/sources.json').read_text())
for name,digest in sources.items():
    assert sha((ROOT/name).read_bytes()) == digest, name
reference=json.loads((BASE/'run-01/evidence.json').read_text())
for name in ('desktop','mobile'):
    other=json.loads((BASE/f'browser-02/{name}-download.json').read_text())
    assert other['binding']==reference['binding']
    assert [x['response']['raw'] for x in other['history']]==[x['response']['raw'] for x in reference['history']]
    assert other['stage']=='WITHDRAWN' and len(other['history'])==5
    assert all(other['provenance'].values())
assert reference['events']==17
assert reference['binding']['origin']=='0580a374ee024525808f19b99f7dca91f3d86880207c3deb3ffa90bbd0206a36_0'
assert json.loads((BASE/'browser-02/report.json').read_text())['result']=='PASS'
files=[]
for folder in (BASE,ROOT/'launch/continuous'):
    for p in folder.rglob('*'):
        if p.is_file() and not any(part.startswith('.') and part not in ('.gitattributes','.gitignore') for part in p.relative_to(folder).parts) and '__pycache__' not in p.parts and p.name not in ('sha256.json','continuous-custody-evidence.zip'):
            files.append(p)
manifest={str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes()) for p in sorted(files)}
if (BASE/'sha256.json').exists():
    assert json.loads((BASE/'sha256.json').read_text())==manifest,'packet changed'
else:
    (BASE/'sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
# If staged, check the exact byte-preserving Git blobs (not only worktree files).
if '--staged' in __import__('sys').argv:
    for name,digest in manifest.items():
        content=subprocess.check_output(['git','show',':'+name],cwd=ROOT)
        assert sha(content)==digest,name+' staged byte mismatch'
print(json.dumps({'source_hashes':len(sources),'packet_files':len(manifest),'cli_browser_same_binding_and_raw_transactions':True,'staged':'--staged' in __import__('sys').argv},indent=2))
