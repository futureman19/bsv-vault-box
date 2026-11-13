from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'norway-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out=p.evaluate('''(()=>{let terrain=[],maps=[],wrong=[];const seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Fjord')){let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);terrain.push(o.name);}if(!o.isMesh)return;for(const [key,ch] of [['map',0],['roughnessMap',1]]){let tex=o.material[key];if(!tex||seen.has(tex.uuid+key))continue;seen.add(tex.uuid+key);let im=tex.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,key,width:im.width,height:im.height,range:mx-mn});}});return {terrain,maps,wrong}})()''')
 assert len(out['terrain'])>=4 and not out['wrong'];assert len(out['maps'])>=3
 assert all(x['range']>0 and max(x['width'],x['height'])<=512 for x in out['maps'])
 text=p.locator('body').inner_text();assert 'Norway / Fjord & Gneiss' in text and not any(x in text for x in ['Japan','Cedar','Yakushima'])
 assert 'Norway' in p.locator('canvas').get_attribute('aria-label')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'norway-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
 out['noJS_poster']=True;out['status']='PASS'
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
