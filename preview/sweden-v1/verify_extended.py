from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA'); pixels=list(im.getdata());assert sum(p[3]>0 and max(p[:3])>30 for p in pixels)>len(pixels)*.1
out={'poster_actual_render_nonblank':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'sweden-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Sweden / Falun Red & Kurbits' in p.locator('body').inner_text()
 assert not any(s in p.locator('body').inner_text() for s in ['Japan','Yakushima','Mossed granite'])
 out['maps']=p.evaluate('''(()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,channel=key==='roughnessMap'?1:0,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}out.push({material:o.material.name,type:key,width:im.width,height:im.height,range:mx-mn,channel});}});return out})()''')
 assert len(out['maps'])>=3 and all(m['range']>10 and max(m['width'],m['height'])<=512 for m in out['maps'])
 # Real pointer orbit for a more elevated ornament detail capture.
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x,y+100,steps=20);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'lid-detail.png'))
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'sweden-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['no_js_poster']=True
 c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
