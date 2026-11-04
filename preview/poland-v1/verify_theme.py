from pathlib import Path
import json
from PIL import Image
import numpy as np
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.2 and im[:,:,:3].max()>100
out={'poster_nonempty':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'poland-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Poland / Cobalt & Cream' in text and not any(s in text.lower() for s in ['japan','yakushima','cedar','moss'])
 out['features']=p.evaluate('''(()=>{let petals=[],wrong=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Rosette')){if(o.name.includes('petal'))petals.push(o.name);let q=o;while(q&&q.name!=='Lid_Hinge')q=q.parent;if(!q)wrong.push(o.name);}for(let [k,ch] of [['map',0],['roughnessMap',1]]){let t=o.material[k];if(!t||seen.has(t.uuid+k))continue;seen.add(t.uuid+k);let im=t.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind:k,width:im.width,height:im.height,range:mx-mn});}});return {petals,wrong,maps};})()''')
 assert len(out['features']['petals'])==8 and not out['features']['wrong']
 assert {m['kind'] for m in out['features']['maps']}=={'map','roughnessMap'}
 assert all(m['range']>0 and max(m['width'],m['height'])<=1024 for m in out['features']['maps'])
 # Real altered hierarchy negative control; restore after asserting rejection.
 negative=p.evaluate('''(()=>{let o=pilot.root.getObjectByName('Rosette__petal_0')||(()=>{let r;pilot.root.traverse(x=>{if(x.name.startsWith('Rosette')&&x.name.includes('petal'))r=x});return r})();let old=o.parent;pilot.root.attach(o);let q=o;while(q&&q.name!=='Lid_Hinge')q=q.parent;let rejected=!q;old.attach(o);return rejected})()''');assert negative;out['detached_petal_negative_rejected']=negative
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'poland-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));out['nojs_poster']=True
 b.close()
a=np.array(Image.open(R/'maps/ceramic-color.png'));blue=(a[:,:,2]>a[:,:,0]*1.5)&(a[:,:,0]<70);cream=(a[:,:,0]>200)&(a[:,:,1]>190);assert blue.mean()>.1 and cream.mean()>.4
out['palette']={'cobalt_fraction':float(blue.mean()),'cream_fraction':float(cream.mean())};out['status']='PASS'
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
