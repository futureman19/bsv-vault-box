from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGB'));assert im.std()>15 and (im.max(axis=2)>40).mean()>.15
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'honduras-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Honduras' in text and 'Yakushima' not in text and 'cedar' not in text.lower()
 maps=p.evaluate('''()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let key of ['map','normalMap','roughnessMap']){let t=o.material[key];if(!t||seen.has(key+t.uuid))continue;seen.add(key+t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let x=c.getContext('2d');x.drawImage(im,0,0);let d=x.getImageData(0,0,c.width,c.height).data,lo=255,hi=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}out.push({key,width:c.width,height:c.height,range:hi-lo});}});return out}''')
 assert {'map','normalMap','roughnessMap'}<=set(x['key'] for x in maps)
 assert all(x['range']>0 and max(x['width'],x['height'])<=512 for x in maps)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'honduras-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);b.close()
r={'status':'PASS','maps':maps,'poster_nonblack':True,'no_js_poster':True,'country_copy':True}
(R/'extended-check.json').write_text(json.dumps(r,indent=2));print(r)
