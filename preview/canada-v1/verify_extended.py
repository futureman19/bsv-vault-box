from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
out={}
a=np.asarray(Image.open(R/'poster.png').convert('RGBA'))
assert (a[:,:,3]>0).mean()>.2 and a[:,:,:3].max()>100
out['poster_nonblack_alpha']=True
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'canada-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Canada / Maple & Shield' in text and not any(x in text.lower() for x in ['japan','yakushima','cedar','iceland'])
 out['visible_country_copy']=True
 out['features']=p.evaluate('''(()=>{let ornaments=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(/^(Pine_|Shield_)/.test(o.name)){let q=o.parent;while(q&&q.name!=='Lid_Hinge')q=q.parent;ornaments.push({name:o.name,lidOwned:!!q});}for(const slot of ['map','roughnessMap']){let tex=o.material[slot];if(!tex||seen.has(tex.uuid+slot))continue;seen.add(tex.uuid+slot);let im=tex.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,channel=slot==='roughnessMap'?1:0,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,slot,channel,width:c.width,height:c.height,range:mx-mn});}});return {ornaments,maps}})()''')
 assert len(out['features']['ornaments'])==34 and all(o['lidOwned'] for o in out['features']['ornaments'])
 assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in out['features']['maps'])
 assert any(m['slot']=='roughnessMap' and m['range']>10 for m in out['features']['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(300);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'canada-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS'
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
