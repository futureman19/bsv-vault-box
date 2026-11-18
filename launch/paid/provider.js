'use strict';
// Explicit user gesture only. No module-load discovery, authentication or signing.
// @1sat/connect 0.1.2 ConnectWalletResult is {wallet,provider,identityKey,disconnect}.
// 'brc100' identifies a protocol, NOT proof the installed product is Yours.
function createProvider({connectWallet,enabled=false}={}){
 let result=null,epoch=0,busy=false;
 const disconnect=()=>{epoch++;const old=result;result=null;if(typeof old?.disconnect==='function')old.disconnect();};
 return {
  disconnect,
  async getWallet(){
   if(!enabled)throw Error('Owner wallet connection is disabled');
   if(busy||result)throw Error('Disconnect before reconnecting');
   busy=true;const generation=++epoch;
   try{
    const connect=connectWallet||(await import('@1sat/connect')).connectWallet;
    // No popup host defaults or configured provider race. BRC100 auto transport
    // may discover an extension or localhost wallet; owner must select/verify it.
    const found=await connect({autoDetect:true,providers:[]});
    if(generation!==epoch){found?.disconnect();throw Error('Connection cancelled');}
    if(!found)throw Error('No compatible BRC100 wallet connected');
    result=found;
    if(found.provider!=='brc100'||typeof found.disconnect!=='function'||!/^0[23][a-f0-9]{64}$/.test(found.identityKey))throw Error('Unexpected provider response');
    for(const method of ['waitForAuthentication','getNetwork','getPublicKey','createSignature'])if(typeof found.wallet?.[method]!=='function')throw Error('WalletInterface method unavailable: '+method);
    const {publicKey}=await found.wallet.getPublicKey({identityKey:true});
    if(generation!==epoch||publicKey!==found.identityKey)throw Error('Provider identity changed');
    return found.wallet;
   }catch(error){disconnect();throw error;}finally{busy=false;}
  }
 };
}
module.exports={createProvider};
