from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent;out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'kiribati-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Kiribati / Pandanus & Lagoon' in text and all(x not in text for x in ['Japan','Cedar','Yakushima','Mossed']);out['visible_copy']='PASS'
 out['features']=p.evaluate('''(()=>{let maps=[],wrong=[],ornaments=0,panels=0;const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Pandanus_'))panels++;if(/^(Atoll|Lagoon)/.test(o.name)){ornaments++;let par=o.parent;while(par&&par.name!=='Lid_Hinge')par=par.parent;if(!par)wrong.push(o.name);}for(let [slot,ch] of [['map',0],['roughnessMap',1],['normalMap',0]]){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let data=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<data.length;i+=4){mn=Math.min(mn,data[i]);mx=Math.max(mx,data[i]);}maps.push({material:o.material.name,slot,channel:ch,width:im.width,height:im.height,range:mx-mn});}});return {maps,wrong,ornaments,panels}})()''')
 f=out['features'];assert f['ornaments']==21 and f['panels']==4 and not f['wrong'];assert len(f['maps'])>=4
 assert all(m['range']>0 and m['width']<=512 and m['height']<=256 for m in f['maps']);assert any(m['slot']=='roughnessMap' and m['channel']==1 for m in f['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'kiribati-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']='PASS';c.close();b.close()
a=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert (a[:,:,3]>0).mean()>.2 and a[:,:,:3].mean()>10;out['poster_pixels']={'width':a.shape[1],'height':a.shape[0],'alpha_coverage':float((a[:,:,3]>0).mean()),'rgb_mean':float(a[:,:,:3].mean())};out['status']='PASS'
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
