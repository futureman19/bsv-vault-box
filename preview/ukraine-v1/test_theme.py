from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert im[:,:,:3].max()>150 and np.mean(im[:,:,3]>0)>.1
out={'poster_actual_pixels_nonblank':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'ukraine-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Ukraine / Petrykivka Bloom' in text and not any(x in text for x in ['Japan','Yakushima','Cedar','Moss'])
 out['features']=p.evaluate('''(()=>{let petals=0,hearts=0,leaves=0,wrong=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(/^(Bloom|Floral|Leaf)/.test(o.name)){let q=o,ok=false;while(q){if(q.name==='Lid_Hinge')ok=true;q=q.parent;}if(!ok)wrong.push(o.name);if(o.name.includes('petal'))petals++;if(o.name.includes('ochre_heart'))hearts++;if(o.name.startsWith('Floral_leaf'))leaves++;}for(let [slot,ch] of [['map',0],['roughnessMap',1]]){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({slot,channel:ch,width:im.width,height:im.height,range:mx-mn});}});return {petals,hearts,leaves,wrong,maps}})()''')
 f=out['features'];assert f['petals']==55 and f['hearts']==5 and f['leaves']==8 and not f['wrong'],f
 assert len(f['maps'])>=3 and all(x['range']>0 and max(x['width'],x['height'])<=1024 for x in f['maps'])
 assert any(x['slot']=='roughnessMap' and x['range']>10 for x in f['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'ukraine-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
