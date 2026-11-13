from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'turkmenistan-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Japan' not in p.locator('body').inner_text()
 assert 'Turkmenistan' in p.locator('canvas').get_attribute('aria-label')
 out['features']=p.evaluate('''(()=>{let ornaments=0,wrong=[],maps=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Carpet')){ornaments++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}for(const [kind,channel] of [['map',0],['roughnessMap',1]]){let t=o.material[kind];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=channel;i<a.length;i+=4){mn=Math.min(mn,a[i]);mx=Math.max(mx,a[i]);}maps.push({kind,channel,width:c.width,height:c.height,range:mx-mn});}});return{ornaments,wrong,maps}})()''')
 assert out['features']['ornaments']==58 and not out['features']['wrong']
 assert len(out['features']['maps'])>=3
 assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in out['features']['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']/2,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'turkmenistan-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.1 and im[:,:,:3].max()>100
out['poster_nonempty']=True;out['status']='PASS'
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
