from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,:3].max(axis=2)>20).mean()>.1;assert (im[:,:,3]>0).mean()>.1
out={'poster_nonblack_nontransparent':True}
assert 'Japan' not in (R/'motion.mjs').read_text() and 'Japan' not in (R/'viewer.js').read_text()
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'azerbaijan-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Azerbaijan / Lahij Copper' in text and not any(s in text for s in ['Japan','Yakushima','Cedar','Moss']);assert 'Azerbaijan' in p.locator('canvas').get_attribute('aria-label')
 out['maps']=p.evaluate('''(()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let [key,ch] of [['map',0],['roughnessMap',1],['normalMap',0]]){let t=o.material[key];if(!t||seen.has(key+t.uuid))continue;seen.add(key+t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}out.push({key,channel:ch,width:c.width,height:c.height,range:mx-mn});}});return out})()''')
 assert {x['key'] for x in out['maps']}=={'map','roughnessMap','normalMap'}
 assert all(0<x['range'] and max(x['width'],x['height'])<=512 for x in out['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'azerbaijan-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
