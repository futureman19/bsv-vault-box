from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');pixels=list(im.getdata());assert sum(p[3]>0 and max(p[:3])>20 for p in pixels)>len(pixels)*.1
out={'actual_poster_nonblack_coverage':sum(p[3]>0 and max(p[:3])>20 for p in pixels)/len(pixels)}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'grenada-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Nutmeg & Mace' in text and all(s not in text for s in ['Japan','Yakushima','cedar','Mossed','Iceland'])
 out['maps']=p.evaluate('''(()=>{let maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let key of ['map','normalMap','roughnessMap']){let tex=o.material[key];if(!tex||seen.has(tex.uuid+key))continue;seen.add(tex.uuid+key);let im=tex.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,key,width:c.width,height:c.height,range:mx-mn});}});return maps})()''')
 assert len(out['maps'])>=6 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in out['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'grenada-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));print('EXTENDED PASS')
