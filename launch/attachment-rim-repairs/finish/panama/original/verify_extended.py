from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));coverage=float((im[:,:,3]>0).mean());assert coverage>.1 and np.ptp(im[:,:,:3])>100
out={'poster_nonblank':True,'poster_alpha_coverage':coverage}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'panama-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Panama' in text and not any(s in text.lower() for s in ['japan','iceland','yakushima','cedar'])
 out['runtime']=p.evaluate('''(()=>{let maps=[],wrong=[],ornaments=0;const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(/^(Mangrove|Bank|Tide)/.test(o.name)){ornaments++;let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}for(const type of ['map','roughnessMap']){let t=o.material[type];if(!t||seen.has(t.uuid+type))continue;seen.add(t.uuid+type);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0,ch=type==='roughnessMap'?1:0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({type,material:o.material.name,width:c.width,height:c.height,range:mx-mn});}});return {maps,ornaments,wrong}})()''')
 assert out['runtime']['ornaments']==55 and not out['runtime']['wrong']
 assert len(out['runtime']['maps'])>=4
 assert all(m['range']>10 and max(m['width'],m['height'])<=512 for m in out['runtime']['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'panama-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
out['noJS_poster']=True;out['status']='PASS'
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
