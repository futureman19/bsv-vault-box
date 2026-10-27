'use strict';
const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const {ids}=require('./checker-fixtures');
test('UI sends optional locators, shows pack and manifest link, escapes evidence',async()=>{
 const html=fs.readFileSync('docs/check.html','utf8');
 assert.match(html,/id="manifestTxid"/);assert.match(html,/id="mintTxid"/);
 const elements={txid:{value:ids.open},manifestTxid:{value:ids.manifest},mintTxid:{value:ids.mint},out:{innerHTML:''}};
 const ctx=vm.createContext({document:{getElementById:id=>elements[id]},VaultCheck:{checkBox:async(id,k,opts)=>{
 assert.equal(opts.manifestTxid,ids.manifest);assert.equal(opts.mintTxid,ids.mint);
 return {verdict:'OPENED-VERIFIED',evidence:['<img src=x onerror=alert(1)>'],outputs:[{pack:{designs:[1,2,3]},manifestTxid:ids.manifest}],confirmations:3};}}});
 vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],ctx);await ctx.run();
 assert.match(elements.out.innerHTML,/Pack: 1, 2, 3/);assert.ok(elements.out.innerHTML.includes('https://whatsonchain.com/tx/'+ids.manifest));assert.ok(!elements.out.innerHTML.includes('<img'));
 for(const verdict of ['OPENED-SPENT','INVALID-MANIFEST']){
  ctx.VaultCheck.checkBox=async()=>({verdict,evidence:['Not payable'],outputs:[]});await ctx.run();
  assert.ok(elements.out.innerHTML.includes('class="verdict bad"'));
 }
});
