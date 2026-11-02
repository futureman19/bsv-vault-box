from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent;out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'morocco-atlas-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let tiles=0,ridges=0,maps=[],wrong=[],forbidden=[],root=pilot.root;const seen=new Set();root.traverse(o=>{if(!o.isMesh)return;if(/tree|moss|glacier|river|foliage|granite/i.test(o.name))forbidden.push(o.name);if(o.name.startsWith('Ceramic_tessera')||o.name.startsWith('Atlas_ridge')){if(o.name.startsWith('Ceramic'))tiles++;else ridges++;let q=o,ok=false;while(q){if(q.name==='Lid_Hinge')ok=true;q=q.parent;}if(!ok)wrong.push(o.name);}for(let key of ['map','roughnessMap']){let map=o.material[key];if(map&&!seen.has(map.uuid)){seen.add(map.uuid);let im=map.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,key,width:im.width,height:im.height,range:mx-mn});}}});return {tiles,ridges,maps,wrong,forbidden,latchParent:root.getObjectByName('Latch_Pivot').parent.name}})()''')
 assert out['features']['tiles']>=150 and out['features']['ridges']==1 and not out['features']['wrong'] and not out['features']['forbidden']
 assert out['features']['latchParent']=='Lid_Hinge'
 assert len(out['features']['maps'])>=4 and all(x['range']>10 and max(x['width'],x['height'])<=512 for x in out['features']['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();requests=[];p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None);p.goto((R/'morocco-atlas-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not requests;p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;out['noJS_external_requests']=requests;c.close();b.close()
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
