from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.2 and im[:,:,:3].max()>100
out={'poster_nonempty':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'tuvalu-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Tuvalu' in text and not any(s in text for s in ['Japan','JAPAN','Yakushima','cedar','Mossed'])
 out['maps']=p.evaluate('''(()=>{let maps=[];let seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let key of ['map','roughnessMap','normalMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,lo=255,hi=0,ch=key==='roughnessMap'?1:0;for(let i=ch;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}maps.push({key,width:c.width,height:c.height,range:hi-lo});}});return maps})()''')
 assert {m['key'] for m in out['maps']}=={'map','roughnessMap','normalMap'}
 assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in out['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'tuvalu-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));print('EXTENDED PASS')
