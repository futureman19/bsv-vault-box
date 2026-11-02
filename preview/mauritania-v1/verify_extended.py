from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'mauritania-v1.html').as_uri());p.wait_for_function('pilot.ready')
 features=p.evaluate('''(()=>{let terrain=[],maps=[],wrong=[],root=pilot.root;const seen=new Set();root.traverse(o=>{if(!o.isMesh)return;let terrainNode=o;while(terrainNode&&!terrainNode.name.startsWith('Terrain'))terrainNode=terrainNode.parent;if(terrainNode){terrain.push(o.name);let ancestor=o;while(ancestor&&ancestor.name!=='Lid_Hinge')ancestor=ancestor.parent;if(!ancestor)wrong.push(o.name);}for(const tex of [o.material.map,o.material.roughnessMap]){if(!tex||seen.has(tex.uuid))continue;seen.add(tex.uuid);let im=tex.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0,sum=[0,0,0];for(let i=0;i<d.length;i+=4){mn=Math.min(mn,d[i+(tex===o.material.roughnessMap?1:0)]);mx=Math.max(mx,d[i+(tex===o.material.roughnessMap?1:0)]);for(let j=0;j<3;j++)sum[j]+=d[i+j];}maps.push({material:o.material.name,width:im.width,height:im.height,range:mx-mn,mean:sum.map(v=>v/(d.length/4))});}});return {terrain,maps,wrong}})()''')
 assert len(features['terrain'])>=1 and not features['wrong']
 assert len(features['maps'])>=3
 assert all(x['range']>30 and x['width']<=512 and x['height']<=512 for x in features['maps'])
 ochre=next(x for x in features['maps'] if x['material'].startswith('Ochre'))
 assert ochre['mean'][0]>ochre['mean'][1]>ochre['mean'][2]
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'mauritania-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True)
 c.close();b.close()
out={'status':'PASS','features':features,'noJS_poster':True};(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
