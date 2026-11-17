"""Actual served claw; mocked identity methods only, no extension/keys/network."""
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import threading,json
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT/'docs')))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
results=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='msedge',headless=True)
  for mode in ['success','reject','empty','absent']:
   ctx=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce')
   ctx.route('**/*',lambda r:r.continue_() if r.request.url.startswith(base) and r.request.method=='GET' else r.abort())
   ctx.add_init_script("""window.calls=[];window.open=(...a)=>{calls.push(['open',...a]);return null};"""+('' if mode=='absent' else """window.CWI=new Proxy({waitForAuthentication:async()=>{calls.push(['auth']);REJECT},getPublicKey:async a=>{calls.push(['identity',a]);return ID}}, {get(t,k){if(k in t)return t[k];return ()=>{calls.push(['FORBIDDEN',k]);throw Error('Signing/payment forbidden')}}});""".replace('REJECT',"throw Error('fixture denied')" if mode=='reject' else '').replace('ID','{}' if mode=='empty' else '{publicKey:"02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5"}')))
   page=ctx.new_page();page.goto(base+'/');page.wait_for_function("clawPresentation.state!=='loading'")
   page.locator('#playBtn').click();page.locator('#optYours').click()
   if mode=='success':
    page.wait_for_function("clawGame.state.phase==='armed'")
    expect(page.locator('#walletChip')).to_contain_text('connected:')
    assert page.evaluate('calls')==[['auth'],['identity',{'identityKey':True}]]
   else:
    expect(page.locator('#walletModal')).to_be_visible()
    if mode!='absent': expect(page.locator('#werr')).to_contain_text('fixture denied' if mode=='reject' else 'no identity key')
    else: assert page.evaluate('calls')[0][1]=='https://yours.org'
    page.locator('#optDemo').click();page.wait_for_function("clawGame.state.phase==='armed'")
    expect(page.locator('#walletChip')).to_contain_text('no wallet connected')
   calls=page.evaluate('calls');assert not any(x[0]=='FORBIDDEN' for x in calls)
   results.append({'case':mode,'pass':True,'calls':calls})
   page.screenshot(path=str(OUT/('wallet-'+mode+'.png')))
   ctx.close()
  browser.close()
 (OUT/'wallet.json').write_text(json.dumps({'status':'PASS','cases':results,'boundary':'Mock identity connect only. No transaction signing, paid mint, extension compatibility or custody integration.'},indent=2)+'\n')
finally:server.shutdown();server.server_close()
print(json.dumps(results))
