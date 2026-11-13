from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert np.count_nonzero(im[:,:,3])>im.shape[0]*im.shape[1]*.1;assert np.ptp(im[:,:,:3])>50
out={'poster_nonblank':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'brazil-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Brazil' in text and not any(w in text for w in ['Japan','JAPAN','Yakushima','cedar'])
 out['features']=p.evaluate('''(()=>{let counts={forest:0,river:0,canopy:0},maps=[],wrong=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Forest')||o.name.startsWith('River')){counts[o.name.startsWith('Forest')?'forest':'river']++;if(o.name.includes('canopy'))counts.canopy++;let a=o,ok=false;while(a.parent){a=a.parent;if(a.name==='Lid_Hinge')ok=true;}if(!ok)wrong.push(o.name);}for(let [key,ch] of [['map',0],['normalMap',0],['roughnessMap',1]]){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,channel:ch,width:im.width,height:im.height,range:mx-mn});}});return {counts,maps,wrong}})()''')
 f=out['features'];assert f['counts']['canopy']>=12 and f['counts']['river']>=1 and not f['wrong'];assert len(f['maps'])>=5
 assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in f['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'brazil-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
