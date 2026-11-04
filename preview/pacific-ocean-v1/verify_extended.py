from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'pacific-ocean-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Pacific Ocean / Abyss & Atoll' in p.locator('h1').inner_text()
 assert not any(s in p.locator('body').inner_text() for s in ['Japan','Cedar','Yakushima','Mossed'])
 out=p.evaluate('''(()=>{let maps=[],ornaments=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Atoll')||o.name.startsWith('Seamount')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;ornaments.push({name:o.name,lid:!!a});}for(let [slot,ch] of [['map',0],['roughnessMap',1]]){let tex=o.material[slot];if(!tex||seen.has(tex.uuid+ch))continue;seen.add(tex.uuid+ch);let im=tex.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,slot,channel:ch,width:im.width,height:im.height,range:mx-mn});}});return {maps,ornaments}})()''')
 assert len(out['ornaments'])==3 and all(x['lid'] for x in out['ornaments'])
 assert len(out['maps'])>=3 and all(x['range']>10 and max(x['width'],x['height'])<=512 for x in out['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'pacific-ocean-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
