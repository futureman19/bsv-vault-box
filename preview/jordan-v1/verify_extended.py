from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'jordan-v1.html').as_uri());p.wait_for_function('pilot.ready')
 result=p.evaluate('''(()=>{const maps=[],terrain=[],wrong=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Terrain')){terrain.push(o.name);if(o.parent.name!=='Lid_Hinge')wrong.push(o.name)};for(const slot of ['map','roughnessMap']){const tx=o.material[slot];if(!tx||seen.has(tx.uuid))continue;seen.add(tx.uuid);let im=tx.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,min=255,max=0,sum=[0,0,0];for(let i=0;i<d.length;i+=4){min=Math.min(min,d[i+(slot==='roughnessMap'?1:0)]);max=Math.max(max,d[i+(slot==='roughnessMap'?1:0)]);for(let k=0;k<3;k++)sum[k]+=d[i+k]}maps.push({material:o.material.name,slot,width:im.width,height:im.height,range:max-min,mean:sum.map(x=>x/(im.width*im.height))})}});return {terrain,wrong,maps}})()''')
 assert len(result['terrain'])==5 and not result['wrong']
 assert len(result['maps'])==3
 assert all(m['width']==512 and m['height']==256 and m['range']>20 for m in result['maps'])
 body=next(m for m in result['maps'] if 'Sandstone' in m['material'] and m['slot']=='map')
 assert 145<body['mean'][0]<190 and 70<body['mean'][1]<115 and 40<body['mean'][2]<85,body
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'jordan-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);result['noJS_poster']=True;c.close();b.close()
result['status']='PASS';(R/'extended-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
