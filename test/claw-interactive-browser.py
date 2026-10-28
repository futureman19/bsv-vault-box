"""Headed local-only interaction evidence. Run: python test/claw-interactive-browser.py"""
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import pathlib, threading, json, subprocess, statistics, os
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/os.environ.get('BOXSV_EVIDENCE_DIR','evidence/claw-interactive'); OUT.mkdir(parents=True,exist_ok=True)
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(ROOT/'docs')))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/'
report={}
def phase(page,name): page.wait_for_function('(phase)=>window.clawGame.state.phase===phase',arg=name,timeout=12000)
def shot(page,name): page.screenshot(path=str(OUT/(name+'.png')),full_page=True)
def state(page): return page.evaluate('window.clawGame.state')
def arm(page):
 page.locator('#playBtn').click();page.locator('#optDemo').click();phase(page,'armed')
def watch(page):
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 page.add_init_script("window.addEventListener('unhandledrejection',e=>console.error('Unhandled rejection: '+e.reason))")
 return errors
def frames(page):
 return page.evaluate('''()=>new Promise(resolve=>{let times=[],last;function frame(t){if(last)times.push(t-last);last=t;if(times.length<180)requestAnimationFrame(frame);else{times.sort((a,b)=>a-b);resolve({samples:times.length,median_ms:times[90],p95_ms:times[171],fps:1000/(times.reduce((a,b)=>a+b)/times.length)})}}requestAnimationFrame(frame)})''')
