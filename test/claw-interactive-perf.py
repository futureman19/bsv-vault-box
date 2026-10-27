"""Compare vsync ceiling, parent scene and interactive input on same headed GPU."""
import json,pathlib,subprocess,threading
from functools import partial
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from playwright.sync_api import sync_playwright
root=pathlib.Path(__file__).resolve().parents[1]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root/'docs')))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/'
measure='''()=>new Promise(resolve=>{let samples=[],last;function f(t){if(last)samples.push(t-last);last=t;if(samples.length<180)requestAnimationFrame(f);else{samples.sort((a,b)=>a-b);resolve({median_ms:samples[90],p95_ms:samples[171],fps:1000/(samples.reduce((a,b)=>a+b)/samples.length)})}}requestAnimationFrame(f)})'''
report={}
try:
 with sync_playwright() as p:
  b=p.chromium.launch(channel='chrome',headless=False,args=['--disable-features=Vulkan'])
  for mode in ['blank','parent_scene','interactive']:
   page=b.new_page(viewport={'width':1280,'height':1000})
   if mode=='parent_scene':
    for filename in ['index.html','claw.js','claw3d.js']:
     data=subprocess.check_output(['git','show',f'e6727f0:docs/{filename}'],cwd=root)
     page.route(url+('' if filename=='index.html' else filename),lambda r,request,data=data,filename=filename:r.fulfill(body=data,content_type='text/html' if filename=='index.html' else 'text/javascript'))
   if mode!='blank':
    page.goto(url);page.wait_for_function('!!window.claw3dHandle')
   if mode=='interactive':
    page.locator('#playBtn').click();page.locator('#optDemo').click()
    page.keyboard.down('ArrowRight')
    page.evaluate('''()=>{window.stepCosts=[];const h=claw3dHandle,step=h.step;h.step=now=>{const t=performance.now();step(now);stepCosts.push(performance.now()-t)}}''')
   report[mode]=page.evaluate(measure)
   if mode=='interactive':
    c=page.context.new_cdp_session(page);c.send('Emulation.setCPUThrottlingRate',{'rate':4});page.evaluate('stepCosts=[]')
    report['cpu4x']=page.evaluate(measure)
    report['cpu4x']['mechanics_step']=page.evaluate('''()=>{stepCosts.sort((a,b)=>a-b);return {samples:stepCosts.length,p95_ms:stepCosts[Math.floor(stepCosts.length*.95)],max_ms:Math.max(...stepCosts)}}''')
   page.close()
  b.close()
finally: server.shutdown()
(root/'evidence/claw-interactive/perf-comparison.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
