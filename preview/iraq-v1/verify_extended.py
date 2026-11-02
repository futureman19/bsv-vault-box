from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'iraq-v1.html').as_uri());p.wait_for_function('pilot.ready')
 maps=p.evaluate('''(()=>{let maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh||!o.material.map||seen.has(o.material.map.uuid))return;seen.add(o.material.map.uuid);let im=o.material.map.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0,s=[0,0,0];for(let i=0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);for(let j=0;j<3;j++)s[j]+=d[i+j];}maps.push({name:o.material.name,width:c.width,height:c.height,range:mx-mn,mean:s.map(v=>v/(d.length/4))});});return maps})()''')
 assert len(maps)==2 and all(m['range']>20 and max(m['width'],m['height'])<=512 for m in maps)
 cobalt=next(m for m in maps if 'Cobalt' in m['name']);assert cobalt['mean'][2]>cobalt['mean'][0]*3
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'iraq-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
r={'status':'PASS','decoded_maps':maps,'noJS_poster':True};(R/'extended-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
