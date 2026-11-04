from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert im[:,:,:3].max()>100 and (im[:,:,3]>0).mean()>.1
out={'poster_nonblack':True,'poster_alpha_coverage':float((im[:,:,3]>0).mean())}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'guatemala-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Guatemala' in p.locator('h1').inner_text();assert not any(s in p.locator('body').inner_text() for s in ['Japan','Yakushima','Cedar','Moss'])
 out['features']=p.evaluate('''(()=>{let maps=[],wrong=[],terrain=[],root=pilot.root;const seen=new Set();root.traverse(o=>{if(o.name.startsWith('Terrain')){let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);terrain.push(o.name);}if(!o.isMesh)return;for(let key of ['map','normalMap','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,key,width:im.width,height:im.height,range:mx-mn});}});return {maps,terrain,wrong}})()''')
 assert not out['features']['wrong'];assert len(out['features']['maps'])>=4
 assert all(x['range']>0 and max(x['width'],x['height'])<=1024 for x in out['features']['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'guatemala-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
