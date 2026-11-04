from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'togo-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Togo' in p.title() and 'Togo' in p.locator('canvas').get_attribute('aria-label')
 assert not any(s in p.locator('body').inner_text() for s in ['Japan','Yakushima','Cedar','Moss'])
 r=p.evaluate('''(()=>{let ornaments=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Compound')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;ornaments.push({name:o.name,lid:!!a});}for(const key of ['map','roughnessMap']){const t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);const im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;const ctx=c.getContext('2d');ctx.drawImage(im,0,0);const d=ctx.getImageData(0,0,c.width,c.height).data;let lo=255,hi=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}maps.push({key,width:c.width,height:c.height,range:hi-lo});}});return {ornaments,maps}})()''')
 assert len(r['ornaments'])==12 and all(o['lid'] for o in r['ornaments'])
 assert len(r['maps'])>=3 and all(m['range']>10 and max(m['width'],m['height'])<=512 for m in r['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'togo-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
r.update(status='PASS',no_js_poster=True,copy_and_accessibility=True)
(R/'extended-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
