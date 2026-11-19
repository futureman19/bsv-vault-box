'use strict';
// Public deterministic test data only. Never fund these keys.
const fs=require('node:fs'),path=require('node:path');
const C=require('../../launch/continuous/common'),F=require('../../launch/continuous/fixture-wallet');
const {requestFor}=require('../../launch/continuous/engine');
async function fixture(slug='japan',id='order-1') {
  const item=JSON.parse(fs.readFileSync(path.join(C.ROOT,'launch/collection/upstream/candidate-manifest.json'))).items.find(x=>x.slug===slug);
  const model=item.files.find(x=>x.role==='model'),art=item.files.find(x=>x.role==='promotional-illustration');
  const metadata=JSON.stringify({protocol:'BOXSV-LAUNCH-METADATA-1',collectionId:'boxes-from-impossible-places',designId:slug,modelSha256:model.sha256,artSha256:art.sha256});
  const candidate={item,model,art,metadata,metadataSha256:C.sha(metadata),manifestSha256:C.candidate().manifestSha256};
  const inventory=F.issue(candidate),binding={designId:slug,designIdentity:item.id,manifestSha256:candidate.manifestSha256,buyerPubkey:F.policy.buyer,metadataSha256:candidate.metadataSha256,origin:C.tx(inventory.foreign).id+'_0'};
  const state={candidate,inventory,binding,policy:F.policy,history:[]};
  const wallet=new F.FixtureWallet();
  for(const action of ['Pack','Seal']) {const request=requestFor(state,action,action),response=await wallet.request(request);state.history.push({action,request,response});}
  const response=await wallet.request(requestFor(state,'delivery-'+id,'Transfer'));
  const funding={raw:response.funding,root:response.fundingRoot,amount:100000,change:99500};
  const reservation={id,inventoryId:C.tx(state.history[1].response.raw).id,buyerPubkey:F.policy.buyer,payAddress:C.M.bsv.PublicKey.fromString(F.policy.buyer).toAddress(C.M.bsv.Networks.testnet).toString(),priceSats:100,expiresAt:10000};
  return {state,funding,reservation};
}
module.exports={fixture};
