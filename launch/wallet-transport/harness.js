'use strict';
const assert=require('node:assert/strict');
const {fixture,bsv}=require('./fixture');
const {WalletTransport,requestHash,verifyResponse}=require('./adapter');
const M=require('../../vault/src/ordinal-pair');
async function run(){
 const f=await fixture(),adapter=new WalletTransport(f.provider,f.policy);
 const response=await adapter.request(f.request,{expectedRequestHash:requestHash(f.request)});
 assert.equal(verifyResponse(f.request,response,f.policy),true);
 f.transaction.inputs[0].setScript(bsv.Script.fromASM(response.transactionSignature+' '+f.policy.signingKey));
 const vm=M.verify(f.transaction,[f.parent]);assert.ok(vm.success,JSON.stringify(vm));
 return {label:'PUBLIC_FIXTURE_SDK_SIGNING_NOT_EXTENSION_NOT_CHAIN',network:'testnet',syntheticRoots:true,request:f.request,response,raw:f.transaction.uncheckedSerialize(),txid:f.transaction.id,vm,providerMethods:f.calls.map(c=>c[0]),realSends:0};
}
if(require.main===module)run().then(r=>console.log(JSON.stringify(r,null,2))).catch(e=>{console.error(e);process.exitCode=1;});
module.exports={run};
