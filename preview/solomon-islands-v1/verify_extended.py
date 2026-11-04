from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.width>=800 and im.getextrema()[3][1]>0
assert max(im.convert('RGB').getextrema()[0])>80
out={'status':'PASS','real_render_nonblack':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'solomon-islands-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Solomon Islands' in text and not any(x in text for x in ['Japan','Yakushima','Moss','cedar'])
 out['maps']=p.evaluate('''(()=>{let maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let [key,ch] of [['map',0],['roughnessMap',1]]){let m=o.material,t=m[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({name:m.name,key,channel:ch,width:c.width,height:c.height,min:mn,max:mx,range:mx-mn});}});return maps;})()''')
 assert len(out['maps'])>=3 and all(x['range']>0 and max(x['width'],x['height'])<=512 for x in out['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'solomon-islands-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
