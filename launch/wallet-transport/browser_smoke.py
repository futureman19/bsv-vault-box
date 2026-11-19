"""Isolated browser bundle smoke; replays public-fixture provider signatures only."""
import json, subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
data=json.loads(subprocess.check_output(['node',str(Path(__file__).with_name('harness.js'))],cwd=ROOT))
with sync_playwright() as p:
    browser=p.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page()
    page.route('**/*',lambda route:route.abort())
    page.set_content('<title>Wallet transport isolated fixture smoke</title>')
    page.add_script_tag(path=str(Path(__file__).with_name('browser')/'adapter.js'))
    result=page.evaluate('''async ({request,response}) => {
      const {WalletTransport,requestHash,verifyResponse}=window.BoxSVWalletTransport;
      let calls=0;
      const fromHex=s=>s.match(/../g).map(x=>parseInt(x,16));
      const provider={
        waitForAuthentication:async()=>({authenticated:true}),
        isAuthenticated:async()=>({authenticated:true}),
        getNetwork:async()=>({network:request.network}),
        getPublicKey:async a=>({publicKey:a.identityKey?request.identityKey:request.signingKey}),
        createSignature:async a=>{calls++;return {signature:fromHex(a.hashToDirectlySign?response.transactionSignature.slice(0,-2):response.signature)};}
      };
      const policy={network:request.network,identityKey:request.identityKey,signingKey:request.signingKey,allowSigning:true};
      const adapter=new WalletTransport(provider,policy);
      const actual=await adapter.request(request,{expectedRequestHash:requestHash(request)});
      const verified=verifyResponse(request,actual,policy);
      let sendDisabled=false;try{adapter.send('00')}catch(e){sendDisabled=e.message==='SEND_DISABLED'}
      if(!verified||calls!==2||!sendDisabled)throw Error('browser smoke failed');
      return {verified,calls,sendDisabled,label:'ISOLATED_BROWSER_PUBLIC_FIXTURE_SIGNATURE_REPLAY_NOT_EXTENSION'};
    }''',data)
    print(json.dumps(result,indent=2))
    browser.close()
