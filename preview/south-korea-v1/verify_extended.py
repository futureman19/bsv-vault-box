from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'south-korea-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Cedar' not in p.locator('canvas').get_attribute('aria-label')
 result=p.evaluate('''()=>{const maps=[];const seen=new Set();let flowers=0;pilot.root.traverse(o=>{if(o.name.startsWith('Pearl__lid_chrysanthemum')||o.name.startsWith('Pearl__lid'))flowers++;if(!o.isMesh)return;for(const [key,ch] of [['map',0],['roughnessMap',1]]){let t=o.material[key];if(!t||seen.has(t.uuid+ch))continue;seen.add(t.uuid+ch);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,key,range:mx-mn,width:c.width,height:c.height});}});return {maps,flowers}}''')
 assert len(result['maps'])>=3 and all(m['range']>0 and m['width']<=256 and m['height']<=256 for m in result['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'south-korea-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('e=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));result['no_js_poster']=True;b.close()
result['status']='PASS';(R/'extended-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
