from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.2 and im[:,:,:3].max()>100
out={'poster_real_pixels':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'afghanistan-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Afghanistan' in text and all(w not in text for w in ['Japan','Yakushima','Cedar','Moss'])
 assert 'Afghanistan' in p.locator('canvas').get_attribute('aria-label')
 out['maps']=p.evaluate('''(()=>{const maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(const [key,ch] of [['map',0],['roughnessMap',1],['normalMap',0]]){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let x=c.getContext('2d');x.drawImage(im,0,0);let d=x.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,width:c.width,height:c.height,range:mx-mn});}});return maps})()''')
 assert len(out['maps'])>=4 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in out['maps'])
 out['terrain']=p.evaluate("(()=>{let o=pilot.root.getObjectByName('Terrain__Hindu_Kush_three_peaks')||null;let names=[];pilot.root.traverse(x=>{if(x.name.startsWith('Terrain')){let p=x;while(p&&p.name!=='Lid_Hinge')p=p.parent;names.push({name:x.name,lid:!!p});}});return names})()")
 assert out['terrain'] and all(o['lid'] for o in out['terrain'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'afghanistan-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
