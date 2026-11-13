from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'bahrain-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out=p.evaluate('''(()=>{let ornaments=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Oyster')||o.name.startsWith('Pearl'))ornaments.push({name:o.name,parent:o.parent.name});for(let slot of ['map','normalMap','roughnessMap']){let tx=o.material[slot];if(!tx||seen.has(tx.uuid))continue;seen.add(tx.uuid);let im=tx.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let cx=c.getContext('2d');cx.drawImage(im,0,0);let d=cx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=(slot==='roughnessMap'?1:0);i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({slot,width:im.width,height:im.height,range:mx-mn});}});return {ornaments,maps};})()''')
 assert len(out['ornaments'])==3 and all(o['parent']=='Lid_Hinge' for o in out['ornaments'])
 print(json.dumps(out,indent=2))
 assert len(out['maps'])>=3 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in out['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'bahrain-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
