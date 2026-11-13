from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert im[:,:,:3].std()>15 and (im[:,:,3]>0).mean()>.1
out={'poster_nonblank':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'barbados-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Yakushima' not in p.locator('body').inner_text() and 'JAPAN' not in p.locator('body').inner_text()
 out['maps']=p.evaluate('''(()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let kind of ['map','roughnessMap','normalMap']){let t=o.material[kind];if(!t||seen.has(t.uuid+kind))continue;seen.add(t.uuid+kind);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=kind==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}out.push({kind,range:mx-mn,width:c.width,height:c.height});}});return out})()''')
 assert {m['kind'] for m in out['maps']}=={'map','roughnessMap','normalMap'}
 assert all(m['range']>0 and max(m['width'],m['height'])<=1024 for m in out['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'barbados-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
