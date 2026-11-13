from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'south-sudan-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['maps']=p.evaluate('''(()=>{const seen=new Set(),out=[];pilot.root.traverse(o=>{if(!o.isMesh)return;for(const key of ['map','roughnessMap']){const t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);const im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;const ctx=c.getContext('2d');ctx.drawImage(im,0,0);const d=ctx.getImageData(0,0,c.width,c.height).data;let lo=255,hi=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}out.push({key,width:c.width,height:c.height,range:hi-lo});}});return out})()''')
 assert len(out['maps'])>=4 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in out['maps'])
 assert 'South Sudan' in p.locator('h1').inner_text() and 'South Sudan' in p.locator('canvas').get_attribute('aria-label')
 assert 'Japan' not in p.locator('body').inner_text()
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']/2,y,steps=30);p.mouse.up();p.screenshot(path=str(R/'desktop-open-rear.png'));c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'south-sudan-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
