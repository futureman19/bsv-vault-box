'use strict'
// Offline deterministic export/replay. Policy is code-owned, NEVER read from bundle.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict')
const M=require('../src/four-ordinal')
const target=path.join(__dirname,'../fixtures/four-ordinal-vectors.json')
const generated=M.vectors()
if(process.argv.includes('--write')) fs.writeFileSync(target,JSON.stringify(generated,null,2)+'\n')
const saved=JSON.parse(fs.readFileSync(target,'utf8'))
assert.deepEqual(saved,generated,'deterministic fixture differs; inspect before regeneration')
const result=M.replayVectors(saved,M.TRUSTED_POLICY)
assert.equal(result.valid,true,JSON.stringify(result))
console.log(JSON.stringify({result,transactions:saved.lifecycle.map(({action,txid,bytes})=>({action,txid,bytes})),artifactSha256:saved.artifactSha256},null,2))
