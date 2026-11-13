from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGB');assert im.getextrema()[0][1]>100
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'senegal-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Senegal' in p.locator('h1').inner_text()
 assert not any(x in p.locator('body').inner_text() for x in ['Japan','JAPAN','Yakushima','cedar'])
 assert 'Senegal' in p.locator('canvas').get_attribute('aria-label')
 maps=p.evaluate('''(()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let [name,ch] of [['map',0],['roughnessMap',1]]){let t=o.material[name];if(!t||seen.has(t.uuid+name))continue;seen.add(t.uuid+name);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=ch;i<a.length;i+=4){mn=Math.min(mn,a[i]);mx=Math.max(mx,a[i])}out.push({name,width:c.width,height:c.height,range:mx-mn,channel:ch})}});return out})()''')
 assert len(maps)>=3 and all(x['range']>0 and max(x['width'],x['height'])<=512 for x in maps)
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(300);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'senegal-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
out={'status':'PASS','portable_maps':maps,'noJS_poster':True,'source_poster_nonblack':True,'copy_and_aria_country':True}
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
