'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {createDemo,requestFor,reduce}=require('./engine');
const {FixtureWallet,FixtureTransport}=require('./fixture-wallet');
const {sha,canonical,M,tx}=require('./common');
const {DatabaseSync}=require('node:sqlite');
const dir=path.join(__dirname,'.test-runs');fs.mkdirSync(dir,{recursive:true});
function file(){return path.join(fs.mkdtempSync(path.join(dir,'negative-')),'journal.sqlite');}
for(const mode of ['reject','disconnect','wrong-buyer','wrong-network','malicious']) test('wallet '+mode+' leaves reservation unallocated',async()=>{
  const transport=new FixtureTransport(),e=createDemo(file(),{wallet:new FixtureWallet(mode),transport});
  try{await assert.rejects(e.reserve('reserve'));assert.equal(e.inspect().stage,'AVAILABLE');assert.equal(e.inspect().events,1);assert.equal(transport.sent.length,0);}finally{e.close();}
});
for(const field of ['designId','metadataSha256','origin','buyerPubkey']) test('swapped '+field+' rejected even with recomputed local journal hashes',async()=>{
  const p=file(),e=createDemo(p);await e.reserve('reserve');e.close();
  const db=new DatabaseSync(p);
  const row=db.prepare('SELECT * FROM events WHERE seq=2').get(),event=JSON.parse(row.payload);
  event.binding[field]=field==='designId'?'japan':'00'.repeat(32);
  const payload=canonical(event);db.prepare('UPDATE events SET payload=?,digest=? WHERE seq=2').run(payload,sha(row.previous+payload));db.close();
  assert.throws(()=>createDemo(p),/immutable binding mismatch/);
});
test('valid signature on different binding is rejected at application boundary',async()=>{
  const e=createDemo(file());
  try {
    const {state:s}=e.journal.read(),request=requestFor(s,'reserve','Reserve');
    request.binding={...request.binding,designId:'japan'};
    const response=await new FixtureWallet().request(request);
    assert.throws(()=>reduce(s,{type:'RESERVE',binding:s.binding,request,response}));
  }finally{e.close();}
});
test('duplicate reservation and transition do not sign or dispense twice',async()=>{
  const wallet=new FixtureWallet(),transport=new FixtureTransport(),e=createDemo(file(),{wallet,transport});
  try{
    await e.reserve('reserve');await e.reserve('reserve');assert.equal(wallet.calls,1);
    await e.advance('pack');const state=e.inspect();await e.advance('pack');
    assert.equal(wallet.calls,2);assert.equal(transport.sent.length,1);assert.equal(e.inspect().head,state.head);
    await assert.rejects(e.reserve('pack'),/duplicate request changed/);
    await assert.rejects(e.advance('reserve'),/duplicate request changed/);
  }finally{e.close();}
});
test('restart at prepared handoff uses exact saved signed bytes without wallet or new funding',async()=>{
  const p=file(),transport=new FixtureTransport();
  let e=createDemo(p,{transport,hooks:{afterPrepared(){throw Error('crash after preparation');}}});
  await e.reserve('reserve');await assert.rejects(e.advance('pack'),/crash/);
  const before=e.inspect().pending.response;e.close();
  const wallet=new FixtureWallet('disconnect');e=createDemo(p,{transport,wallet});
  try{await e.advance('pack');assert.equal(wallet.calls,0);assert.deepEqual(e.inspect().history[0].response,before);assert.deepEqual(transport.sent,[before.raw]);}finally{e.close();}
});
test('crash after durable attempt never retries or replaces funding on restart',async()=>{
  const p=file(),transport=new FixtureTransport();
  let e=createDemo(p,{transport,hooks:{afterAttempt(){throw Error('crash after attempt');}}});
  await e.reserve('reserve');await assert.rejects(e.advance('pack'),/crash/);const before=e.inspect().pending.response;e.close();
  const wallet=new FixtureWallet();e=createDemo(p,{transport,wallet});
  try{await assert.rejects(e.advance('pack'),/Interrupted send quarantined/);assert.deepEqual(e.inspect().pending.response,before);assert.equal(wallet.calls,0);assert.equal(transport.sent.length,0);assert.deepEqual(e.inspect().holds,['INTERRUPTED_SEND']);}finally{e.close();}
});
test('ambiguous send holds exact raw/funding bytes across restart with no retry',async()=>{
  const p=file(),transport=new FixtureTransport('ambiguous');let e=createDemo(p,{transport});
  await e.reserve('reserve');await assert.rejects(e.advance('pack'),/Ambiguous send quarantined/);
  const before=e.inspect().pending.response;e.close();
  const wallet=new FixtureWallet();e=createDemo(p,{transport,wallet});
  try{await assert.rejects(e.advance('pack'),/reconciliation hold/);assert.deepEqual(e.inspect().pending.response,before);assert.equal(transport.sent.length,1);assert.equal(transport.sent[0],before.raw);assert.equal(wallet.calls,0);}finally{e.close();}
});
test('authentically signed wallet response with wrong transition fails before send',async()=>{
  const wallet=new FixtureWallet(),transport=new FixtureTransport(),e=createDemo(file(),{wallet,transport});
  try {
    await e.reserve('reserve');await e.advance('pack');
    const honest=wallet.request.bind(wallet);
    wallet.request=async request=>{
      const response=await honest(request);
      // Re-sign a seal response that claims a changed raw payload. Real valid envelope signature, invalid Script.
      const t=tx(response.raw);t.outputs[0].satoshis=2;response.raw=t.uncheckedSerialize();
      const {signature,...body}=response;
      const key=new M.bsv.PrivateKey(new M.bsv.crypto.BN(1),M.bsv.Networks.testnet);
      response.signature=M.bsv.crypto.ECDSA.sign(Buffer.from(sha(canonical(body)),'hex'),key).toDER().toString('hex');
      return response;
    };
    await assert.rejects(e.advance('seal'));
    assert.equal(e.inspect().stage,'PACKED');assert.equal(transport.sent.length,1);assert.equal(e.inspect().pending,null);
  }finally{e.close();}
});
test('explicit action prevents stale browser request from executing the next phase',async()=>{
  const e=createDemo(file());try{
    await e.reserve('reserve');await e.advance('pack','Pack');
    await assert.rejects(e.advance('stale-pack','Pack'),/unexpected action/);
    await assert.rejects(e.advance('pack','Seal'),/duplicate request changed/);
    assert.equal(e.inspect().stage,'PACKED');
  }finally{e.close();}
});
test('overlapping and cross-instance requests cannot both reach send',async()=>{
  const p=file(),transport=new FixtureTransport(),wallet=new FixtureWallet(),e=createDemo(p,{wallet,transport});
  await e.reserve('reserve');const second=createDemo(p,{transport});
  try{
    let release;const gate=new Promise(r=>{release=r;});const original=wallet.request.bind(wallet);
    wallet.request=async req=>{await gate;return original(req);};
    const pending=e.advance('pack');await assert.rejects(e.advance('other'),/operation busy/);
    const other=second.advance('pack-other');release();
    const results=await Promise.allSettled([pending,other]);
    assert.ok(results.some(x=>x.status==='fulfilled'));assert.equal(transport.sent.length,1);
  }finally{e.close();second.close();}
});
test('finality/excess holds preserve confirmed ownership history and cannot reopen allocation',async()=>{
  const e=createDemo(file());
  try{
    await e.reserve('reserve');for(const k of ['pack','seal','transfer'])await e.advance(k);
    const before=e.inspect();e.hold('FINALITY_LOST');e.hold('EXCESS_PAYMENT');const after=e.inspect();
    assert.equal(after.stage,'TRANSFERRED');assert.deepEqual(after.history,before.history);
    await assert.rejects(e.advance('open'),/reconciliation hold/);await assert.rejects(e.reserve('replacement'));
  }finally{e.close();}
});
