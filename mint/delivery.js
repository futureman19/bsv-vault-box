'use strict';
// Sequential payment -> custody delivery, NOT atomic settlement. No key loading,
// network implementation, refund, replenishment, relisting or production enable switch.
const {DatabaseSync}=require('node:sqlite');
const {fs,path,assert,M,ROOT,sha,canonical,tx}=require('../launch/continuous/common');
const {requestFor,verifyResponse,provenance}=require('../launch/continuous/engine');
const MANIFEST='307598fa4fa9aa4a9abef8d14dbc8bf7ee54c1e22589beb3ea43ec051796b3cb';
const copy=x=>JSON.parse(canonical(x));
const positive=x=>assert.ok(Number.isSafeInteger(x)&&x>0,'positive integer policy required');
const terminal=s=>['LOCAL_ACCEPTED','CONFIRMED','REHEARSED_CONFIRMED'].includes(s);
function policy(c) {
  assert.ok(c,'configuration required');
  assert.ok(['offline-fixture','regtest','testnet','mainnet'].includes(c.network));
  positive(c.paymentDepth);positive(c.deliveryDepth);
  assert.ok(M.bsv.PublicKey.isValid(c.issuerPubkey),'external issuer policy required');
  assert.ok(typeof c.termsRef==='string'&&c.termsRef.length>0,'terms decision reference required');
  return {schema:1,network:c.network,issuerPubkey:c.issuerPubkey,paymentDepth:c.paymentDepth,deliveryDepth:c.deliveryDepth,termsRef:c.termsRef};
}
function validateEnrollment(r,s,f,network) {
  assert.match(r.id,/^[a-zA-Z0-9-]{1,60}$/);positive(r.priceSats);positive(r.expiresAt);
  assert.equal(r.buyerPubkey,s.binding.buyerPubkey);assert.equal(s.policy.buyer,r.buyerPubkey);
  assert.ok(M.bsv.PublicKey.isValid(r.buyerPubkey));
  const address=M.bsv.Address.fromString(r.payAddress);
  assert.equal(address.network.name,network==='mainnet'?'livenet':'testnet','payment address network');
  assert.equal(s.policy.network,network,'custody network');
  const bytes=fs.readFileSync(path.join(ROOT,'launch/collection/upstream/candidate-manifest.json'));
  assert.equal(sha(bytes),MANIFEST,'external candidate manifest pin');
  const items=JSON.parse(bytes).items;
  assert.equal(items.length,201);assert.equal(new Set(items.map(x=>x.id)).size,201);
  const item=items.find(x=>x.slug===s.binding.designId);assert.ok(item,'selected design not in roster');
  assert.deepEqual(s.candidate.item,item,'exact selected design');
  assert.equal(s.binding.designIdentity,item.id);assert.equal(s.binding.manifestSha256,MANIFEST);
  assert.equal(s.candidate.manifestSha256,MANIFEST);
  assert.deepEqual(s.candidate.model,item.files.find(x=>x.role==='model'));
  assert.deepEqual(s.candidate.art,item.files.find(x=>x.role==='promotional-illustration'));
  assert.equal(s.candidate.metadata,s.inventory.metadata);
  assert.equal(s.binding.metadataSha256,sha(s.inventory.metadata));
  assert.equal(s.candidate.metadataSha256,s.binding.metadataSha256);
  assert.equal(s.binding.origin,tx(s.inventory.foreign).id+'_0');
  assert.equal(s.history.length,2,'already packed and sealed custody required');
  assert.deepEqual(s.history.map(h=>h.action),['Pack','Seal']);
  assert.ok(Object.values(provenance(s)).every(Boolean),'signed origin/metadata/custody verification');
  const sealed=tx(s.history[1].response.raw);
  assert.equal(r.inventoryId,sealed.id,'reservation allocation differs from sealed source');
  const c=M.C.fromHex(sealed.outputs[0].script.toHex());
  assert.equal(c.phase,2n);assert.equal(c.owner,s.policy.seller,'seller must own sealed custody');
  assert.equal(sealed.outputs[1].script.toHex(),sealed.outputs[0].script.toHex());
  positive(f.amount);positive(f.change);assert.ok(f.change<f.amount,'explicit fee required');
  const funding=tx(f.raw),root=tx(f.root);
  assert.equal(funding.outputs.length,1);assert.equal(funding.outputs[0].satoshis,f.amount);
  assert.equal(funding.outputs[0].script.toHex(),M.pay(s.policy.sponsor).toHex());
  assert.ok(M.verify(funding,[root]).success,'funding signature');
}
function observation(p) {
  assert.ok(p&&Number.isSafeInteger(p.satoshis)&&p.satoshis>=0,'payment amount');
  assert.ok(Number.isSafeInteger(p.confirmations)&&p.confirmations>=0,'payment depth');
  assert.ok(Array.isArray(p.refs)&&p.refs.length<=1000&&new Set(p.refs).size===p.refs.length,'receipt refs');
  for(const ref of p.refs)assert.match(ref,/^[0-9a-f]{64}:(0|[1-9][0-9]{0,9})$/);
  assert.equal(p.satoshis>0,p.refs.length>0,'payment refs required');
  return {satoshis:p.satoshis,confirmations:p.confirmations,refs:[...p.refs].sort()};
}
class Delivery {
  constructor(file,{config,readOnly=false,...adapters}={}) {
    this.pin=policy(config);this.mode=config.mode||'disabled';this.readOnly=readOnly;
    this.adapters=adapters;this.closed=false;this.busy=false;
    assert.ok(path.isAbsolute(file),'absolute delivery database required');
    const exists=fs.existsSync(file);assert.ok(exists||!readOnly,'recovery database missing');
    this.db=new DatabaseSync(file,{readOnly});
    try {
      this.db.exec('PRAGMA busy_timeout=3000;');
      if(!readOnly)this.db.exec('PRAGMA synchronous=FULL;');
      if(!exists) {
        this.db.exec('BEGIN IMMEDIATE; CREATE TABLE configuration(payload TEXT NOT NULL); CREATE TABLE orders(id TEXT PRIMARY KEY, design TEXT UNIQUE NOT NULL, origin TEXT UNIQUE NOT NULL, address TEXT UNIQUE NOT NULL, funding TEXT UNIQUE NOT NULL, payload TEXT NOT NULL); CREATE TABLE events(seq INTEGER PRIMARY KEY, id TEXT NOT NULL, previous TEXT NOT NULL, digest TEXT NOT NULL, payload TEXT NOT NULL); CREATE TABLE receipts(ref TEXT PRIMARY KEY, id TEXT NOT NULL); PRAGMA user_version=1;');
        this.db.prepare('INSERT INTO configuration VALUES(?)').run(canonical(this.pin));this.db.exec('COMMIT');
      }
      assert.equal(this.db.prepare('PRAGMA user_version').get().user_version,1,'migration required');
      assert.deepEqual(JSON.parse(this.db.prepare('SELECT payload FROM configuration').get().payload),this.pin,'configuration policy changed');
      for(const {id} of this.db.prepare('SELECT id FROM orders').all())this.inspect(id);
    }catch(e){this.db.close();this.closed=true;throw e;}
  }
  writable(){assert.ok(!this.closed&&!this.readOnly,'read-only or closed delivery');}
  atomic(fn){this.writable();this.db.exec('BEGIN IMMEDIATE');try{const v=fn();this.db.exec('COMMIT');return v;}catch(e){this.db.exec('ROLLBACK');throw e;}}
  enroll(reservation,state,funding) {
    const r={id:reservation.id,inventoryId:reservation.inventoryId,buyerPubkey:reservation.buyerPubkey,payAddress:reservation.payAddress,priceSats:reservation.priceSats,expiresAt:reservation.expiresAt};
    // Accept SaleStore's reserved shape, not LISTED/unbound or already refund-held state.
    assert.ok(!reservation.refundRequired&&!reservation.reconciliationRequired,'reservation held');
    assert.ok(!reservation.state||['LISTED','PAID_PENDING'].includes(reservation.state),'reservation no longer eligible');
    assert.ok(!state.holds?.length,'upstream custody held');
    assert.ok(!state.pending,'upstream custody pending');
    const s={candidate:state.candidate,inventory:state.inventory,binding:state.binding,policy:state.policy,history:state.history};
    assert.equal(s.policy.seller,this.pin.issuerPubkey,'external issuer policy mismatch');
    validateEnrollment(r,s,funding,this.pin.network);
    const payload=canonical({reservation:r,custody:s,funding});
    return this.atomic(()=>{
      const prior=this.db.prepare('SELECT payload FROM orders WHERE id=?').get(r.id);
      if(prior){assert.equal(prior.payload,payload,'immutable reservation binding conflict');return this.inspect(r.id);}
      this.db.prepare('INSERT INTO orders VALUES(?,?,?,?,?,?)').run(r.id,s.binding.designIdentity,s.binding.origin,r.payAddress,tx(funding.raw).id,payload);
      return this.inspect(r.id);
    });
  }
  inspect(id) {
    assert.ok(!this.closed,'closed delivery');
    const row=this.db.prepare('SELECT * FROM orders WHERE id=?').get(id);assert.ok(row,'unknown reservation');
    const base=JSON.parse(row.payload);assert.equal(canonical(base),row.payload);
    assert.equal(base.custody.policy.seller,this.pin.issuerPubkey,'external issuer policy mismatch');
    validateEnrollment(base.reservation,base.custody,base.funding,this.pin.network);
    assert.equal(row.design,base.custody.binding.designIdentity);assert.equal(row.origin,base.custody.binding.origin);assert.equal(row.address,base.reservation.payAddress);assert.equal(row.funding,tx(base.funding.raw).id);
    let s={status:'WAITING_PAYMENT',holds:[],payment:null,prepared:null,receipt:null,inclusion:null,paid:false},head='';
    for(const e of this.db.prepare('SELECT * FROM events WHERE id=? ORDER BY seq').all(id)) {
      assert.equal(e.previous,head);assert.equal(e.digest,sha(head+e.payload),'delivery journal hash');
      const next=JSON.parse(e.payload);assert.equal(canonical(next),e.payload);
      assert.ok(s.holds.every(h=>next.holds.includes(h)),'hold removed');
      if(s.prepared)assert.deepEqual(next.prepared,s.prepared,'prepared bytes changed');
      if(terminal(s.status))assert.ok(terminal(next.status),'ownership history revoked');
      for(const ref of next.payment?.refs||[])assert.equal(this.db.prepare('SELECT id FROM receipts WHERE ref=?').get(ref)?.id,id,'receipt registry mismatch');
      s=next;head=e.digest;
    }
    if(s.prepared)verifyResponse(base.custody,requestFor(base.custody,'delivery-'+id,'Transfer'),s.prepared,base.funding);
    return {...s,...base,binding:base.custody.binding,head,launchReady:false,realSendingEnabled:false};
  }
  commit(id,expected,change,refs=[]) {
    return this.atomic(()=>{
      const current=this.inspect(id);assert.equal(current.head,expected,'concurrent delivery change');
      for(const ref of refs) {
        const prior=this.db.prepare('SELECT id FROM receipts WHERE ref=?').get(ref);
        assert.ok(!prior||prior.id===id,'receipt already bound to another reservation');
        this.db.prepare('INSERT OR IGNORE INTO receipts VALUES(?,?)').run(ref,id);
      }
      const next={};for(const k of ['status','holds','payment','prepared','receipt','inclusion','paid'])next[k]=current[k];
      Object.assign(next,change);const payload=canonical(next);
      const prior={};for(const k of Object.keys(next))prior[k]=current[k];
      if(canonical(prior)!==payload)this.db.prepare('INSERT INTO events(id,previous,digest,payload) VALUES(?,?,?,?)').run(id,expected,sha(expected+payload),payload);
      return this.inspect(id);
    });
  }
  hold(r,reason){return this.commit(r.reservation.id,r.head,{holds:[...new Set([...r.holds,reason])].sort()});}
  async observe(id) {
    let r=this.inspect(id),p;
    try {p=observation(await this.adapters.payment.read(r.reservation.payAddress,this.pin.paymentDepth));}
    catch {return this.hold(r,'PAYMENT_OBSERVATION_UNAVAILABLE');}
    const exact=p.satoshis===r.reservation.priceSats&&p.confirmations>=this.pin.paymentDepth;
    const holds=new Set(r.holds);
    if(p.satoshis>r.reservation.priceSats)holds.add('EXCESS_PAYMENT');
    if(r.paid&&!exact)holds.add('PAYMENT_FINALITY_LOST');
    if(!r.paid&&(this.adapters.now||Date.now)()>=r.reservation.expiresAt)holds.add('EXPIRED_RESERVATION');
    if(r.paid&&r.payment&&r.payment.refs.some(ref=>!p.refs.includes(ref)))holds.add('PAYMENT_RECEIPTS_CHANGED');
    try {r=this.commit(id,r.head,{payment:p,paid:r.paid||exact,holds:[...holds].sort()},p.refs);}
    catch(e){if(!e.message.includes('receipt already bound'))throw e;return this.hold(this.inspect(id),'RECEIPT_CONFLICT');}
    return r;
  }
  // PaymentWatcher callback adapter. Never trusts the watcher's volatile seen cache:
  // independently read full evidence (including zero/depth loss) before each step.
  async onPayment(event){const r=this.inspect(event.id);assert.equal(event.payAddress,r.reservation.payAddress);return this.tick(event.id);}
  async tick(id) {
    this.writable();assert.ok(!this.busy,'delivery busy');
    assert.equal(this.mode,'offline-rehearsal','delivery disabled: release/terms policy unresolved');
    assert.equal(this.pin.network,'offline-fixture','real sending disabled: owner/release gates unresolved');
    this.busy=true;
    try {
      let r=await this.observe(id);
      if(r.holds.length||terminal(r.status))return r;
      if(['PREPARING','ATTEMPTED'].includes(r.status))return this.hold(r,r.status==='PREPARING'?'INTERRUPTED_PREPARATION':'INTERRUPTED_SEND');
      if(!r.paid)return r;
      if(!r.prepared) {
        r=this.commit(id,r.head,{status:'PREPARING'});
        if(this.adapters.hooks?.afterClaim)await this.adapters.hooks.afterClaim();
        try {
          const request=requestFor(r.custody,'delivery-'+id,'Transfer');
          const response=await this.adapters.wallet.request(copy(request));
          verifyResponse(r.custody,request,response,r.funding);
          r=this.commit(id,r.head,{status:'PREPARED',prepared:response});
        }catch(e){this.hold(this.inspect(id),'PREPARATION_FAILED');throw e;}
        if(this.adapters.hooks?.afterPrepared)await this.adapters.hooks.afterPrepared();
      }
      r=await this.observe(id);if(r.holds.length)return r;
      r=this.commit(id,r.head,{status:'ATTEMPTED'});
      if(this.adapters.hooks?.afterAttempt)await this.adapters.hooks.afterAttempt();
      try {
        const receipt=await this.adapters.transport.send(r.prepared.raw);
        assert.deepEqual(receipt,{network:this.pin.network,kind:'LOCAL_VM_ACCEPTED_NOT_CHAIN_INCLUSION',txid:tx(r.prepared.raw).id,rawSha256:sha(Buffer.from(r.prepared.raw,'hex'))});
        return this.commit(id,r.head,{status:'LOCAL_ACCEPTED',receipt});
      }catch{return this.hold(this.inspect(id),'AMBIGUOUS_SEND');}
    }finally{this.busy=false;}
  }
  // Read-only external evidence adapter; this records evidence, NEVER sends/retries.
  // Holds are deliberately not cleared even if inclusion is later found.
  async reconcile(id,reader) {
    this.writable();assert.ok(!this.busy,'delivery busy');this.busy=true;
    try {
      let r=await this.observe(id);assert.ok(r.prepared,'no prepared delivery to reconcile');
      let e;
      try {
        e=await reader.transactionEvidence(tx(r.prepared.raw).id);
        assert.equal(e.raw,r.prepared.raw);assert.equal(e.txid,tx(e.raw).id);
        assert.ok(Number.isSafeInteger(e.confirmations)&&e.confirmations>=this.pin.deliveryDepth);
        assert.match(e.block.hash,/^[0-9a-f]{64}$/);assert.ok(e.block.tx.includes(e.txid));
        assert.ok(Number.isSafeInteger(e.block.height)&&e.block.height>=0);
        assert.equal(e.tip.blocks-e.block.height+1,e.confirmations);
        assert.equal(e.block.confirmations,e.confirmations);
        assert.equal(e.detail.blockhash,e.block.hash);assert.equal(e.detail.confirmations,e.confirmations);
        assert.equal(e.detail.blockheight,e.block.height);
        assert.equal(e.tip.chain,this.pin.network==='mainnet'?'main':this.pin.network==='testnet'?'test':this.pin.network);
        if(this.pin.network==='offline-fixture')assert.equal(e.kind,'OFFLINE_INCLUSION_FIXTURE');
      }catch{return this.hold(r,'DELIVERY_FINALITY_UNAVAILABLE_OR_LOST');}
      return this.commit(id,r.head,{status:this.pin.network==='offline-fixture'?'REHEARSED_CONFIRMED':'CONFIRMED',inclusion:e});
    }finally{this.busy=false;}
  }
  close(){assert.ok(!this.busy,'delivery busy');if(!this.closed){this.db.close();this.closed=true;}}
}
function inspectFile(file,id,config){const d=new Delivery(file,{config,readOnly:true});try{return d.inspect(id);}finally{d.close();}}
module.exports={Delivery,inspectFile,validateEnrollment};
