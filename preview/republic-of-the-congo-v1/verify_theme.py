from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'republic-of-the-congo-v1.html').as_uri());p.wait_for_function('pilot.ready')
 result=p.evaluate('''(()=>{const r={crowns:0,trunks:0,clearing:0,water:0,wrong:[],maps:[]};let seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Forest')||o.name.startsWith('Bai')){if(o.name.includes('crown'))r.crowns++;if(o.name.includes('trunk'))r.trunks++;if(o.name.includes('clearing'))r.clearing++;if(o.name.includes('water'))r.water++;if((o.name.includes('crown')||o.name.includes('trunk')||o.name.startsWith('Bai'))&&o.parent.name!=='Lid_Hinge')r.wrong.push(o.name);}if(o.material.map&&!seen.has(o.material.map.uuid)){seen.add(o.material.map.uuid);let im=o.material.map.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let cx=cv.getContext('2d');cx.drawImage(im,0,0);let d=cx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}r.maps.push({name:o.material.name,width:im.width,height:im.height,range:mx-mn});}});return r})()''')
 def accept(r):
  assert r['crowns']==21 and r['trunks']==7 and r['clearing']==1 and r['water']==1 and not r['wrong'],r
  assert len(r['maps'])>=2 and all(m['range']>30 and max(m['width'],m['height'])<=512 for m in r['maps'])
 accept(result)
 # Deliberate post-implementation negative control, not test-first evidence.
 negative=dict(result,crowns=0)
 try:accept(negative)
 except AssertionError:result['missing_canopy_negative_control']='REJECTED as required'
 else:raise AssertionError('Negative control erroneously passed')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'republic-of-the-congo-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);result['noJS_poster']=True;c.close();b.close()
result['status']='PASS';(R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