try:
 with sync_playwright() as p:
  b=p.chromium.launch(channel='chrome',headless=False,args=['--disable-features=Vulkan'])
  page=b.new_page(viewport={'width':1280,'height':1000});errors=watch(page)
  page.goto(url);page.wait_for_function('!!window.claw3dHandle');page.wait_for_function("claw3dHandle.assets.status !== 'loading'");arm(page);shot(page,'armed')
  latency=page.evaluate('''()=>new Promise(resolve=>{const start=performance.now(),x=clawGame.state.x;document.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));function check(){if(clawGame.state.x!==x){document.dispatchEvent(new KeyboardEvent('keyup',{key:'ArrowRight',bubbles:true}));resolve(performance.now()-start)}else requestAnimationFrame(check)}requestAnimationFrame(check)})''');assert latency<100
  renderer=page.evaluate("(()=>{const gl=document.querySelector('canvas.claw3d-canvas').getContext('webgl2');const e=gl.getExtension('WEBGL_debug_renderer_info');return e?gl.getParameter(e.UNMASKED_RENDERER_WEBGL):'unknown'})()")
  page.keyboard.down('ArrowRight');page.wait_for_timeout(500);page.keyboard.up('ArrowRight');assert state(page)['x']>0;shot(page,'moving')
  page.locator('#joystick').scroll_into_view_if_needed()
  r=page.locator('#joystick').bounding_box();x=r['x']+r['width']/2;y=r['y']+r['height']/2
  before=state(page)['z'];page.mouse.move(x,y);page.mouse.down();page.mouse.move(x-25,y-25);page.wait_for_timeout(500);page.mouse.up();assert state(page)['z']<before
  page.keyboard.down('ArrowRight');page.keyboard.down('ArrowDown');page.wait_for_timeout(2500)
  bounds=state(page);assert bounds['x']==.9 and bounds['z']==.5
  perf=frames(page);cdp=page.context.new_cdp_session(page);cdp.send('Emulation.setCPUThrottlingRate',{'rate':4});proxy=frames(page);cdp.send('Emulation.setCPUThrottlingRate',{'rate':1})
  page.keyboard.up('ArrowRight');page.keyboard.up('ArrowDown')
  page.keyboard.press('Space');phase(page,'descend');page.keyboard.press('Space');assert state(page)['drops']==1
  for name in ['descend','grab','carry','drop','reveal']:
   phase(page,name);page.wait_for_timeout(120 if name!='reveal' else 2600);shot(page,name)
  assert page.locator('#prizeCard').is_visible();page.locator('#againBtn').click();phase(page,'armed');assert state(page)['selected']==-1
  # Real thirty-second wait: no production clock shortcuts.
  page.wait_for_function("window.clawGame.state.reason==='timeout' && window.clawGame.state.phase==='descend'",timeout=33000)
  timeout=state(page);shot(page,'timeout');phase(page,'reveal')
  report['desktop']={'errors':errors,'input_response_ms':latency,'renderer':renderer,'bounds':bounds,'timeout':timeout,'input_frames':perf,'cpu4x_proxy':proxy,'strict_60fps_pass':perf['fps']>=60};assert not errors
  page.locator('#againBtn').click();phase(page,'armed')
  page.evaluate("claw3dHandle.dispose();window.claw3dHandle=Claw3D.mount(document.querySelector('.machine-wrap'))")
  assert page.evaluate('claw3dHandle.state===clawMotionHandle.state')
  page.evaluate("document.querySelector('canvas.claw3d-canvas').getContext('webgl2').getExtension('WEBGL_lose_context').loseContext()")
  page.wait_for_timeout(200);assert page.locator('#cabinet').is_visible()
  page.keyboard.press('Space');phase(page,'reveal');assert not errors
  report['desktop']['remount_and_context_loss']='passed'
  page.close()
  # Wallet API is synthetic; verifies unchanged call contract, not extension auth.
  page=b.new_page(viewport={'width':390,'height':844},reduced_motion='reduce');errors=watch(page)
  page.add_init_script("window.walletCalls=[];window.CWI={waitForAuthentication:async o=>walletCalls.push(['auth',o]),getPublicKey:async o=>{walletCalls.push(['key',o]);return {publicKey:'synthetic-test-identity-key'}}}")
  page.goto(url);page.wait_for_function('!!window.claw3dHandle');page.locator('#playBtn').click();page.locator('#optCancel').click();assert state(page)['phase']=='idle'
  page.locator('#playBtn').click();page.locator('#optYours').click();phase(page,'armed');assert state(page)['remaining']>=29
  calls=page.evaluate('walletCalls');assert calls==[['auth',{}],['key',{'identityKey':True}]]
  page.locator('#joystick').scroll_into_view_if_needed()
  r=page.locator('#joystick').bounding_box();x=r['x']+r['width']/2;y=r['y']+r['height']/2
  touch=page.context.new_cdp_session(page)
  touch.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
  touch.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+26,'y':y+20}]})
  page.wait_for_timeout(350);touch.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]});assert state(page)['x']>0 and state(page)['z']>0
  page.locator('#dropBtn').click();phase(page,'reveal');page.wait_for_timeout(700);shot(page,'mobile-wallet-reduced');assert 'synthetic' in page.locator('#prizeKey').inner_text();assert not errors
  report['wallet_reduced']={'mock_calls':calls,'errors':errors};page.close();b.close()
  b=p.chromium.launch(channel='chrome',headless=False,args=['--disable-webgl'])
  page=b.new_page(viewport={'width':390,'height':844},reduced_motion='reduce');errors=watch(page)
  page.goto(url);page.wait_for_timeout(1000);assert page.locator('.claw3d-canvas').count()==0;arm(page)
  page.keyboard.down('ArrowLeft');page.wait_for_timeout(400);page.keyboard.up('ArrowLeft');assert state(page)['x']<0
  page.locator('.machine-wrap').scroll_into_view_if_needed()
  r=page.locator('.machine-wrap').bounding_box();x=r['x']+r['width']/2;y=r['y']+r['height']/2
  page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+30,y+30);page.wait_for_timeout(500);page.mouse.up();assert state(page)['z']>0
  shot(page,'fallback-moving');page.keyboard.press('Enter');phase(page,'grab');shot(page,'fallback-grab');phase(page,'carry');shot(page,'fallback-carry')
  attachment=page.evaluate("(()=>{const a=document.querySelector('#claw').getBoundingClientRect(),b=document.querySelectorAll('.loot')[clawGame.state.selected].getBoundingClientRect();return {dx:Math.abs((a.x+a.width/2)-(b.x+b.width/2)),dy:b.y-a.y}})()")
  assert attachment['dx']<3 and 30<=attachment['dy']<=38,attachment
  phase(page,'reveal');page.wait_for_timeout(700);shot(page,'fallback-reveal')
  page.locator('#againBtn').click();phase(page,'armed');assert state(page)['remaining']>=29;assert not errors
  report['fallback']={'errors':errors,'reset':state(page)};b.close()
 # Preserve the original core payload guard; budget the newly requested optional
 # authored assets separately rather than pretending they existed at baseline.
 files=['docs/index.html','docs/claw.js','docs/claw3d.js','docs/vendor/three/three.module.min.js','docs/vendor/three/RoomEnvironment.js']
 baseline=sum(len(subprocess.check_output(['git','show',f'e6727f0:{f}'],cwd=ROOT)) for f in files)
 current=sum((ROOT/f).stat().st_size for f in files)+(ROOT/'docs/claw-motion.js').stat().st_size+(ROOT/'docs/arcade.css').stat().st_size
 report['payload']={'baseline_bytes':baseline,'current_bytes':current,'delta_percent':100*(current-baseline)/baseline};assert abs(report['payload']['delta_percent'])<=5
 optional=[ROOT/'docs/vault-assets.js',*(ROOT/'docs/assets/vault-kit').glob('*.glb'),*(ROOT/'docs/vendor/three/loaders').glob('*.js'),*(ROOT/'docs/vendor/three/utils').glob('*.js')]
 report['payload']['optional_authored_bytes']=sum(f.stat().st_size for f in optional)
 assert report['payload']['optional_authored_bytes']<=1000000
finally:
 server.shutdown();(OUT/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
