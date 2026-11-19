'use strict';
// Public scalar 2 ONLY. Never fund these addresses. SDK implements real BRC-42/100.
const {ProtoWallet, PrivateKey} = require('@bsv/sdk');
const {bsv} = require('../../vault/node_modules/scryptlib');
const crypto = require('node:crypto');
const KEY = {protocolID:[1,'boxsv custody'],keyID:'testnet:owner:v1',counterparty:'self'};
async function fixture() {
  const proto = new ProtoWallet(new PrivateKey(2));
  const identityKey = (await proto.getPublicKey({identityKey:true})).publicKey;
  const signingKey = (await proto.getPublicKey({...KEY, forSelf:true})).publicKey;
  const calls=[];
  const provider = {
    async waitForAuthentication(args) {calls.push(['waitForAuthentication',args]);return {authenticated:true};},
    async isAuthenticated(args) {calls.push(['isAuthenticated',args]);return {authenticated:true};},
    async getNetwork(args) {calls.push(['getNetwork',args]);return {network:'testnet'};},
    async getPublicKey(args) {calls.push(['getPublicKey',structuredClone(args)]);return proto.getPublicKey(args);},
    async createSignature(args) {calls.push(['createSignature',structuredClone(args)]);return proto.createSignature(args);}
  };
  const script = bsv.Script.buildPublicKeyHashOut(bsv.PublicKey.fromString(signingKey).toAddress(bsv.Networks.testnet));
  const parent = new bsv.Transaction().addInput(new bsv.Transaction.Input({prevTxId:crypto.createHash('sha256').update('boxsv public fixture synthetic root').digest('hex'),outputIndex:0,script:'',output:new bsv.Transaction.Output({script:bsv.Script.empty(),satoshis:1000})})).addOutput(new bsv.Transaction.Output({script,satoshis:1000}));
  const transaction = new bsv.Transaction().addInput(new bsv.Transaction.Input({prevTxId:parent.id,outputIndex:0,script:'',output:parent.outputs[0]})).addOutput(new bsv.Transaction.Output({script,satoshis:900}));
  const request = {version:1,id:'fixture-request-0001',expiresAt:Date.now()+60000,network:'testnet',identityKey,signingKey,action:'Withdraw',binding:{manifestSha256:'11'.repeat(32),designId:'iceland',metadataSha256:'22'.repeat(32),origin:parent.id+'_0',buyerPubkey:signingKey},transaction:{raw:transaction.uncheckedSerialize(),parents:[parent.uncheckedSerialize()],inputIndex:0},intent:{outputs:[{script:script.toHex(),satoshis:900}],maxFee:100}};
  return {proto,provider,calls,parent,transaction,request,policy:{network:'testnet',identityKey,signingKey,allowSigning:true}};
}
module.exports={fixture,KEY,bsv};
