from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'oman-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Oman' in p.title() and 'Oman' in p.locator('canvas').get_attribute('aria-label')
 assert not any(w in p.locator('body').inner_text() for w in ['Japan','Cedar','Yakushima'])
 result=p.evaluate('''(()=>{let maps=[],seen=new Set(),ornaments=[];pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Terrace')||o.name.startsWith('Falaj'))ornaments.push({name:o.name,parent:o.parent.name});for(let slot of ['map','roughnessMap']){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=slot==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({slot,range:mx-mn,width:c.width,height:c.height});}});return {maps,ornaments}})()''')
 assert len(result['ornaments'])==15 and all(o['parent']=='Lid_Hinge' for o in result['ornaments'])
 assert len(result['maps'])>=3 and all(m['range']>10 and max(m['width'],m['height'])<=256 for m in result['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'oman-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));c.close();b.close()
result.update(status='PASS',nojs_poster=True,copy_accessibility=True)
(R/'extended-check.json').write_text(json.dumps(result,indent=2));print('PASS runtime theme, decoded maps, no-JS poster, copy/accessibility')
