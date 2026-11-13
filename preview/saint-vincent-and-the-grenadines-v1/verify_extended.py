from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.width>=700 and im.height>=600
pixels=list(im.getdata());assert sum(max(p[:3])>30 and p[3]>0 for p in pixels)>len(pixels)*.25
out={'poster_nonblack':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'saint-vincent-and-the-grenadines-v1.html').as_uri());p.wait_for_function('pilot.ready',timeout=90000)
 text=p.locator('body').inner_text();assert 'Saint Vincent and the Grenadines' in text and 'Yakushima' not in text and 'Japan' not in text
 out['features']=p.evaluate('''(()=>{let maps=[],wrong=[],cays=0;const seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Cay_'))cays++;if(['Cay_','Soufriere_','Sea_','Reef_'].some(n=>o.name.startsWith(n))){let a=o,ok=false;while(a){if(a.name==='Lid_Hinge')ok=true;a=a.parent;}if(!ok)wrong.push(o.name);}if(!o.isMesh)return;for(const [key,ch] of [['map',0],['roughnessMap',1],['normalMap',0]]){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,channel:ch,width:im.width,height:im.height,range:mx-mn});}});return {cays,maps,wrong}})()''')
 # Multi-material source cays export as a group plus primitives; count groups by exact base names.
 out['cay_groups']=p.evaluate("[1,2,3,4,5].map(i=>!!pilot.root.getObjectByName('Cay__'+i))")
 assert all(out['cay_groups']) and len(out['cay_groups'])==5
 assert not out['features']['wrong'];assert len(out['features']['maps'])>=3
 assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in out['features']['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(250);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'saint-vincent-and-the-grenadines-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out,indent=2))
