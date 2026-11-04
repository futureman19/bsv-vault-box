from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,:3].max(2)>20).mean()>.1;assert (im[:,:,3]>0).mean()>.1
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'suriname-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Yakushima' not in p.locator('body').inner_text() and 'Japan' not in p.locator('body').inner_text()
 maps=p.evaluate('''(()=>{let a=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let [key,ch] of [['map',0],['roughnessMap',1],['normalMap',0]]){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mi=255,ma=0;for(let i=ch;i<d.length;i+=4){mi=Math.min(mi,d[i]);ma=Math.max(ma,d[i]);}a.push({key,channel:ch,width:im.width,height:im.height,range:ma-mi});}});return a})()''')
 assert {'map','normalMap','roughnessMap'} <= {x['key'] for x in maps}
 assert all(x['range']>0 and max(x['width'],x['height'])<=1024 for x in maps)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'suriname-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));b.close()
r=dict(status='PASS',maps=maps,nojs_poster=True,poster_nonblack=True,copy_no_inherited_country=True)
(R/'extended-check.json').write_text(json.dumps(r,indent=2));print('EXTENDED PASS',r)
