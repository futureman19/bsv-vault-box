from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.asarray(Image.open(R/'maps/stone-color.png').convert('RGB'));means=im.mean(axis=(0,1));assert 145<means[0]<185 and 105<means[1]<155 and 65<means[2]<115
poster=np.asarray(Image.open(R/'poster.png').convert('RGB'));assert (poster.max(axis=2)>40).mean()>.1
out={'status':'PASS','stone_mean_rgb':means.tolist(),'poster_nonblack_fraction':float((poster.max(axis=2)>40).mean())}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'cambodia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Cambodia' in p.locator('canvas').get_attribute('aria-label')
 assert not any(s in p.locator('body').inner_text() for s in ['Japan','Cedar','Yakushima'])
 out['maps']=p.evaluate('''(()=>{let seen=new Set(),maps=[];pilot.root.traverse(o=>{if(!o.isMesh)return;for(const k of ['map','roughnessMap']){let t=o.material[k];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,lo=255,hi=0,ch=k==='roughnessMap'?1:0;for(let i=ch;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}maps.push({kind:k,width:c.width,height:c.height,range:hi-lo});}});return maps})()''')
 assert len(out['maps'])>=3 and all(m['range']>0 and max(m['width'],m['height'])<=256 for m in out['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'cambodia-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['no_js_poster']=True;c.close();b.close()
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
