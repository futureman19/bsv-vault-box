from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'sri-lanka-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Sri Lanka' in p.locator('h1').inner_text()
 assert 'Sri Lanka' in p.locator('canvas').get_attribute('aria-label')
 assert not any(x in p.locator('body').inner_text().lower() for x in ['japan','cedar','yakushima','moss'])
 maps=p.evaluate('''(()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}out.push({key,material:o.material.name,width:c.width,height:c.height,range:mx-mn});}});return out})()''')
 assert len(maps)>=3 and all(x['range']>0 and max(x['width'],x['height'])<=512 for x in maps),maps
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'sri-lanka-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
(R/'extended-check.json').write_text(json.dumps({'status':'PASS','copy_and_aria':True,'maps':maps,'no_js_poster':True},indent=2));print('EXTENDED PASS')
