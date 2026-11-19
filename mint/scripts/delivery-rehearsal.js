'use strict';
// Offline public-fixture execution ONLY; no live node/network or key discovery.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {Delivery}=require('../delivery'),{SaleStore}=require('../sale'),{PaymentWatcher}=require('../watcher'),Canary=require('../canary');
const {fixture}=require('../test/delivery-fixture'),F=require('../../launch/continuous/fixture-wallet'),C=require('../../launch/continuous/common');
async function main() {
  const [destination,design='japan']=process.argv.slice(2);
  assert.ok(destination,'usage: node mint/scripts/delivery-rehearsal.js NEW_DIRECTORY [design-slug]');
  const dir=path.resolve(destination);assert.ok(!fs.existsSync(dir),'fresh evidence directory required');fs.mkdirSync(dir,{recursive:true});
  const config={mode:'offline-rehearsal',network:C.NETWORK,issuerPubkey:F.policy.seller,paymentDepth:2,deliveryDepth:2,termsRef:'TEST-ONLY-NOT-APPROVED'};
  const f=await fixture(design,'box-1');
  const hd=C.M.bsv.HDPrivateKey.fromSeed(Buffer.alloc(32,7),C.M.bsv.Networks.testnet);
  const store=new SaleStore({file:path.join(dir,'sales.jsonl'),xpub:hd.hdPublicKey.toString(),chain:'regtest'});
  let d;
  try {
    const listed=store.list({priceSats:100,inventoryId:f.reservation.inventoryId});
    const reservation=store.reserve(listed.id,F.policy.buyer,10000);
    const payment={policy:Canary.policy({chain:'regtest'}),read:async()=>({satoshis:100,confirmations:2,refs:['a'.repeat(64)+':0']})};
    const wallet=new F.FixtureWallet(),transport=new F.FixtureTransport();
    d=new Delivery(path.join(dir,'delivery.sqlite'),{config,wallet,transport,payment,now:()=>100});
    d.enroll(reservation,f.state,f.funding);
    const watcher=new PaymentWatcher({chain:'regtest',transport:payment,depth:2});watcher.watch(reservation);
    await watcher.poll(event=>d.onPayment(event));await watcher.poll(event=>d.onPayment(event));
    const result=d.inspect(reservation.id);assert.equal(result.status,'LOCAL_ACCEPTED');assert.equal(transport.sent.length,1);
    fs.writeFileSync(path.join(dir,'config.json'),JSON.stringify(config,null,2)+'\n');
    fs.writeFileSync(path.join(dir,'evidence.json'),JSON.stringify(result,null,2)+'\n');
    console.log(JSON.stringify({status:result.status,binding:result.binding,txid:C.tx(result.prepared.raw).id,signatures:wallet.calls,localSends:transport.sent.length,realBroadcasts:0,chainInclusion:false,launchReady:false},null,2));
  } finally {d?.close();store.close();}
}
main().catch(e=>{console.error(e.message);process.exitCode=1;});
