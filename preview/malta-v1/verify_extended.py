from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.1 and im[:,:,:3].max()>100
out={'poster_nonempty':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'malta-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Malta' in text and not any(s in text.lower() for s in ['japan','cedar','yakushima','moss'])
 out['features']=p.evaluate('''(()=>{let maps=[],orn=0,wrong=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Harbour')||o.name.startsWith('Peninsula')){orn++;let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}for(const [key,ch] of [['map',0],['roughnessMap',1]]){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,material:o.material.name,width:im.width,height:im.height,range:mx-mn,channel:ch});}});return {orn,wrong,maps}})()''')
 f=out['features'];assert f['orn']==9 and not f['wrong'];assert len(f['maps'])>=3 and all(m['range']>0 and max(m['width'],m['height'])<=1024 for m in f['maps'])
 assert any(m['key']=='roughnessMap' and m['range']>10 for m in f['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'malta-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
a=np.array(Image.open(R/'maps/limestone-color.png'));mean=a.mean(axis=(0,1));assert mean[0]>mean[1]>mean[2] and mean[0]>180
out.update(status='PASS',stone_palette_mean=mean.tolist(),copy_check=True)
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
