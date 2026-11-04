from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'))
assert (im[:,:,:3].max(axis=2)>20).mean()>.1,'black poster'
assert (im[:,:,3]>128).mean()>.1,'transparent poster'
out={'poster_nonblack_fraction':float((im[:,:,:3].max(axis=2)>20).mean())}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'vatican-city-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Vatican City' in p.locator('h1').inner_text()
 assert not any(s in p.locator('body').inner_text() for s in ['Japan','Yakushima','Cedar','Moss'])
 out['maps']=p.evaluate('''(()=>{const maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(const [slot,ch] of [['map',0],['roughnessMap',1]]){const t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);const im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;const ctx=c.getContext('2d');ctx.drawImage(im,0,0);const d=ctx.getImageData(0,0,c.width,c.height).data;let mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,slot,channel:ch,width:c.width,height:c.height,range:mx-mn});}});return maps})()''')
 assert len(out['maps'])>=3 and any(m['slot']=='roughnessMap' for m in out['maps'])
 assert all(m['range']>10 and max(m['width'],m['height'])<=256 for m in out['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.locator('#reset').click();p.wait_for_function('pilot.progress===0')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'vatican-city-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
