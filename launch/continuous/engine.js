'use strict';
// Application orchestration: no private keys, wallet discovery or network fetch.
const {DatabaseSync}=require('node:sqlite');
const {fs,path,assert,M,NETWORK,ACTIONS,sha,canonical,candidate,verifySignature,raw,tx}=require('./common');
const {verifyLaunch}=require('../../vault/src/launch-record');
const Fixture=require('./fixture-wallet');
const STAGES=['RESERVED','PACKED','SEALED','TRANSFERRED','OPENED','WITHDRAWN'];
function provenance(s) {
  return verifyLaunch({f:{foreign:tx(s.inventory.foreign),box:tx(s.inventory.box)},entries:s.history.map(h=>tx(h.response.raw)),fundingParents:s.history.map(h=>tx(h.response.funding)),metadata:s.inventory.metadata,envelope:s.inventory.envelope,mediaHashes:{modelSha256:s.candidate.model.sha256,artSha256:s.candidate.art.sha256},policy:{issuer:s.policy.seller,collectionId:'boxes-from-impossible-places',designId:s.binding.designId}});
}
function requestFor(s,key,action) {
  const request={protocol:'BOXSV-CONTINUOUS-REQUEST-1',network:s.policy.network||NETWORK,key,action,binding:s.binding};
  if(action!=='Reserve') Object.assign(request,{actionIndex:ACTIONS.indexOf(action),inventory:s.inventory,source:s.history.at(-1)?.response.raw||null});
  return request;
}
function verifyResponse(s,request,response,fundingPolicy) {
  const signer=request.action==='Reserve'||request.action==='Open'||request.action==='Withdraw'?s.policy.buyer:s.policy.seller;
  const brc=Object.hasOwn(response,'authorizations');
  if(brc)require('./integrated-wallet').verifyAuthorizations(s,request,response);
  const {signature,...signed}=response;
  assert.equal(response.network,s.policy.network||NETWORK,'wrong network');
  assert.equal(response.signer,signer,'wrong buyer/owner');
  assert.equal(response.requestHash,sha(canonical(request)),'signed response request mismatch');
  if(!brc)assert.ok(verifySignature(canonical(signed),signature,signer),'malicious wallet signed response');
  if(request.action==='Reserve') {assert.deepEqual(Object.keys(response).sort(),(brc?['authorizations','network','requestHash','signer']:['network','requestHash','signature','signer']));return;}
  assert.deepEqual(Object.keys(response).sort(),(brc?['authorizations','funding','fundingRoot','network','raw','requestHash','signer']:['funding','fundingRoot','network','raw','requestHash','signature','signer']));
  const t=tx(response.raw), funding=tx(response.funding), root=tx(response.fundingRoot);
  assert.equal(raw(t),response.raw,'noncanonical transaction');
  assert.equal(funding.outputs.length,1);assert.equal(funding.outputs[0].satoshis,fundingPolicy?.amount??100000);
  assert.equal(funding.outputs[0].script.toHex(),M.pay(s.policy.sponsor).toHex());
  assert.ok(M.verify(funding,[root]).success,'funding preparation Script');
  if(fundingPolicy) {
    assert.equal(response.funding,fundingPolicy.raw,'pinned funding changed');
    assert.equal(response.fundingRoot,fundingPolicy.root,'pinned funding root changed');
    assert.ok(Number.isSafeInteger(fundingPolicy.amount)&&Number.isSafeInteger(fundingPolicy.change)&&fundingPolicy.change>0&&fundingPolicy.change<fundingPolicy.amount,'explicit fee policy required');
  } else {
  assert.equal(root.outputs.length,1);assert.equal(root.outputs[0].satoshis,100500);
  assert.equal(root.outputs[0].script.toHex(),M.pay(s.policy.sponsor).toHex());
  // Synthetic root identity is deterministic and frozen per prior custody tip.
  const prior=request.source?tx(request.source):tx(s.inventory.box);
  assert.equal(root.inputs.length,1);
  assert.equal(root.inputs[0].prevTxId.toString('hex'),M.bsv.crypto.Hash.sha256(Buffer.from('BoxSV sponsor root:'+prior.id)).toString('hex'));
  }
  assert.equal(t.inputs.length,3);assert.equal(t.outputs.length,3);
  assert.equal(t.inputs[2].prevTxId.toString('hex'),funding.id);assert.equal(t.inputs[2].outputIndex,0);
  assert.equal(t.outputs[2].satoshis,fundingPolicy?.change??99500);assert.equal(t.outputs[2].script.toHex(),M.pay(s.policy.sponsor).toHex());
  for(let i=0;i<2;i++) assert.equal(t.outputs[i].satoshis,1);
  const nextOwner=request.actionIndex>=2?s.policy.buyer:s.policy.seller;
  if(request.action==='Withdraw') {
    for(let i=0;i<2;i++) assert.equal(t.outputs[i].script.toHex(),M.pay(nextOwner).toHex(),'withdraw recipient');
  } else {
    const initial=M.C.fromHex(tx(s.inventory.box).outputs[0].script.toHex());
    const phase=BigInt([1,2,2,3][request.actionIndex]);
    const expected=initial.getNewStateScript({phase,owner:nextOwner}).toHex();
    for(let i=0;i<2;i++) assert.equal(t.outputs[i].script.toHex(),expected,'wrong transition or owner');
  }
  const f={foreign:tx(s.inventory.foreign),box:tx(s.inventory.box)};
  const history=[...s.history.map(h=>tx(h.response.raw)),t];
  const parents=[...s.history.map(h=>tx(h.response.funding)),funding];
  const result=M.verifyHistory(f,history,parents);
  assert.ok(result.valid,'anchored VM replay: '+result.error);
}
function reduce(s,e,policy=Fixture.policy) {
  if(e.type==='INIT') {
    assert.equal(s,null,'duplicate initialization');
    const c=candidate();
    assert.deepEqual(e.candidate,c,'candidate changed');assert.deepEqual(e.policy,policy,'fixture trust policy changed');
    const i=e.inventory;
    assert.ok(M.verify(tx(i.foreign),[tx(i.originRoot)]).success,'independent issuance signature');
    assert.ok(M.verify(tx(i.box),[tx(i.boxRoot)]).success,'box issuance signature');
    assert.equal(i.metadata,c.metadata);
    const binding={designId:c.item.slug,designIdentity:c.item.id,manifestSha256:c.manifestSha256,buyerPubkey:e.policy.buyer,metadataSha256:c.metadataSha256,origin:tx(i.foreign).id+'_0'};
    assert.deepEqual(e.binding,binding,'immutable binding mismatch');
    s={candidate:c,policy:e.policy,inventory:i,binding,stage:'AVAILABLE',history:[],requests:{},pending:null,holds:[]};
    assert.ok(Object.values(provenance(s)).every(Boolean),'initial provenance');
    return s;
  }
  assert.ok(s,'missing initialization');assert.deepEqual(e.binding,s.binding,'immutable binding mismatch');
  if(e.type==='RESERVE') {
    assert.equal(s.stage,'AVAILABLE');assert.equal(s.holds.length,0);
    assert.deepEqual(e.request,requestFor(s,e.request.key,'Reserve'));
    verifyResponse(s,e.request,e.response);
    s.stage='RESERVED';s.reservation=e.request.key;s.requests[e.request.key]='Reserve';
  } else if(e.type==='PREPARED') {
    assert.equal(s.holds.length,0,'reconciliation hold');assert.equal(s.pending,null,'pending request');
    assert.equal(s.stage,STAGES[s.history.length]);
    assert.ok(!Object.hasOwn(s.requests,e.request.key),'duplicate request');
    assert.deepEqual(e.request,requestFor(s,e.request.key,ACTIONS[s.history.length]),'request binding mismatch');
    verifyResponse(s,e.request,e.response);
    s.pending={request:e.request,response:e.response,attempted:false};
  } else if(e.type==='ATTEMPT') {
    assert.equal(s.holds.length,0);assert.ok(s.pending&&!s.pending.attempted,'already attempted');
    assert.equal(e.txid,tx(s.pending.response.raw).id);s.pending.attempted=true;
  } else if(e.type==='ACCEPTED') {
    assert.equal(s.holds.length,0);assert.ok(s.pending?.attempted);
    assert.deepEqual(e.receipt,{network:NETWORK,kind:'LOCAL_VM_ACCEPTED_NOT_CHAIN_INCLUSION',txid:tx(s.pending.response.raw).id,rawSha256:sha(Buffer.from(s.pending.response.raw,'hex'))});
    s.history.push({action:s.pending.request.action,request:s.pending.request,response:s.pending.response,receipt:e.receipt,vm:true});
    s.requests[s.pending.request.key]=s.pending.request.action;
    s.pending=null;s.stage=STAGES[s.history.length];
  } else if(e.type==='HOLD') {
    assert.ok(['AMBIGUOUS_SEND','INTERRUPTED_SEND','FINALITY_LOST','EXCESS_PAYMENT'].includes(e.reason));
    if(!s.holds.includes(e.reason))s.holds.push(e.reason);
  } else throw Error('unknown event');
  return s;
}
class Journal {
  constructor(file,initial,policy=Fixture.policy) {
    this.reduce=(s,e)=>reduce(s,e,policy);
    const exists=fs.existsSync(file);
    fs.mkdirSync(path.dirname(path.resolve(file)),{recursive:true});
    this.db=new DatabaseSync(file);
    try {
      this.db.exec('PRAGMA synchronous=FULL; PRAGMA busy_timeout=3000;');
      if(!exists) {
        this.db.exec('BEGIN IMMEDIATE; CREATE TABLE events(seq INTEGER PRIMARY KEY, previous TEXT NOT NULL, digest TEXT NOT NULL, payload TEXT NOT NULL);');
        try { const e=initial();this.reduce(null,e);const payload=canonical(e);this.db.prepare('INSERT INTO events VALUES(1,?,?,?)').run('',sha(payload),payload);this.db.exec('COMMIT'); }
        catch(error){this.db.exec('ROLLBACK');throw error;}
      }
      this.read();
    }catch(e){this.db.close();throw e;}
  }
  read() {
    const rows=this.db.prepare('SELECT * FROM events ORDER BY seq').all();
    assert.ok(rows.length,'empty journal');let state=null,previous='';
    for(const [index,r] of rows.entries()) {
      assert.equal(r.seq,index+1);assert.equal(r.previous,previous);
      assert.equal(r.digest,sha(previous+r.payload),'journal hash mismatch');
      const e=JSON.parse(r.payload);assert.equal(canonical(e),r.payload);
      state=this.reduce(state,e);previous=r.digest;
    }
    return {state,head:previous,events:rows.length};
  }
  append(e,head) {
    this.db.exec('BEGIN IMMEDIATE');
    try {
      const current=this.read();assert.equal(current.head,head,'concurrent state change');this.reduce(current.state,e);
      const payload=canonical(e);this.db.prepare('INSERT INTO events VALUES(?,?,?,?)').run(current.events+1,head,sha(head+payload),payload);
      this.db.exec('COMMIT');
    } catch(error){this.db.exec('ROLLBACK');throw error;}
  }
  close(){this.db.close();}
}
class Engine {
  constructor(journal,{wallet,transport,hooks={},beforeAttempt}) {this.journal=journal;this.wallet=wallet;this.transport=transport;this.hooks=hooks;this.beforeAttempt=beforeAttempt;this.busy=false;}
  inspect() {
    const {state:s,head,events}=this.journal.read();
    return {...s,head,events,provenance:provenance(s),originalOutpoint:s.binding.origin,withdrawnOwner:s.stage==='WITHDRAWN'?s.binding.buyerPubkey:null,simulation:true,chainInclusion:false,launchReady:false};
  }
  async exclusive(fn) {assert.ok(!this.busy,'operation busy');this.busy=true;try{return await fn();}finally{this.busy=false;}}
  async reserve(key) {return this.exclusive(async()=>{
    assert.match(key,/^[a-zA-Z0-9-]{1,80}$/);
    const {state:s,head}=this.journal.read();
    if(Object.hasOwn(s.requests,key)){assert.equal(s.requests[key],'Reserve','duplicate request changed');return this.inspect();}
    assert.equal(s.stage,'AVAILABLE');assert.equal(s.holds.length,0,'reconciliation hold');
    const request=requestFor(s,key,'Reserve'),response=await this.wallet.request(structuredClone(request));
    this.journal.append({type:'RESERVE',binding:s.binding,request,response},head);return this.inspect();
  });}
  async advance(key,expectedAction) {return this.exclusive(async()=>{
    assert.match(key,/^[a-zA-Z0-9-]{1,80}$/);
    let {state:s,head}=this.journal.read();
    if(Object.hasOwn(s.requests,key)) {assert.notEqual(s.requests[key],'Reserve','duplicate request changed');if(expectedAction!==undefined)assert.equal(s.requests[key],expectedAction,'duplicate request changed');return this.inspect();}
    if(expectedAction!==undefined)assert.equal(expectedAction,ACTIONS[s.history.length],'unexpected action');
    assert.equal(s.holds.length,0,'reconciliation hold');
    assert.ok(s.stage!=='AVAILABLE'&&s.stage!=='WITHDRAWN','not eligible');
    if(!s.pending) {
      const request=requestFor(s,key,ACTIONS[s.history.length]),response=await this.wallet.request(structuredClone(request));
      this.journal.append({type:'PREPARED',binding:s.binding,request,response},head);
      if(this.hooks.afterPrepared) await this.hooks.afterPrepared();
      ({state:s,head}=this.journal.read());
    }
    assert.equal(s.pending.request.key,key,'pending request key mismatch');
    if(s.pending.attempted) {
      this.journal.append({type:'HOLD',binding:s.binding,reason:'INTERRUPTED_SEND'},head);
      throw Error('Interrupted send quarantined; same bytes retained, no retry');
    }
    // Trusted composition guard: also runs for prepared-only recovery, never retries an attempt.
    if(this.beforeAttempt)await this.beforeAttempt(structuredClone(s.pending.request));
    this.journal.append({type:'ATTEMPT',binding:s.binding,txid:tx(s.pending.response.raw).id},head);
    ({state:s,head}=this.journal.read());
    if(this.hooks.afterAttempt) await this.hooks.afterAttempt();
    try {
      const receipt=await this.transport.send(s.pending.response.raw);
      this.journal.append({type:'ACCEPTED',binding:s.binding,receipt},head);
    } catch(error) {
      this.journal.append({type:'HOLD',binding:s.binding,reason:'AMBIGUOUS_SEND'},head);
      throw Error('Ambiguous send quarantined; same bytes retained, no replacement funding');
    }
    return this.inspect();
  });}
  hold(reason){assert.ok(!this.busy,'operation busy');const {state:s,head}=this.journal.read();this.journal.append({type:'HOLD',binding:s.binding,reason},head);return this.inspect();}
  close(){assert.ok(!this.busy,'operation busy');this.journal.close();}
}
function createDemo(file,options={}) {
  const journal=new Journal(file,()=>{
    const c=candidate(),inventory=Fixture.issue(c),policy=options.policy||Fixture.policy;
    const binding={designId:c.item.slug,designIdentity:c.item.id,manifestSha256:c.manifestSha256,buyerPubkey:policy.buyer,metadataSha256:c.metadataSha256,origin:tx(inventory.foreign).id+'_0'};
    return {type:'INIT',candidate:c,inventory,policy,binding};
  },options.policy||Fixture.policy);
  return new Engine(journal,{wallet:options.wallet||new Fixture.FixtureWallet(),transport:options.transport||new Fixture.FixtureTransport(),hooks:options.hooks,beforeAttempt:options.beforeAttempt});
}
module.exports={createDemo,Engine,Journal,requestFor,verifyResponse,reduce,provenance};
