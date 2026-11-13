from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent;out={}
im=np.asarray(Image.open(R/'poster.png').convert('RGB'));assert im.max()-im.min()>40 and np.count_nonzero(im)>im.size*.1
out['source_poster_nonblank']=True
color=np.asarray(Image.open(R/'maps/stone-color.png'));med=np.median(color,axis=(0,1));assert np.max(np.abs(med-[74,80,69]))<5
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'sao-tome-and-principe-v1.html').as_uri());p.wait_for_function('pilot.ready',timeout=60000)
 out['features']=p.evaluate('''(()=>{let maps=[],wrong=[],terrain=0;const seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Terrain')){terrain++;let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}if(!o.isMesh)return;for(const [kind,t,channel] of [['color',o.material.map,0],['roughness',o.material.roughnessMap,1]]){if(!t||seen.has(t.uuid+kind))continue;seen.add(t.uuid+kind);let im=t.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind,material:o.material.name,width:im.width,height:im.height,range:mx-mn});}});return {terrain,maps,wrong}})()''')
 assert out['features']['terrain']>35 and not out['features']['wrong']
 assert len(out['features']['maps'])>=3
 assert all(x['range']>20 and max(x['width'],x['height'])<=512 for x in out['features']['maps'])
 body=p.locator('body').inner_text();assert 'Sao Tome' in body and not any(s in body for s in ['Japan','Yakushima','cedar'])
 assert 'Sao Tome' in p.locator('canvas').get_attribute('aria-label')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(250);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'sao-tome-and-principe-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
