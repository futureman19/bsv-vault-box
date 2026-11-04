from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'finland-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Finland' in p.locator('canvas').get_attribute('aria-label')
 assert not any(s in p.locator('body').inner_text() for s in ['Japan','Yakushima','Cedar'])
 r=p.evaluate('''(()=>{let maps=[],ornaments=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Lake_')||o.name.startsWith('Island_'))ornaments.push({name:o.name,parent:o.parent.name});for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mi=255,ma=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mi=Math.min(mi,d[i]);ma=Math.max(ma,d[i]);}maps.push({key,width:im.width,height:im.height,range:ma-mi});}});return {ornaments,maps}})()''')
 assert len(r['ornaments'])==4 and all(o['parent']=='Lid_Hinge' for o in r['ornaments'])
 assert len(r['maps'])>=5 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in r['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'finland-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
r.update(status='PASS',noJS_poster=True,country_copy=True)
(R/'extended-check.json').write_text(json.dumps(r,indent=2));print('EXTENDED PASS',r)
