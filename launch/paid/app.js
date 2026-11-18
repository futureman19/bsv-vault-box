'use strict';
const $=id=>document.getElementById(id);let state,busy=false;
const nextFor=s=>({AVAILABLE:'Reserve',RESERVED:'Pack',PACKED:'Seal',SEALED:'Transfer',TRANSFERRED:'Open',OPENED:'Withdraw'})[s.stage];
function render(s){state=s;$('stage').textContent=s.stage;$('payment').textContent=s.payment.qualified?'Exact fixture receipt confirmed':'Waiting for exact confirmed fixture receipt';$('holds').textContent=s.holds.length?'Reconciliation hold: '+s.holds.join(', '):'No reconciliation holds';$('next').textContent=nextFor(s)||'Complete — withdrawn';$('next').disabled=busy||!nextFor(s)||s.holds.length>0||(nextFor(s)==='Transfer'&&!s.payment.qualified);$('observe').disabled=busy;$('evidence').textContent=JSON.stringify({binding:s.binding,invoice:s.payment.invoice,receiptCount:s.payment.acceptedReceipts.length,events:s.events,history:s.history.map(h=>({action:h.action,txid:h.receipt.txid})),holds:s.holds,provenance:s.provenance,chainInclusion:s.chainInclusion},null,2);}
async function refresh(){const r=await fetch('/api/state');if(!r.ok)throw Error('State unavailable');render(await r.json());}
async function post(data){if(busy)return;busy=true;if(state)render(state);$('message').textContent='Working…';try{const r=await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json','X-BoxSV-Demo':'1'},body:JSON.stringify(data)});const s=await r.json();if(!r.ok)throw Error(s.error||'Operation rejected');render(s);$('message').textContent='Saved and verified locally.';}catch(e){$('message').textContent=e.message;}finally{busy=false;await refresh();}}
$('next').onclick=()=>post({action:nextFor(state),key:'browser-'+nextFor(state),mode:$('mode').value});
$('observe').onclick=()=>post({action:'Observe',scenario:$('scenario').value});
function detect(){const available=typeof window.CWI==='object'&&window.CWI!==null;$('extension').textContent=available?'CWI interface present. No authentication or signing requested.':'No CWI interface observed on this page. Real Yours signing remains unverified.';}
detect();
async function init(){
 const config=await (await fetch('/api/config')).json();
 if(config.browserWallet){
  const load=src=>new Promise((resolve,reject)=>{const script=document.createElement('script');script.src=src;script.onload=resolve;script.onerror=()=>reject(Error('Wallet bundle load failed'));document.head.append(script);});
  await load('/browser-wallet.bundle.js');await load('/browser-wallet-fixture.bundle.js');
  const fixture=BoxSVBrowserWalletFixture.createFixtureProvider();
  const root=document.createElement('section');root.id='wallet-controls';$('next').before(root);
  const ui=BoxSVBrowserWallet.mount({root,getWallet:()=>fixture.wallet,network:'test',label:'public fixture buyer'});
  $('mode').onchange=()=>{fixture.control.mode=({'wrong-buyer':'account-switch',disconnect:'reject',ambiguous:'ok'})[$('mode').value]||$('mode').value;};
  window.paidFixture={fixture,client:ui.client}; // explicit local fixture harness, never a real wallet
  $('extension').textContent='Buyer signatures happen in this browser using a PUBLIC test key. Connect, then approve each pending signature separately. No extension is contacted.';
 }
 await refresh();
}
init().catch(e=>{$('message').textContent=e.message;});
