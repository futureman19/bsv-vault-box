from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.2 and im[:,:,:3].max()>100
out={'poster_nonblack_nontransparent':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'netherlands-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Netherlands / Delft & Polder' in p.locator('body').inner_text()
 assert 'Japan' not in p.locator('body').inner_text()
 out['maps']=p.evaluate('''(()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let slot of ['map','roughnessMap']){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,channel=slot==='roughnessMap'?1:0,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}out.push({slot,channel,width:c.width,height:c.height,range:mx-mn});}});return out})()''')
 assert len(out['maps'])==2
 assert all(x['range']>0 and max(x['width'],x['height'])<=1024 for x in out['maps'])
 # Negative control: actually detach mill from lid, then ancestry oracle rejects.
 out['ancestry_negative_control']=p.evaluate('''(()=>{const mill=pilot.root.getObjectByName('Mill__tower')||(()=>{let m;pilot.root.traverse(o=>{if(o.name.includes('Mill')&&o.name.includes('tower'))m=o});return m})();const parent=mill.parent;const valid=()=>{let p=mill.parent;while(p){if(p.name==='Lid_Hinge')return true;p=p.parent}return false};let before=valid();pilot.root.attach(mill);let rejected=!valid();parent.attach(mill);return {before,rejected,restored:valid()}})()''')
 assert all(out['ancestry_negative_control'].values())
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'netherlands-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['no_js_poster']=True;c.close();b.close()
a=np.array(Image.open(R/'maps/delft-color.png'));blue=(a[:,:,2]>a[:,:,0]*1.4)&(a[:,:,0]<100);ivory=(a[:,:,0]>200)&(a[:,:,1]>200)
assert blue.mean()>.08 and ivory.mean()>.45
out.update(status='PASS',cobalt_fraction=float(blue.mean()),ivory_fraction=float(ivory.mean()))
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
