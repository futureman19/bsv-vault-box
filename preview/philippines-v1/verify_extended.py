from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'philippines-v1.html').as_uri());p.wait_for_function('pilot.ready')
 r=p.evaluate('''(()=>{let maps=[],names=[];let seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;names.push(o.name);for(let kind of ['map','roughnessMap']){let t=o.material[kind];if(!t||seen.has(t.uuid+kind))continue;seen.add(t.uuid+kind);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=kind==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind,width:c.width,height:c.height,range:mx-mn});}});return {maps,names};})()''')
 assert r['maps'] and all(x['range']>0 and max(x['width'],x['height'])<=256 for x in r['maps'])
 text=p.locator('body').inner_text();assert 'Philippines' in text and not any(x in text for x in ['Japan','Yakushima','Cedar'])
 assert 'Contour' in p.locator('canvas').get_attribute('aria-label');c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'philippines-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));c.close();b.close()
r.update(status='PASS',no_js_poster=True,copy_audit=True)
(R/'extended-check.json').write_text(json.dumps(r,indent=2));print('PASS maps, copy and no-JS fallback')
