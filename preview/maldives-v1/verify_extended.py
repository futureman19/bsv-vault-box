from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.size==(900,820);assert max(im.getchannel('A').getextrema())>0;assert max(im.convert('RGB').getextrema()[0])>100
out={'poster_pixels':'PASS'}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'maldives-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Japan' not in p.locator('body').inner_text();assert 'Maldives' in p.locator('canvas').get_attribute('aria-label')
 out['maps']=p.evaluate('''(()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let slot of ['map','roughnessMap','normalMap']){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let cx=c.getContext('2d');cx.drawImage(im,0,0);let d=cx.getImageData(0,0,c.width,c.height).data,min=255,max=0;for(let i=slot==='roughnessMap'?1:0;i<d.length;i+=4){min=Math.min(min,d[i]);max=Math.max(max,d[i]);}out.push({slot,width:c.width,height:c.height,range:max-min})}});return out})()''')
 assert len(out['maps'])==3 and all(m['range']>0 and m['width']==256 and m['height']==256 for m in out['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(250);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'maldives-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']='PASS';c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
