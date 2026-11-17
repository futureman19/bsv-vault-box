"""Local authored-claw acceptance; no wallet calls or external requests."""
from playwright.sync_api import sync_playwright
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import pathlib, threading, json, os, time
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/os.environ.get('BOXSV_EVIDENCE_DIR','evidence/launch-03/acceptance')
OUT.mkdir(parents=True,exist_ok=True)
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(ROOT/'docs')))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/'
report={'checks':[], 'scope':'Headed Chrome, desktop and emulated mobile; no physical phone proof.'}
def check(name,fn):
 if os.environ.get('BOXSV_CHECK_FILTER') and os.environ['BOXSV_CHECK_FILTER'] not in name:return
 try:
  data=fn();report['checks'].append({'name':name,'pass':True,'data':data})
 except Exception as e: report['checks'].append({'name':name,'pass':False,'error':str(e)})
 print(report['checks'][-1],flush=True)
def ready(page): page.wait_for_function("window.clawPresentation && clawPresentation.state!=='loading'")
def phase(page,name): page.wait_for_function('(s)=>clawGame.state.phase===s',arg=name,timeout=15000)
def arm(page):
 page.locator('#playBtn').click()
 if page.locator('#walletModal').is_visible():page.locator('#optDemo').click()
 phase(page,'armed')
