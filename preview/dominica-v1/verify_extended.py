from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGB');a=np.array(im);assert im.width>=800 and a.std()>15 and (a>50).mean()>.15
out={'poster_dimensions':im.size,'poster_nonblack_fraction':float((a>50).mean())}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'dominica-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Dominica' in text and not any(s in text for s in ['Japan','Yakushima','Cedar','Mossed granite'])
 out['features']=p.evaluate('''(()=>{let terrain=[],maps=[],wrong=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Rainforest')||o.name.startsWith('Lake')){terrain.push(o.name);let p=o.parent;while(p&&p.name!=='Lid_Hinge')p=p.parent;if(!p)wrong.push(o.name);}for(const [kind,t,ch] of [['color',o.material.map,0],['roughness',o.material.roughnessMap,1]]){if(!t||seen.has(t.uuid+kind))continue;seen.add(t.uuid+kind);let im=t.image,can=document.createElement('canvas');can.width=im.width;can.height=im.height;let ctx=can.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind,width:im.width,height:im.height,range:mx-mn});}});return {terrain_count:terrain.length,maps,wrong}})()''')
 assert out['features']['terrain_count']>72 and not out['features']['wrong']
 assert len(out['features']['maps'])>=3 and all(m['range']>15 and max(m['width'],m['height'])<=256 for m in out['features']['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'dominica-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
