"""Bounded real Edge verification. No network beyond owned loopback server."""
import json,hashlib,threading,os
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright
from build import ROOT,OUT,dump
E=ROOT/os.environ.get('CAPTURE_DIR','browser');E.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(OUT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
results=[]
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
  for offline in [False,True]:
   for mobile in [False,True]:
    label=('offline' if offline else 'hosted')+('-mobile' if mobile else '-desktop')
    ctx=browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 1000},is_mobile=mobile,has_touch=mobile,reduced_motion='reduce',offline=offline)
    page=ctx.new_page();errors=[];external=[]
    page.on('pageerror',lambda x:errors.append(str(x)))
    page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
    def route(r):
     u=r.request.url
     if u.startswith(('http:','https:')) and not u.startswith(base+'/'):external.append(u);r.abort()
     else:r.continue_()
    ctx.route('**/*',route)
    page.goto((OUT/'review.html').as_uri() if offline else base+'/index.html')
    page.wait_for_function('window.__collection?.count===201')
    assert page.locator('.card').count()==201
    page.screenshot(path=str(E/f'{label}.png'),full_page=False)
    for cat,count in [('Country',195),('Ocean',5),('Moon',1),('All',201)]:
     page.locator('#category').select_option(cat);assert page.locator('.card').count()==count
    for q,id in [('the moon','the-moon'),('COTE D IVOIRE','cote-d-ivoire'),('bangladesh','bangladesh'),('united states','united-states')]:
     page.locator('#search').fill(q);assert page.locator('.card').count()==1;assert page.locator('.card').get_attribute('data-id')==id
    page.locator('#search').fill('zzzzzz-no-design');assert page.locator('#empty').is_visible()
    page.locator('#reset').click();page.locator('#scope').select_option('changed');assert page.locator('.card').count()==17
    page.locator('#scope').select_option('hold');expected=len([x for x in json.loads((OUT/'manifest.json').read_bytes())['entries'] if x['disposition']=='substantive-feature-hold']);assert page.locator('.card').count()==expected
    page.locator('#reset').click();page.locator('#imagery').select_option('marketing');assert 'Promotional artwork' in page.locator('#status').inner_text()
    page.locator('#search').fill('united states');card=page.locator('.card');card.focus();page.keyboard.press('Enter');page.wait_for_selector('dialog[open]');assert page.locator('#close').evaluate('(e)=>e===document.activeElement')
    assert 'main wall' in page.locator('#issue').inner_text()
    for key in ['Tab','Tab','Shift+Tab','Shift+Tab']:
     page.keyboard.press(key);assert page.evaluate("document.activeElement===document.body||document.querySelector('dialog').contains(document.activeElement)")
    page.locator('#search').evaluate('(e)=>e.focus()');assert not page.locator('#search').evaluate('(e)=>e===document.activeElement')
    page.screenshot(path=str(E/f'{label}-usa-detail.png'),full_page=False)
    page.keyboard.press('Escape');page.wait_for_selector('dialog[open]',state='hidden');assert card.evaluate('(e)=>e===document.activeElement')
    card.tap() if mobile else card.click()
    if offline:assert page.locator('#full-viewer').is_hidden() and page.locator('#load-model').is_hidden()
    else:
     page.locator('#load-model').click();frame=page.frame_locator('#interactive iframe');frame.locator('#open').wait_for(state='visible',timeout=30000)
     page.wait_for_function("document.querySelector('iframe').contentWindow.pilot?.ready===true",timeout=30000)
     frame.locator('#open').click();page.wait_for_function("document.querySelector('iframe').contentWindow.pilot.progress===1")
     page.locator('#load-model').click();assert page.locator('iframe').count()==0
    page.locator('#close').click();assert card.evaluate('(e)=>e===document.activeElement')
    page.locator('#reset').click();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    # Decode all 402 actual model / promotional images, not just first viewport.
    count=page.evaluate('''async()=>{let n=0;for(const e of DATA)for(const kind of ['poster','marketing']){const im=new Image();im.src=e[kind].url;await im.decode();if(!im.naturalWidth)throw Error(e.id);n++}return n}''');assert count==402
    assert not errors and not external,(errors,external)
    results.append({'case':label,'cards':201,'decoded_images':count,'search_filters_empty_reset':True,'dialog_keyboard_touch_focus_restore':True,'iframe_open_close':not offline,'offline_no_broken_viewer_links':offline,'errors':errors,'external':external,'overflow':False})
    dump(E/'progress.json',results);ctx.close()
  # Native controls on delivered immutable changed models. No engine re-authoring/collision rerun.
  ids=['united-states','bangladesh','ghana','guyana','mozambique','panama','cabo-verde','saint-vincent-and-the-grenadines']
  manifest={e['id']:e for e in json.loads((OUT/'manifest.json').read_bytes())['entries']}
  for id in ids:
   for mobile in [False,True]:
    ctx=browser.new_context(viewport={'width':390 if mobile else 1440,'height':844 if mobile else 1000},is_mobile=mobile,has_touch=mobile,offline=True)
    page=ctx.new_page();errors=[];requests=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
    path=OUT/manifest[id]['viewer']['url'];assert hashlib.sha256(path.read_bytes()).hexdigest()==manifest[id]['viewer']['sha256']
    page.goto(path.as_uri());page.wait_for_function('window.pilot?.ready===true',timeout=45000)
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    mode='mobile' if mobile else 'desktop';page.screenshot(path=str(E/f'{id}-{mode}-closed.png'),full_page=True)
    def press(sel):page.locator(sel).tap() if mobile else page.locator(sel).click()
    rotation=page.evaluate('pilot.rotation');b=page.locator('canvas').bounding_box();x=b['x']+b['width']*.5;y=b['y']+b['height']*.5
    if mobile:
     c=ctx.new_cdp_session(page);c.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]});c.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+75,'y':y+10}]});c.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    else:page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+100,y+10,steps=8);page.mouse.up()
    page.wait_for_function('(r)=>Math.abs(pilot.rotation-r)>.1',arg=rotation)
    press('#reset');press('#open');page.wait_for_function('pilot.progress===1');page.screenshot(path=str(E/f'{id}-{mode}-open.png'),full_page=True)
    press('#open');page.wait_for_function('pilot.progress===0');press('#open');page.wait_for_function('pilot.progress>0&&pilot.progress<1');press('#reset');page.wait_for_function('pilot.progress===0')
    page.emulate_media(reduced_motion='reduce');press('#open');page.wait_for_function('pilot.progress===1');press('#reset');page.wait_for_function('pilot.progress===0')
    assert not errors and not requests
    results.append({'id':id,'mode':mode,'viewer_sha256':manifest[id]['viewer']['sha256'],'native_open_close_reset_drag':True,'interrupted_reset':True,'reduced_motion_endpoints':True,'errors':errors,'external_requests':requests,'offline':True})
    dump(E/'progress.json',results);ctx.close()
  browser.close()
 dump(E/'results.json',results);print(json.dumps({'cases':len(results),'pass':True}))
finally:server.shutdown();server.server_close()
