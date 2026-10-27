"""Optional read-only differential gate; never invokes v3_ref.main()."""
import importlib.util
import json
import pathlib
import subprocess

root = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('baseline', root / 'v3_ref.py')
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
cases = []
for i in range(50):
    m = ref.canonical_manifest() if i < 25 else {
        'name': 'é😀\x7f', 'pack_size': 3, 'allow_pack_duplicates': False,
        'designs': [{'id': j, 'ref': str(j), 'weight': 10 if j == 0 else 1} for j in range(3)],
        'total_weight': 12, 'manifest_version': 1,
    }
    pack, retries = ref.draw_pack(m, f'box{i}', f'seed{i}')
    cases.append({'manifest': m, 'box': f'box{i}', 'seed': f'seed{i}', 'designs': pack,
                  'retries': retries, 'canonical': json.dumps(m, sort_keys=True, separators=(',', ':')),
                  'root': ref.manifest_root(m)})
script = """
const fs=require('node:fs'), assert=require('node:assert/strict');
const {drawPack}=require('./draw'),{buildManifest,canonicalSerialize,manifestRoot}=require('./manifest');
for(const c of JSON.parse(fs.readFileSync(0,'utf8'))) {
 // Historical bytes/root remain compared unchanged; enrich only the drawing input.
 const published=buildManifest({...c.manifest,per_slot_odds_published:true});
 const result=drawPack(published,c.box,c.seed);
 assert.deepEqual(result.designs,c.designs); assert.equal(result.retries,c.retries);
 assert.equal(canonicalSerialize(c.manifest),c.canonical); assert.equal(manifestRoot(c.manifest),c.root);
}
console.log('PASS 50 Python differential cases: canonical bytes, roots, designs and retry counts');
"""
subprocess.run(['node', '-e', script], input=json.dumps(cases), text=True, cwd=root, check=True)
