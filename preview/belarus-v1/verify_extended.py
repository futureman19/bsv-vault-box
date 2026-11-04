from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'belarus-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let warp=0,weft=0,maps=[],wrong=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Weave')){if(o.name.includes('warp'))warp++;if(o.name.includes('weft'))weft++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}for(const key of ['map','roughnessMap']){const tex=o.material[key];if(!tex||seen.has(tex.uuid))continue;seen.add(tex.uuid);let im=tex.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,material:o.material.name,width:im.width,height:im.height,range:mx-mn});}});return {warp,weft,maps,wrong}})()''')
 f=out['features'];assert f['warp']==21 and f['weft']==13 and not f['wrong'];assert len(f['maps'])>=3 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in f['maps'])
 text=p.locator('body').inner_text();assert 'Belarus / Golden Straw' in text and not any(s in text for s in ['Japan','Yakushima','Cedar & Moss'])
 assert 'Belarus' in p.locator('canvas').get_attribute('aria-label')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'belarus-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
