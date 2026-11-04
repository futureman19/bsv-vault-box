from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.asarray(Image.open(R/'maps/celadon-color.png').convert('RGB'));means=im.mean(axis=(0,1));ranges=np.ptp(im,axis=(0,1));assert 95<means[0]<155 and 145<means[1]<200 and 135<means[2]<190 and min(ranges)>20
poster=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert (poster[:,:,3]>0).mean()>.05 and poster[:,:,:3].max()>60
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'thailand-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Japan' not in p.locator('body').inner_text();assert 'Thailand' in p.locator('canvas').get_attribute('aria-label')
 maps=p.evaluate('''()=>{let a=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}a.push({key,width:c.width,height:c.height,range:mx-mn});}});return a}''')
 assert maps and all(x['range']>0 and x['width']<=256 and x['height']<=256 for x in maps)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'thailand-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);b.close()
r={'status':'PASS','palette_means':means.tolist(),'palette_ranges':ranges.tolist(),'runtime_maps':maps,'poster_nonempty':True,'noJS_poster':True,'country_copy_accessibility':True}
(R/'extended-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
