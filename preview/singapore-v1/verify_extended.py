from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,:3].max(axis=2)>20).mean()>.25
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);page=c.new_page();page.goto((R/'singapore-v1.html').as_uri());page.wait_for_function('pilot.ready')
 maps=page.evaluate('''()=>{let rows=[];pilot.root.traverse(o=>{if(!o.isMesh||!o.material.name.includes('Celadon'))return;for(let key of ['map','roughnessMap','normalMap']){let t=o.material[key];if(!t)throw Error('Missing '+key);let im=t.image;let c=document.createElement('canvas');c.width=im.width;c.height=im.height;let x=c.getContext('2d');x.drawImage(im,0,0);let a=x.getImageData(0,0,c.width,c.height).data;let lo=255,hi=0,ch=key==='roughnessMap'?1:0;for(let i=ch;i<a.length;i+=4){lo=Math.min(lo,a[i]);hi=Math.max(hi,a[i]);}rows.push({key,width:im.width,height:im.height,range:hi-lo});}});return rows}''')
 assert maps and all(m['range']>0 and m['width']<=256 for m in maps)
 text=page.locator('body').inner_text();assert 'Singapore' in text and 'Japan' not in text and 'Yakushima' not in text
 assert 'Singapore' in page.locator('canvas').get_attribute('aria-label')
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});page=c.new_page();page.goto((R/'singapore-v1.html').as_uri());assert page.locator('#fallback').is_visible();assert page.locator('#fallback').evaluate('(i)=>i.complete&&i.naturalWidth>0');page.screenshot(path=str(R/'mobile-nojs.png'));b.close()
r={'status':'PASS','decoded_map_ranges':maps,'no_js_poster':True,'poster_nonblack_fraction':float((im[:,:,:3].max(axis=2)>20).mean()),'country_copy_and_aria':True}
(R/'extended-check.json').write_text(json.dumps(r,indent=2));print('EXTENDED PASS')
