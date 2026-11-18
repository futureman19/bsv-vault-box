'use strict';
// Durable first-writer allocation. Never release/reassign, including failed journal
// commits: orphan allocations are deliberately held for operator reconciliation.
const {DatabaseSync}=require('node:sqlite');
const {randomUUID}=require('node:crypto');
const {assert,canonical,fs,path}=require('../continuous/common');
class ReceiptRegistry {
 constructor(file,{fixtureOnly=false}={}) {
  this.fixtureOnly=fixtureOnly;this.owned=typeof file==='string';
  if(this.owned){assert.ok(file&&file!==':memory:'&&!file.startsWith('file:'),'durable registry file required');fs.mkdirSync(path.dirname(path.resolve(file)),{recursive:true});this.db=new DatabaseSync(file);}
  else {assert.ok(fixtureOnly&&file instanceof DatabaseSync,'borrowed DB requires explicit fixture scope');this.db=file;}
  this.db.exec(`PRAGMA synchronous=FULL; PRAGMA busy_timeout=3000;
   CREATE TABLE IF NOT EXISTS payment_invoices(id TEXT PRIMARY KEY, network TEXT NOT NULL, address TEXT NOT NULL, owner TEXT NOT NULL, invoice TEXT NOT NULL, UNIQUE(network,address));
   CREATE TABLE IF NOT EXISTS payment_receipts(network TEXT NOT NULL, outpoint TEXT NOT NULL, invoice_id TEXT NOT NULL, owner TEXT NOT NULL, PRIMARY KEY(network,outpoint));
   CREATE TABLE IF NOT EXISTS payment_registry_identity(singleton INTEGER PRIMARY KEY CHECK(singleton=1), id TEXT NOT NULL);`);
  this.db.prepare('INSERT OR IGNORE INTO payment_registry_identity VALUES(1,?)').run(randomUUID());
  this.id=this.db.prepare('SELECT id FROM payment_registry_identity WHERE singleton=1').get().id;
 }
 transaction(fn){this.db.exec('BEGIN IMMEDIATE');try{const result=fn();this.db.exec('COMMIT');return result;}catch(error){this.db.exec('ROLLBACK');throw error;}}
 check(invoice,owner){
  assert.ok(typeof owner==='string'&&owner.length,'registry journal owner required');
  if(this.fixtureOnly)assert.equal(invoice.network,'offline-fixture','fixture registry cannot allocate live invoices');
  const old=this.db.prepare('SELECT * FROM payment_invoices WHERE id=?').get(invoice.id);
  if(old){assert.equal(old.invoice,canonical(invoice),'immutable registry invoice');assert.equal(old.owner,owner,'invoice journal owner mismatch');}
  return old;
 }
 allocate(invoice,owner){return this.transaction(()=>{if(!this.check(invoice,owner))this.db.prepare('INSERT INTO payment_invoices VALUES(?,?,?,?,?)').run(invoice.id,invoice.network,invoice.address,owner,canonical(invoice));});}
 claim(invoice,owner,receipts){return this.transaction(()=>{
  assert.ok(this.check(invoice,owner),'invoice allocation missing');
  for(const r of receipts){assert.match(r.outpoint,/^[0-9a-f]{64}:(0|[1-9][0-9]*)$/);const old=this.db.prepare('SELECT * FROM payment_receipts WHERE network=? AND outpoint=?').get(invoice.network,r.outpoint);
   if(old){assert.equal(old.invoice_id,invoice.id,'receipt attribution mismatch');assert.equal(old.owner,owner,'receipt attribution owner mismatch');}
   else this.db.prepare('INSERT INTO payment_receipts VALUES(?,?,?,?)').run(invoice.network,r.outpoint,invoice.id,owner);
  }
 });}
 close(){if(this.owned)this.db.close();}
}
function journalOwner(journal){
 const db=journal.db;db.exec('CREATE TABLE IF NOT EXISTS payment_registry_owner(singleton INTEGER PRIMARY KEY CHECK(singleton=1), owner TEXT NOT NULL)');
 db.prepare('INSERT OR IGNORE INTO payment_registry_owner VALUES(1,?)').run(randomUUID());
 return db.prepare('SELECT owner FROM payment_registry_owner WHERE singleton=1').get().owner;
}
module.exports={ReceiptRegistry,journalOwner};
