from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'))
assert (im[:,:,:3].max(2)>30).mean()>.10,'black poster'
assert (im[:,:,3]>0).mean()>.5,'transparent poster'
out={'poster_nonblack_fraction':float((im[:,:,:3].max(2)>30).mean())}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'marshall-islands-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let orn=[],maps=[],wrong=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Chart')||o.name.startsWith('Atoll')){orn.push(o.name);let q=o.parent;while(q&&q.name!=='Lid_Hinge')q=q.parent;if(!q)wrong.push(o.name);}for(const [slot,ch] of [['map',0],['roughnessMap',1]]){let map=o.material[slot];if(!map||seen.has(map.uuid+slot))continue;seen.add(map.uuid+slot);let im=map.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,slot,channel:ch,width:im.width,height:im.height,range:mx-mn});}});return {orn,maps,wrong}})()''')
 assert len(out['features']['orn'])==15 and not out['features']['wrong']
 assert all(x['range']>5 and max(x['width'],x['height'])<=512 for x in out['features']['maps'])
 assert len(out['features']['maps'])>=4
 text=p.locator('body').inner_text();assert 'Marshall Islands / Pandanus & Swell' in text and not any(x in text for x in ['Japan','Yakushima','Mossed granite','JAPAN'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'marshall-islands-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
