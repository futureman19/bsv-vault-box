from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'pakistan-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Pakistan / Multan Blue' in p.locator('body').inner_text()
 assert 'Pakistan' in p.locator('canvas').get_attribute('aria-label')
 data=p.evaluate('''(()=>{let ornaments=0,wrong=[],maps=[];let seen=new Set;pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Rosette')){ornaments++;let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}for(let [key,channel] of [['map',0],['roughnessMap',1]]){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,width:c.width,height:c.height,range:mx-mn});}});return {ornaments,wrong,maps};})()''')
 assert data['ornaments']==27 and not data['wrong']
 assert len(data['maps'])>=4 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in data['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'pakistan-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
 data.update(status='PASS',no_js_poster=True,copy_accessibility=True)
(R/'extended-check.json').write_text(json.dumps(data,indent=2));print(json.dumps(data))
