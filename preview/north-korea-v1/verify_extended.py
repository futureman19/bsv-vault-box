from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'north-korea-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'North Korea' in p.locator('canvas').get_attribute('aria-label')
 assert 'Japan' not in p.locator('body').inner_text()
 maps=p.evaluate('''(()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let [key,ch] of [['map',0],['roughnessMap',1]]){let t=o.material[key];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}out.push({key,width:c.width,height:c.height,range:mx-mn});}});return out})()''')
 assert len(maps)>=2 and all(x['range']>10 and x['width']<=256 for x in maps)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'north-korea-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));c.close();b.close()
(R/'extended-check.json').write_text(json.dumps({'status':'PASS','decoded_maps':maps,'no_js_poster':True,'country_copy_and_aria':True},indent=2));print('EXTENDED PASS')