def snap(page,name):page.screenshot(path=str(OUT/(name+'.png')),full_page=True)
def assert_true(v):assert v
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='chrome',headless=False)
  context=browser.new_context(viewport={'width':1280,'height':900})
  context.route('**/*',lambda r:r.continue_() if r.request.url.startswith(url) else r.abort())
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(url);ready(page)
  check('authored ready',lambda:assert_true(page.evaluate("clawPresentation.state==='ready' && claw3dHandle.assets.parts===11 && !claw3dHandle.visualSnapshot().primitiveCabinetVisible")))
  arm(page);snap(page,'desktop-armed')
  def foreign_keys():
   page.locator('nav a[href="#box-demo"]').first.focus()
   page.keyboard.press('Space');page.wait_for_timeout(100)
   assert page.evaluate("clawGame.state.phase==='armed'")
  check('navigation Space does not drop',foreign_keys)
  # New document makes every section independent of previous failure.
  page.reload();ready(page);arm(page)
  page.locator('#dropBtn').click();phase(page,'reveal');page.wait_for_timeout(2700)
  snap(page,'desktop-reveal')
  def return_play():
   page.locator('#tryBoxBtn').click()
   page.locator('a[href="#claw-demo"]').last.click()
   assert page.locator('#playBtn').is_visible()
   arm(page)
  check('Try Box then return can play',return_play)
  check('no uncaught errors',lambda:assert_true(not errors))
  def input_and_races():
   page.reload();ready(page);arm(page)
   page.keyboard.down('ArrowRight');page.wait_for_timeout(350);page.keyboard.up('ArrowRight')
   assert page.evaluate('clawGame.state.x>0')
   page.locator('#box-demo button').first.focus();page.keyboard.press('Space')
   assert page.evaluate("clawGame.state.phase==='armed'")
   page.locator('#joystick').focus();page.keyboard.press('Space');page.keyboard.press('Space')
   assert page.evaluate('clawGame.state.drops===1')
   for name in ['grab','carry','reveal']:
    phase(page,name);snap(page,'desktop-'+name)
   # Force the hidden action during the pending reveal to stress stale callbacks.
   page.evaluate("document.getElementById('againBtn').click()")
   phase(page,'armed');page.wait_for_timeout(2600)
   assert page.evaluate("!document.getElementById('prizeCard').classList.contains('on') && clawGame.state.drops===0")
   page.wait_for_function("clawGame.state.reason==='timeout'",timeout=32000)
   phase(page,'reveal')
   return {'timeout':'real 30-second deadline','duplicate_drop':'one','interrupted_reveal':'no stale card'}
  check('input isolation duplicate drop reset and deadline',input_and_races)
  def perf():
   page.reload();ready(page)
   data=page.evaluate('''()=>new Promise(resolve=>{let a=[],last;function f(t){if(last)a.push(t-last);last=t;if(a.length<120)requestAnimationFrame(f);else {a.sort((x,y)=>x-y);resolve({samples:a.length,median_ms:a[60],p95_ms:a[114],fps:1000/(a.reduce((x,y)=>x+y)/a.length),scene:claw3dHandle.visualSnapshot()})}}requestAnimationFrame(f)})''')
   return data
  check('desktop frame measurement (not phone certification)',perf)
  def mobile():
   page.set_viewport_size({'width':390,'height':844});page.emulate_media(reduced_motion='no-preference');page.reload();ready(page)
   assert page.evaluate("clawPresentation.state==='ready'")
   page.emulate_media(reduced_motion='reduce');arm(page)
   page.locator('#joystick').scroll_into_view_if_needed();r=page.locator('#joystick').bounding_box();x=r['x']+r['width']/2;y=r['y']+r['height']/2
   cdp=context.new_cdp_session(page)
   cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]})
   cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+25,'y':y+20}]})
   page.wait_for_timeout(400);cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
   assert page.evaluate('clawGame.state.x>0 && clawGame.state.z>0')
   snap(page,'mobile-armed');page.set_viewport_size({'width':844,'height':390});page.wait_for_timeout(300)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   snap(page,'mobile-landscape');page.set_viewport_size({'width':390,'height':844})
   page.locator('#dropBtn').click();phase(page,'reveal');page.wait_for_timeout(700);snap(page,'mobile-reveal')
   assert page.locator('#prizeCard').is_visible()
   page.locator('#againBtn').click();phase(page,'armed')
   page.evaluate("document.querySelector('.claw3d-canvas').getContext('webgl2').getExtension('WEBGL_lose_context').loseContext()")
   page.wait_for_timeout(300);assert page.locator('#cabinet').is_visible()
   page.locator('#dropBtn').click();phase(page,'reveal')
   return {'touch':'native CDP','orientation':'viewport emulated','reduced_motion':True,'context_loss':'playable CSS'}
  check('mobile touch orientation reduced motion and context loss',mobile)
  page.close()
  def loading_case(kind):
   c=browser.new_context(viewport={'width':390,'height':844})
   held=[]
   def route(r):
    u=r.request.url
    if not u.startswith(url):r.abort();return
    target=u.endswith('claw3d.js') if 'module' in kind else u.endswith('.glb')
    if target:
     if 'failure' in kind:r.abort()
     else:held.append(r)
    else:r.continue_()
   c.route('**/*',route)
   q=c.new_page();q.on('pageerror',lambda e:errors.append(str(e)));q.goto(url,wait_until='domcontentloaded');q.wait_for_timeout(1000)
   if 'failure' not in kind:
    assert q.locator('#playBtn').is_disabled()
    assert not q.locator('#cabinet').is_visible()
    snap(q,kind+'-loading')
    if kind=='GLB-delayed':
     for r in held:r.continue_()
     held.clear();ready(q);assert q.evaluate("clawPresentation.state==='ready'")
    else:
     ready(q);assert q.evaluate("clawPresentation.state==='fallback'")
     for r in held:r.continue_()
     held.clear();q.wait_for_timeout(1500)
     assert q.evaluate("clawPresentation.state==='fallback'")
     assert not q.evaluate("!!window.claw3dHandle && claw3dHandle.assets.status==='ready'")
   else:ready(q);assert q.evaluate("clawPresentation.state==='fallback'")
   q.emulate_media(reduced_motion='reduce');arm(q);q.locator('#dropBtn').click();phase(q,'reveal');q.wait_for_timeout(600);snap(q,kind+'-playable')
   assert q.locator('#prizeCard').is_visible();c.close()
  for kind in ['GLB-delayed','GLB-timeout-late','module-timeout-late','GLB-failure','module-failure']:
   check(kind,lambda kind=kind:loading_case(kind))
  browser.close()
  def no_webgl():
   b=p.chromium.launch(channel='chrome',headless=False,args=['--disable-webgl'])
   q=b.new_page(viewport={'width':390,'height':844});q.on('pageerror',lambda e:errors.append(str(e)));q.goto(url);ready(q)
   assert q.locator('.claw3d-canvas').count()==0
   assert q.evaluate("clawPresentation.state==='fallback' && !matchMedia('(prefers-reduced-motion: reduce)').matches")
   q.emulate_media(reduced_motion='reduce')
   arm(q);q.keyboard.press('Space');phase(q,'reveal');q.wait_for_timeout(600);snap(q,'no-webgl');assert q.locator('#prizeCard').is_visible();b.close()
  check('no WebGL playable fallback',no_webgl)
  report['uncaught_page_errors']=errors
  assert not errors,errors
finally:
 server.shutdown();server.server_close()
 (OUT/'report.json').write_text(json.dumps(report,indent=2))
if any(not c['pass'] for c in report['checks']):raise SystemExit(1)
