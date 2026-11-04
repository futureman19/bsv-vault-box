from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert np.count_nonzero(im[:,:,:3])>im.shape[0]*im.shape[1];assert im[:,:,3].max()>0
out={'poster_nonblack':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'slovenia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Slovenia' in p.inner_text('body') and not any(s in p.inner_text('body') for s in ['Japan','Yakushima','cedar','JAPAN'])
 out['runtime']=p.evaluate('''(()=>{let maps=[],wrong=[],land=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Landscape')){land.push(o.name);let q=o;while(q&&q.name!=='Lid_Hinge')q=q.parent;if(!q)wrong.push(o.name);}for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0,ch=key==='roughnessMap'?1:0;for(let i=ch;i<a.length;i+=4){mn=Math.min(mn,a[i]);mx=Math.max(mx,a[i]);}maps.push({key,width:im.width,height:im.height,range:mx-mn});}});return {land,wrong,maps}})()''')
 assert len(out['runtime']['land'])==21 and not out['runtime']['wrong']
 assert len(out['runtime']['maps'])>=3 and all(x['range']>10 and max(x['width'],x['height'])<=512 for x in out['runtime']['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'));c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'slovenia-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS')
