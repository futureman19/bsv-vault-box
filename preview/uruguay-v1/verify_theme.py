from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.1 and im[:,:,:3].max()>40
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'uruguay-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Uruguay / Quebrada & Grassland' in p.locator('body').inner_text()
 assert not any(s in p.locator('body').inner_text() for s in ['Japan','Yakushima','Cedar'])
 out=p.evaluate('''(()=>{let terrain=[],maps=[],wrong=[],seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Terrain')){terrain.push(o.name);let a=o,ok=false;while(a){if(a.name==='Lid_Hinge')ok=true;a=a.parent;}if(!ok)wrong.push(o.name);}if(!o.isMesh)return;for(const [kind,tex,channel] of [['color',o.material.map,0],['roughness',o.material.roughnessMap,1]]){if(!tex||seen.has(tex.uuid+kind))continue;seen.add(tex.uuid+kind);let im=tex.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind,channel,range:mx-mn,width:c.width,height:c.height});}});return{terrain,maps,wrong}})()''')
 (R/'theme-runtime-probe.json').write_text(json.dumps(out,indent=2))
 assert len(out['terrain'])>=21 and not out['wrong']
 assert len(out['maps'])>=3 and any(m['kind']=='roughness' for m in out['maps'])
 assert all(m['range']>20 and max(m['width'],m['height'])<=256 for m in out['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'uruguay-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
out.update(status='PASS',noJS_poster=True,source_poster_nonblank=True,visible_copy=True)
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print('THEME RUNTIME PASS',json.dumps(out))
