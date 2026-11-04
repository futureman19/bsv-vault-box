from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'switzerland-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Alpine Walnut & Matterhorn' in p.locator('h1').inner_text()
 assert 'Japan' not in p.locator('body').inner_text() and 'Yakushima' not in p.locator('body').inner_text()
 maps=p.evaluate('''()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(const key of ['map','roughnessMap','normalMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let x=c.getContext('2d');x.drawImage(im,0,0);let d=x.getImageData(0,0,c.width,c.height).data,lo=255,hi=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}out.push({key,width:c.width,height:c.height,range:hi-lo});}});return out}''')
 assert all(m['range']>0 and max(m['width'],m['height'])<=1024 for m in maps)
 assert {'map','normalMap','roughnessMap'}.issubset({m['key'] for m in maps})
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'switzerland-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));b.close()
out={'status':'PASS','decoded_maps':maps,'country_copy':True,'nojs_poster':True}
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(out)
