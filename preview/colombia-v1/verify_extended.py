from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.getchannel('A').getextrema()[1]>0
assert max(im.convert('RGB').getextrema()[i][1] for i in range(3))>80
out={'poster_nonblack':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'colombia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['maps']=p.evaluate('''(()=>{const out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(const k of ['map','roughnessMap']){let t=o.material[k];if(!t||seen.has(t.uuid+k))continue;seen.add(t.uuid+k);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let x=c.getContext('2d');x.drawImage(im,0,0);let d=x.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=k==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}out.push({material:o.material.name,kind:k,range:mx-mn,width:c.width,height:c.height});}});return out})()''')
 assert len(out['maps'])>=3 and all(m['range']>10 and max(m['width'],m['height'])<=512 for m in out['maps'])
 text=p.locator('body').inner_text();assert 'Coffee Cordillera' in text and not any(s in text for s in ['Japan','Yakushima','Cedar','Moss'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'colombia-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));out['nojs_poster']=True;b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
