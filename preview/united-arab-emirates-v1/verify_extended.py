from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);page=c.new_page();page.goto((R/'united-arab-emirates-v1.html').as_uri());page.wait_for_function('pilot.ready')
 assert 'Cedar' not in page.locator('canvas').get_attribute('aria-label'),'Inherited cedar accessibility copy'
 r=page.evaluate('''(()=>{let count=0,maps=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Loom__diamond')||o.name.includes('diamond')){count++;let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)throw Error('Detached diamond');}for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,key,range:mx-mn});}});return {count,maps}})()''')
 assert r['count']==28
 assert any(x['key']=='map' and x['range']>100 for x in r['maps'])
 assert any(x['key']=='roughnessMap' and x['range']>0 for x in r['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});page=c.new_page();page.goto((R/'united-arab-emirates-v1.html').as_uri());assert page.locator('#fallback').is_visible();assert page.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');page.screenshot(path=str(R/'mobile-nojs.png'));b.close()
r.update(status='PASS',noJS_poster=True,accessibility_copy=True)
(R/'extended-check.json').write_text(json.dumps(r,indent=2));print(r)
