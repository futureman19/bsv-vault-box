'use strict';
// Synthetic WoC-shaped chain; no signatures or mined transactions are claimed.
const {buildManifest,manifestRoot}=require('../manifest');
const {drawPack}=require('../draw');
const checker=require('../docs/vaultcheck');
const ids={sealed:'11'.repeat(32),open:'22'.repeat(32),transfer:'33'.repeat(32),manifest:'44'.repeat(32),mint:'55'.repeat(32),block:'66'.repeat(32),seed:'77'.repeat(32),box:'88'.repeat(32)};
const manifest=buildManifest({name:'Fixture',pack_size:3,allow_pack_duplicates:false,per_slot_odds_published:true,designs:[{id:0,ref:'a',weight:5},{id:1,ref:'b',weight:3},{id:2,ref:'c',weight:1}],slots:{2:{table:[{id:2,weight:1}]}}});
const root=manifestRoot(manifest),owner='02'+'99'.repeat(32);
function script(state,commitment=root){
 const constants='0176018801a901ac20'+'97dfd76851bf465e8f715593b217714858bbe9570ff3bd5e33840a34e20ff026'+'21'+'02ba79df5f8ae7604a9830f03c7933028186aede0675a16f025dc4f8be8eec0382'+'20'+'1008ce7480da41702918d1ec8e6849ba32b4d65b1e40dc669c31a1e6306b266c';
 return constants+'00'.repeat(10)+'20'+ids.box+'20'+commitment+'21'+owner+checker.ARTIFACT_CODETAIL+'6a0001'+(state?'01':'00')+'21'+owner+'2500000000';
}
function push(s){const b=Buffer.from(s);if(b.length<76)return Buffer.concat([Buffer.from([b.length]),b]).toString('hex');const h=Buffer.alloc(3);h[0]=77;h.writeUInt16LE(b.length,1);return Buffer.concat([h,b]).toString('hex');}
function tagged(tag,obj){return {value:0,scriptPubKey:{hex:'006a'+push(tag)+push(JSON.stringify(obj))}};}
const output=state=>({value:0.00000001,scriptPubKey:{hex:script(state)}});
function chain(){return {
 ['/tx/'+ids.sealed]:{txid:ids.sealed,confirmations:10,vin:[],vout:[output(0)]},
 ['/tx/'+ids.open]:{txid:ids.open,confirmations:8,blockhash:ids.block,blockheight:100,vin:[{txid:ids.sealed,vout:0}],vout:[output(1)]},
 ['/tx/'+ids.transfer]:{txid:ids.transfer,confirmations:3,blockheight:105,vin:[{txid:ids.open,vout:0}],vout:[output(1)]},
 ['/tx/'+ids.manifest]:{txid:ids.manifest,vout:[tagged('VAULT3-MANIFEST',manifest)]},
 ['/tx/'+ids.mint]:{txid:ids.mint,vin:[{txid:ids.open,vout:1}],vout:[tagged('VAULT3-MINT',{manifest_root:root,box_id:ids.box,designs:drawPack(manifest,ids.box,ids.seed).designs})]},
 '/block/height/101':{hash:ids.seed,height:101,previousblockhash:ids.block},
};}
module.exports={ids,manifest,root,script,tagged,chain};
