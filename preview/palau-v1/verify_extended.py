from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,:3]>20).any(axis=2).mean()>.1;assert (im[:,:,3]>240).mean()>.5
out={'poster_real_render_nonblank':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'palau-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Palau' in text and 'Yakushima' not in text and 'Japan' not in text
 out['features']=p.evaluate('''(()=>{let islands=0,maps=[],wrong=[],seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Island_')){let q=o;while(q&&q.name!=='Lid_Hinge')q=q.parent;if(!q)wrong.push(o.name);if(o.type==='Group'||o.isMesh&&o.parent.name==='Lid_Hinge')islands++;}if(!o.isMesh)return;for(const [key,ch] of [['map',0],['roughnessMap',1]]){let tex=o.material[key];if(!tex||seen.has(tex.uuid+ch))continue;seen.add(tex.uuid+ch);let im=tex.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,kind:key,channel:ch,width:im.width,height:im.height,range:mx-mn});}});return {islands,maps,wrong};})()''')
 assert out['features']['islands']==6 and not out['features']['wrong'],out
 assert len(out['features']['maps'])>=4
 assert all(x['range']>0 and max(x['width'],x['height'])<=1024 for x in out['features']['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'palau-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS'
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
