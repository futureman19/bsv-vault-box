from playwright.sync_api import sync_playwright
import json,pathlib
out=pathlib.Path('evidence/claw3d');out.mkdir(parents=True,exist_ok=True)
report={}
with sync_playwright() as p:
 b=p.chromium.launch(channel='chrome',headless=False,args=['--disable-features=Vulkan'])
 for name,w,h in [('desktop',1280,900),('mobile',390,844)]:
  page=b.new_page(viewport={'width':w,'height':h},device_scale_factor=1,reduced_motion='reduce')
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.goto('http://127.0.0.1:4179/');page.wait_for_timeout(2000)
  data=page.evaluate('''() => { const c=document.querySelector('.claw3d-canvas');const gl=c?.getContext('webgl2');const ext=gl?.getExtension('WEBGL_debug_renderer_info');return {ready:document.querySelector('.machine-wrap').className,renderer:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):null,canvas:c?{width:c.width,height:c.height}:null, fallback:getComputedStyle(document.querySelector('.cabinet')).display}; }''')
  page.screenshot(path=str(out/(name+'.png')));data['errors']=errors;report[name]=data
  assert data['renderer'] and 'SwiftShader' not in data['renderer'],data
  assert 'claw3d-ready' in data['ready'] and not errors,data
  frozen=page.locator('.claw3d-canvas').screenshot();page.wait_for_timeout(250)
  assert frozen==page.locator('.claw3d-canvas').screenshot()
  page.emulate_media(reduced_motion='no-preference');page.wait_for_timeout(500)
  assert frozen!=page.locator('.claw3d-canvas').screenshot()
  data['raf_timing']=page.evaluate('''() => new Promise(resolve=>{let times=[],last;function frame(t){if(last)times.push(t-last);last=t;if(times.length<180)requestAnimationFrame(frame);else {times.sort((a,b)=>a-b);resolve({samples:times.length,median_ms:times[90],p95_ms:times[171],note:'desktop GPU even at mobile viewport; not phone proof'})}}requestAnimationFrame(frame)})''')
  data['reduced_motion_and_idle']='passed'
  page.evaluate('window.claw3dHandle.dispose();window.claw3dHandle.dispose()')
  assert page.locator('.claw3d-canvas').count()==0
  assert page.locator('.cabinet').is_visible()
  page.evaluate("window.claw3dHandle=window.Claw3D.mount(document.querySelector('.machine-wrap'))")
  assert page.locator('.claw3d-canvas').count()==1
  page.evaluate("document.querySelector('canvas').getContext('webgl2').getExtension('WEBGL_lose_context').loseContext()")
  page.wait_for_timeout(300)
  assert page.locator('.cabinet').is_visible()
  data['dispose_remount_context_loss']='passed'
  page.close()
 b.close()
 b=p.chromium.launch(channel='chrome',headless=False,args=['--disable-webgl'])
 page=b.new_page(viewport={'width':390,'height':844},reduced_motion='reduce'); errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
 page.goto('http://127.0.0.1:4179/');page.wait_for_timeout(1000)
 assert page.locator('.cabinet').is_visible() and page.locator('.claw3d-canvas').count()==0
 page.screenshot(path=str(out/'fallback.png'));report['fallback']={'present':True,'errors':errors};assert not errors
 candidate=page.locator('.cabinet').screenshot()
 import subprocess
 baseline_html=subprocess.check_output(['git','show','2258bf5b7fb319c33e94112a5bedf00b71231f6f:docs/index.html'])
 page.route('http://127.0.0.1:4179/',lambda route:route.fulfill(body=baseline_html,content_type='text/html'))
 page.reload();page.wait_for_timeout(1000)
 assert candidate==page.locator('.cabinet').screenshot()
 report['fallback']['baseline_pixel_parity']='passed'
 b.close()
(out/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
