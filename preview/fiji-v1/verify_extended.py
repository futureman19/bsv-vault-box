from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert im[:,:,:3].max()>100 and np.mean(im[:,:,3]>0)>.1
out={'poster_nonblank':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'fiji-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Masi & Lagoon' in p.locator('h1').inner_text()
 assert not any(s in p.locator('body').inner_text() for s in ['Japan','Yakushima','Cedar','Moss'])
 out['maps']=p.evaluate('''(()=>{let rows=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}rows.push({material:o.material.name,key,width:c.width,height:c.height,range:mx-mn});}});return rows})()''')
 assert len(out['maps'])>=3 and all(x['range']>0 and max(x['width'],x['height'])<=512 for x in out['maps'])
 out['lid_ancestry']=p.evaluate('''(()=>{let names=[],bad=[];pilot.root.traverse(o=>{if(!/^(Reef|Lagoon|Island)_/.test(o.name))return;names.push(o.name);let p=o;while(p&&p.name!=='Lid_Hinge')p=p.parent;if(!p)bad.push(o.name);});return {names,bad};})()''')
 assert len(out['lid_ancestry']['names'])>=8 and not out['lid_ancestry']['bad']
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'fiji-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
