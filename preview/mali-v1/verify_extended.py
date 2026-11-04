from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
mean=np.array(Image.open(R/'maps/ochre-color.png')).mean(axis=(0,1));assert all(lo<v<hi for v,lo,hi in zip(mean,[130,75,35],[205,150,100]))
poster=np.array(Image.open(R/'poster.png').convert('RGB'));assert poster.std()>10 and (poster.max(axis=2)>20).mean()>.2
out={'palette_mean':mean.tolist(),'source_poster_variation':float(poster.std())}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'mali-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let terrain=0,maps=[],wrong=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Terrain')){terrain++;let p=o;while(p&&p.name!=='Lid_Hinge')p=p.parent;if(!p)wrong.push(o.name);}for(const [kind,tex,channel] of [['color',o.material.map,0],['roughness',o.material.roughnessMap,1]]){if(!tex||seen.has(tex.uuid+kind))continue;seen.add(tex.uuid+kind);let im=tex.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind,width:im.width,height:im.height,range:mx-mn});}});return{terrain,maps,wrong}})()''')
 assert out['features']['terrain']>=1 and not out['features']['wrong']
 assert len(out['features']['maps'])>=3 and all(x['range']>10 and max(x['width'],x['height'])<=512 for x in out['features']['maps'])
 text=p.locator('body').inner_text().lower();assert 'mali' in text and not any(x in text for x in ['japan','cedar','yakushima'])
 assert 'Mali' in p.locator('canvas').get_attribute('aria-label')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'mali-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
