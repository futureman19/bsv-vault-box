"""Capture exact read-only upstream excerpts and bounded local verification."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)==2 else None
if OUT is None: raise SystemExit('usage: python capture.py FRESH_OUTPUT_DIRECTORY')
OUT.mkdir(parents=True,exist_ok=False)

def run(name,argv):
    r=subprocess.run(argv,cwd=ROOT,capture_output=True)
    (OUT/name).write_bytes(r.stdout+r.stderr)
    print(name,r.returncode)
    if r.returncode: raise SystemExit(r.returncode)
    return {'file':name,'argv':argv,'exit':r.returncode}

if __name__=='__main__':
    rows=[]
    rows.append(run('focused.txt',['node','--test','launch/wallet-transport/test.js','launch/wallet-transport/security.test.js']))
    rows.append(run('harness.json',['node','launch/wallet-transport/harness.js']))
    rows.append(run('build.txt',['node','launch/wallet-transport/node_modules/browserify/bin/cmd.js','launch/wallet-transport/adapter.js','--standalone','BoxSVWalletTransport','-o','launch/wallet-transport/browser/adapter.js']))
    rows.append(run('browser.txt',['python','launch/wallet-transport/browser_smoke.py']))
    rows.append(run('continuous-regression.txt',['node','--test','launch/continuous/test.js','launch/continuous/security.test.js','launch/continuous/server.test.js','launch/continuous/process.test.js']))
    (OUT/'commands.json').write_text(json.dumps(rows,indent=2)+'\n')
    manifest={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for base in [OUT,ROOT/'launch/wallet-transport'] for p in base.rglob('*') if p.is_file() and 'node_modules' not in p.parts and p.name!='sha256.json' and '__pycache__' not in p.parts}
    (OUT/'sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
