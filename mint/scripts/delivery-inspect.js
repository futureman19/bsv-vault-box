'use strict';
// Opens SQLite READONLY: no wallet, payment reads, locks removed, retry or edits.
const fs=require('node:fs'),path=require('node:path');
const {inspectFile}=require('../delivery');
try {
  const [file,id,configFile]=process.argv.slice(2);
  if(!file||!id||!configFile)throw Error('usage: node mint/scripts/delivery-inspect.js DATABASE RESERVATION EXTERNAL_CONFIG_JSON');
  const config=JSON.parse(fs.readFileSync(configFile,'utf8'));
  const r=inspectFile(path.resolve(file),id,config);
  console.log(JSON.stringify({schema:1,reservation:r.reservation,binding:r.binding,status:r.status,holds:r.holds,payment:r.payment,prepared:r.prepared,receipt:r.receipt,inclusion:r.inclusion,head:r.head,launchReady:false,realSendingEnabled:false,recovery:'Preserve database and original signed bytes. No automatic refund, retry, release or replacement funding. Inclusion evidence does not clear holds.'},null,2));
}catch(e){console.error(e.message);process.exitCode=1;}
