from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,:3].max(2)>30).mean()>.1 and (im[:,:,3]>0).mean()>.1
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'belize-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Japan' not in p.locator('body').inner_text() and 'Yakushima' not in p.locator('body').inner_text()
 maps=p.evaluate('''(()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(const key of ['map','roughnessMap','normalMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,a=[];for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4)a.push(d[i]);out.push({key,width:c.width,height:c.height,range:Math.max(...a)-Math.min(...a)});}});return out})()''')
 assert len(maps)>=3 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in maps)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'belize-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
result={'status':'PASS','maps':maps,'no_js_poster':True,'source_poster_nonblack_coverage':float((im[:,:,:3].max(2)>30).mean()),'source_poster_alpha_coverage':float((im[:,:,3]>0).mean()),'no_inherited_country_copy':True}
(R/'extended-check.json').write_text(json.dumps(result,indent=2));print('EXTENDED PASS',json.dumps(result))
