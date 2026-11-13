from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.asarray(Image.open(R/'poster.png').convert('RGBA'))
assert (im[:,:,:3].max(axis=2)>30).mean()>.10
assert (im[:,:,3]>128).mean()>.10
out={'poster_nonblack_fraction':float((im[:,:,:3].max(axis=2)>30).mean()),'poster_opaque_fraction':float((im[:,:,3]>128).mean())}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'micronesia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Micronesia / Basalt & Tidal Canals' in text and not any(w in text for w in ['Yakushima','Japan','Cedar','Moss'])
 out['maps']=p.evaluate('''(()=>{let maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(const [slot,ch] of [['map',0],['roughnessMap',1]]){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,lo=255,hi=0;for(let i=ch;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}maps.push({material:o.material.name,slot,channel:ch,width:im.width,height:im.height,range:hi-lo});}});return maps})()''')
 assert len(out['maps'])>=3 and all(m['range']>20 and max(m['width'],m['height'])<=1024 for m in out['maps'])
 out['ancestry']=p.evaluate('''(()=>{let count=0,wrong=[];pilot.root.traverse(o=>{if(!o.isMesh||!['Islet','Lagoon','Basalt_enclosure','Basalt_relief'].some(n=>o.name.startsWith(n)))return;count++;let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name)});return {count,wrong}})()''')
 assert out['ancestry']['count']>=40 and not out['ancestry']['wrong']
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(300);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'micronesia-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
