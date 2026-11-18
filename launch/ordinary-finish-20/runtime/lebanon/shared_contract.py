from pathlib import Path
import json,math,statistics
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent; results=[]
URL='file:///C:/Users/futur/Desktop/bsv-vault-box/.worktrees/t_01954ef5/launch/ordinary-finish-20/baseline/lebanon/lebanon-v1.html'
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for mode,w,h,dpr in [('desktop',1280,900,1),('mobile',390,844,1)]:
  mobile=mode.startswith('mobile');c=b.new_context(offline=True,viewport={'width':w,'height':h},device_scale_factor=dpr,is_mobile=mobile,has_touch=mobile)
  p=c.new_page();errs=[];net=[]
  p.on('pageerror',lambda e:errs.append(str(e)));p.on('request',lambda r:net.append(r.url) if r.url.startswith(('http:','https:')) else None)
  p.goto(URL);p.wait_for_function('pilot.ready',timeout=90000);p.wait_for_timeout(200)
  assert p.evaluate('pilot.renderer.getPixelRatio()')==min(dpr,2)
  assert not p.evaluate('document.documentElement.scrollWidth>innerWidth')
  p.screenshot(path=str(R/f'{mode}-closed.png'),full_page=True,scale='css')
  def press(s):
   p.locator(s).tap() if mobile else p.locator(s).click()
  initial=p.evaluate('pilot.rotation');box=p.locator('canvas').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2
  if mobile:
   cd=c.new_cdp_session(p);cd.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y}]});cd.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x+75,'y':y+10}]});cd.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
  else:
   p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+130,y+20,steps=8);p.mouse.up()
  p.wait_for_function('(a)=>Math.abs(pilot.rotation-a)>.1',arg=initial)
  press('#reset');p.wait_for_function('(a)=>Math.abs(pilot.rotation-a)<1e-6',arg=initial)
  press('#open');p.wait_for_function('pilot.progress===1');assert abs(p.evaluate('pilot.lid')+math.radians(105))<1e-6
  projection=p.evaluate('''(()=>{let max=0;pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(!o.isMesh)return;let p=o.geometry.attributes.position,v=pilot.root.position.clone();for(let i=0;i<p.count;i++){v.fromBufferAttribute(p,i).applyMatrix4(o.matrixWorld).project(pilot.camera);max=Math.max(max,Math.abs(v.x),Math.abs(v.y));}});return max})()''');assert projection<1
  p.screenshot(path=str(R/f'{mode}-open.png'),full_page=True,scale='css')
  press('#open');p.wait_for_function('pilot.progress===0');press('#open');p.wait_for_function('pilot.progress>0 && pilot.progress<1');press('#reset');p.wait_for_function('pilot.progress===0');p.wait_for_timeout(1100);assert p.evaluate('pilot.progress')==0
  p.emulate_media(reduced_motion='reduce');press('#open');p.wait_for_function('pilot.progress===1');press('#reset');p.wait_for_function('pilot.progress===0')
  frames=p.evaluate('''()=>new Promise(resolve=>{let a=[],last;function tick(t){if(last)a.push(t-last);last=t;if(a.length===30)resolve(a);else requestAnimationFrame(tick)}requestAnimationFrame(tick)})''')
  assert not errs and not net
  results.append({'mode':mode,'dpr':dpr,'drawing_ratio':min(dpr,2),'open_close':True,'drag':True,'native_touch':mobile,'interrupted_reset':True,'reduced_motion':True,'projection':projection,'errors':errs,'network':net,'asset':p.evaluate('pilot.asset'),'frame_intervals_ms':frames,'median_frame_interval_ms':statistics.median(frames),'physical_phone_performance':False});c.close()
 for case in ['corrupt-glb','no-js']:
  c=b.new_context(offline=True,viewport={'width':390,'height':844},java_script_enabled=case!='no-js')
  if case=='corrupt-glb':c.add_init_script("const original=window.atob;window.atob=function(s){return s.startsWith('Z2xURg')?'invalid glb bytes':original(s)}")
  p=c.new_page();p.goto(URL)
  if case=='corrupt-glb':
   p.wait_for_function("document.querySelector('#status').textContent.includes('unavailable')");assert p.locator('#fallback').is_visible() and p.locator('#open').is_disabled()
  else:assert p.locator('#fallback').is_visible() and p.locator('#open').is_disabled() and p.locator('#fallback').evaluate('(img)=>img.complete && img.naturalWidth>0')
  p.screenshot(path=str(R/f'{case}.png'),full_page=True,scale='css');results.append({'case':case,'pass':True});c.close()
 b.close()
(R/'browser-check.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
