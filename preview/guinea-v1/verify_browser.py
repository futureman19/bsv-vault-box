from pathlib import Path
from playwright.sync_api import sync_playwright
import json, math
ROOT=Path(__file__).resolve().parent
results=[]
with sync_playwright() as pw:
 browser=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for name,width,height,mobile in [('desktop',1440,1080,False),('mobile',390,844,True)]:
  context=browser.new_context(viewport={'width':width,'height':height},is_mobile=mobile,has_touch=mobile,offline=True,device_scale_factor=1)
  page=context.new_page();errors=[];requests=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None);page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
  page.goto((ROOT/'guinea-v1.html').as_uri());page.wait_for_function('window.pilot?.ready===true',timeout=25000);page.wait_for_timeout(250)
  asset=page.evaluate('window.pilot.asset');assert asset['degenerate']==0 and asset['nonfinite']==0
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.screenshot(path=str(ROOT/(name+'-closed.png')),full_page=True)
  def press(selector):
   locator=page.locator(selector)
   locator.tap() if mobile else locator.click()
  initial=page.evaluate('pilot.rotation');box=page.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
  if mobile:
   cdp=context.new_cdp_session(page);cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]});cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+75,'y':y+10}]});cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
  else:
   page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+130,y+20,steps=8);page.mouse.up()
  page.wait_for_timeout(100);assert abs(page.evaluate('pilot.rotation')-initial)>.1
  press('#reset');page.wait_for_function('(initial)=>Math.abs(pilot.rotation-initial)<1e-6',arg=initial)
  press('#open');page.wait_for_function('pilot.progress===1');assert abs(page.evaluate('pilot.lid')+math.radians(105))<1e-6
  projected=page.evaluate("""(()=>{let max=0;pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(!o.isMesh)return;let p=o.geometry.attributes.position,v=pilot.root.position.clone();for(let i=0;i<p.count;i++){v.fromBufferAttribute(p,i).applyMatrix4(o.matrixWorld).project(pilot.camera);max=Math.max(max,Math.abs(v.x),Math.abs(v.y));}});return max})()""")
  assert projected<1, f'Open model clipped: {projected}'
  asset['open_projection_max_abs_ndc']=projected
  page.screenshot(path=str(ROOT/(name+'-open.png')),full_page=True)
  press('#open');page.wait_for_function('pilot.progress===0')
  press('#open');page.wait_for_timeout(120);press('#reset');page.wait_for_timeout(1100);assert page.evaluate('pilot.progress')==0
  page.emulate_media(reduced_motion='reduce');press('#open');page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1
  press('#reset');page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0
  assert not errors and not requests
  results.append({'case':name,'asset':asset,'offline_file':True,'external_requests':requests,'errors':errors,'rotation':True,'touch_rotation':mobile,'open_close':True,'reset_mid_motion':True,'reduced_motion':True,'overflow':False,'webgl':page.evaluate("(()=>{let gl=pilot.renderer.getContext(),e=gl.getExtension('WEBGL_debug_renderer_info');return e?gl.getParameter(e.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER)})()")})
  context.close()
 # Corrupt actual embedded GLB input before GLTFLoader.parse, not a bypass flag.
 context=browser.new_context(offline=True,viewport={'width':390,'height':844})
 context.add_init_script("const original=window.atob;window.atob=function(s){return s.startsWith('Z2xURg')?'invalid glb bytes':original(s)}")
 page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((ROOT/'guinea-v1.html').as_uri());page.wait_for_function("document.querySelector('#status').textContent.includes('unavailable')")
 assert page.locator('#fallback').is_visible() and page.locator('#open').is_disabled();assert not errors
 page.screenshot(path=str(ROOT/'mobile-fallback.png'),full_page=True)
 results.append({'case':'corrupted GLB','fallback':True,'unhandled_errors':errors,'caught_loader_errors':page.evaluate('pilot.errors')})
 context.close();browser.close()
(ROOT/'browser-check.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
