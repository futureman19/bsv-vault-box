from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.1 and im[:,:,:3].max()>100
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'portugal-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Portugal' in p.locator('body').inner_text() and 'Japan' not in p.locator('body').inner_text()
 out=p.evaluate('''(()=>{let waves=[],maps=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Atlantic_wave')){waves.push({name:o.name,parent:o.parent.name});}for(let key of ['map','roughnessMap','normalMap']){let t=o.material[key];if(!t||seen.has(key+t.uuid))continue;seen.add(key+t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let x=c.getContext('2d');x.drawImage(im,0,0);let d=x.getImageData(0,0,c.width,c.height).data,mi=255,ma=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mi=Math.min(mi,d[i]);ma=Math.max(ma,d[i]);}maps.push({key,width:c.width,height:c.height,range:ma-mi});}});return {waves,maps}})()''')
 assert len(out['waves'])==3 and all(w['parent']=='Lid_Hinge' for w in out['waves'])
 assert len(out['maps'])==3 and all(m['range']>0 and m['width']==512 and m['height']==512 for m in out['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'portugal-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
out.update(status='PASS',noJS_poster=True,poster_pixels=True,visible_country_copy=True)
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
