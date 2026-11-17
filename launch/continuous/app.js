'use strict';
const $=id=>document.getElementById(id);
let state,busy=false;
const actions=['Pack','Seal','Transfer','Open','Withdraw'];
const copy={AVAILABLE:['Your Iceland candidate','Reserve this one fixed design for the public fixture buyer. No random draw, payment or sale.'],RESERVED:['Reserved for one buyer','The reservation, signed buyer authorization and issued origin are now bound. Pack the inner collectible into the outer custody Box.'],PACKED:['Packed, not yet sealed','The original ordinal is held with its companion control output. Seal this package next.'],SEALED:['Sealed for transfer','The seal is intact. Transfer both custody outputs to the fixture buyer without changing the original collectible.'],TRANSFERRED:['Buyer now controls the Box','Local VM acceptance, not chain confirmation. The former owner cannot authorize the current pair. Open to irreversibly end this seal.'],OPENED:['Opened · still inside','The seal is broken. The original collectible remains in custody until the buyer signs withdrawal.'],WITHDRAWN:['The original asset, withdrawn','Both outputs now pay the fixture buyer. Output zero retains the original ordinal through the full signed ancestry. This seal cannot be reused.']};
function next(){return state?.stage==='AVAILABLE'?'Reserve':actions[state?.history.length];}
function render(s){
 state=s;document.body.dataset.stage=s.stage;
 const [title,description]=copy[s.stage];$('stage').textContent=title;$('description').textContent=description;
 const step=s.stage==='AVAILABLE'?0:s.history.length+1;
 document.querySelectorAll('#progress li').forEach((li,i)=>{li.className=i<step?'done':i===step?'current':'';if(i===step)li.setAttribute('aria-current','step');else li.removeAttribute('aria-current');});
 const held=s.holds.length||s.pending?.attempted;
 $('advance').textContent=held?'Reconciliation hold':next()?(next()==='Reserve'?'Reserve Iceland · simulation':next()+' · fixture signature'):'Journey complete';
 $('advance').disabled=busy||held||!next();$('mode').disabled=busy||held||!next();
 $('binding-summary').textContent=s.binding.designIdentity+' · '+s.history.length+' of 5 custody transitions VM-verified';
 for(const [id,value] of Object.entries({origin:s.binding.origin,digest:s.binding.metadataSha256,buyer:s.binding.buyerPubkey,manifest:s.binding.manifestSha256,head:s.head}))$(id).textContent=value;
 $('transactions').replaceChildren();
 for(const h of s.history){const box=document.createElement('div');box.className='transaction';const title=document.createElement('strong');title.textContent=h.action+' · Script PASS';const id=document.createElement('p');id.textContent=h.receipt.txid;box.append(title,id);$('transactions').append(box);}
 if(held){$('error').hidden=false;$('error').textContent='Reconciliation hold: '+(s.holds.join(', ')||'interrupted send')+'. Exact signed bytes and funding are preserved. No replacement allocation or automatic send.';}
}
async function load(){const r=await fetch('/api/state');if(!r.ok)throw Error('Saved state unavailable');render(await r.json());}
$('advance').addEventListener('click',async()=>{
 if(busy||!state)return;busy=true;$('advance').disabled=true;$('mode').disabled=true;$('error').hidden=true;$('activity').textContent='Signing public fixture bytes and replaying Script…';
 const action=next(),key=action.toLowerCase()+'-fixture-1',mode=$('mode').value;
 try{
  const r=await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json','X-BoxSV-Demo':'1'},body:JSON.stringify({key,action,mode})});
  const result=await r.json();if(!r.ok)throw Error(result.error);
  render(result);$('activity').textContent=action==='Reserve'?'Signed reservation saved.':'Signed transaction saved and VM-verified. No chain broadcast.';
 }catch(e){$('error').textContent=e.message;$('error').hidden=false;$('activity').textContent='No success inferred. Reloading durable state…';try{await load();}catch{ $('activity').textContent='State unavailable. Stop and restart the local server; do not create a replacement journey.';state=null; }}
 finally{busy=false;$('mode').value='ok';if(state)render(state);}
});
load().catch(e=>{$('error').hidden=false;$('error').textContent=e.message;});
