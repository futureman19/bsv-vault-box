from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'brunei-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Brunei / Tenunan Gold' in p.inner_text('body')
 assert 'Cedar' not in p.locator('canvas').get_attribute('aria-label')
 maps=p.evaluate('''()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let k of ['map','roughnessMap']){let t=o.material[k];if(!t||seen.has(t.uuid+k))continue;seen.add(t.uuid+k);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=k==='roughnessMap'?1:0;i<a.length;i+=4){mn=Math.min(mn,a[i]);mx=Math.max(mx,a[i]);}out.push({kind:k,range:mx-mn,width:c.width,height:c.height});}});return out}''')
 assert len(maps)>=4 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in maps)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'brunei-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));b.close()
r={'status':'PASS','maps':maps,'no_js_poster':True,'copy_and_accessibility':True};(R/'extended-check.json').write_text(json.dumps(r,indent=2));print(r)
