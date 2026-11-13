from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert im.shape[:2]==(760,900);assert (im[:,:,3]>0).mean()>.15 and (im[:,:,:3]>20).mean()>.1
out={'poster_source_render_nonblank':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'saint-kitts-and-nevis-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Twin Peaks & Narrows' in p.locator('h1').inner_text()
 assert 'Japan' not in p.locator('body').inner_text() and 'cedar' not in p.locator('body').inner_text().lower()
 out['maps']=p.evaluate('''(()=>{const maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(const slot of ['map','roughnessMap','normalMap']){const t=o.material[slot];if(!t||seen.has(slot+t.uuid))continue;seen.add(slot+t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0,channel=slot==='roughnessMap'?1:0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({slot,width:c.width,height:c.height,range:mx-mn,channel});}});return maps})()''')
 assert {m['slot'] for m in out['maps']}=={'map','normalMap','roughnessMap'}
 assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in out['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'saint-kitts-and-nevis-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
