from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
out={}
a=np.array(Image.open(R/'poster.png').convert('RGBA'));assert a[:,:,:3].max()>100 and np.count_nonzero(a[:,:,3])>a.shape[0]*a.shape[1]*.1
out['poster_nonblank']=True
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'spain-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Spain / Cobalt & Clay' in p.locator('body').inner_text()
 assert not any(x in p.locator('body').inner_text() for x in ['Japan','Yakushima','Mossed'])
 out['runtime']=p.evaluate('''(()=>{let ornaments=[],wrong=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Lid_ornament')){ornaments.push(o.name);let q=o;while(q&&q.name!=='Lid_Hinge')q=q.parent;if(!q)wrong.push(o.name);}for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,material:o.material.name,width:im.width,height:im.height,range:mx-mn});}});return {ornaments,wrong,maps}})()''')
 assert len(out['runtime']['ornaments'])==50 and not out['runtime']['wrong']
 assert len(out['runtime']['maps'])>=4
 assert all(x['range']>0 and max(x['width'],x['height'])<=512 for x in out['runtime']['maps'])
 # Observe reduced motion only on actual rendering frames, not fixed wall-clock sleep.
 p.emulate_media(reduced_motion='reduce')
 p.evaluate('window.samples=[];window.sampling=true;function take(){samples.push(pilot.progress);if(sampling)requestAnimationFrame(take)};requestAnimationFrame(take)')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.locator('#reset').click();p.wait_for_function('pilot.progress===0');p.evaluate('sampling=false')
 samples=p.evaluate('samples');assert all(x in [0,1] for x in samples);out['reduced_motion_frame_samples']=samples
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'spain-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
