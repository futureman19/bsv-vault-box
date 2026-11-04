from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGB');assert max(im.getextrema()[0])>100
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files']);c=b.new_context(offline=True);p=c.new_page();p.goto((R/'yemen-v1.html').as_uri());p.wait_for_function('pilot.ready')
 r=p.evaluate('''(()=>{let maps=[],wrong=[],towers=0;let seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Tower')){let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);if(o.name.startsWith('Tower__house'))towers++;}if(!o.isMesh)return;for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,width:c.width,height:c.height,range:mx-mn});}});return {maps,wrong,towers}})()''')
 assert not r['wrong'];assert len(r['maps'])>=3;assert all(m['range']>0 and max(m['width'],m['height'])<=256 for m in r['maps'])
 text=p.locator('body').inner_text();assert 'Yemen' in text and 'Yakushima' not in text and 'Japan' not in text
 assert 'Yemen' in p.locator('canvas').get_attribute('aria-label');c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'yemen-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));c.close();b.close()
r.update(status='PASS',nojs=True,poster_nonblack=True,country_copy=True)
(R/'extended-check.json').write_text(json.dumps(r,indent=2));print(r)
