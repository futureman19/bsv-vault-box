from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'liechtenstein-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Japan' not in p.locator('body').inner_text();assert 'Liechtenstein' in p.locator('canvas').get_attribute('aria-label')
 data=p.evaluate('''()=>{let maps=[],peaks=[],seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Three_Sisters')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;peaks.push({name:o.name,lid:!!a});}if(!o.isMesh)return;for(const slot of ['map','roughnessMap']){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let cx=c.getContext('2d');cx.drawImage(im,0,0);let d=cx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=slot==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({slot,width:c.width,height:c.height,range:mx-mn});}});return {maps,peaks}}''')
 assert len(data['peaks'])==3 and all(o['lid'] for o in data['peaks'])
 assert len(data['maps'])>=3 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in data['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'liechtenstein-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
data.update(status='PASS',noJS_poster=True,country_copy=True);(R/'extended-check.json').write_text(json.dumps(data,indent=2));print(json.dumps(data))
