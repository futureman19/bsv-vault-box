from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');a=np.array(im);assert (a[:,:,3]>0).mean()>.1 and a[:,:,:3].max()>80,'blank poster'
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'indian-ocean-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out=p.evaluate('''()=>{let arcs=[],wrong=[],maps=[];let seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Reef_island')||o.name.startsWith('Lagoon')){arcs.push(o.name);let q=o;while(q&&q.name!=='Lid_Hinge')q=q.parent;if(!q)wrong.push(o.name)}if(!o.isMesh)return;for(let k of ['map','roughnessMap','normalMap']){let t=o.material[k];if(!t||seen.has(t.uuid+k))continue;seen.add(t.uuid+k);let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=k==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i])}maps.push({kind:k,range:mx-mn,width:im.width,height:im.height})}});return {arcs,wrong,maps}}''')
 assert len(out['arcs'])==5 and not out['wrong'];assert len(out['maps'])>=4 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in out['maps'])
 text=p.locator('body').inner_text();assert 'Indian Ocean' in text and not any(x in text for x in ['Japan','Yakushima','Cedar','Moss'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.screenshot(path=str(R/'desktop-open-rear.png'));c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'indian-ocean-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('e=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));c.close();b.close()
out.update(status='PASS',no_js_poster=True,poster_nonblank=True,visible_copy=True)
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('PASS EXTENDED',json.dumps(out))
