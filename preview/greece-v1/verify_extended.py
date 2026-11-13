from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'greece-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Tinian Marble' in p.locator('h1').inner_text();assert 'Greece' in p.locator('canvas').get_attribute('aria-label')
 assert all(x not in p.locator('body').inner_text() for x in ['Japan','Yakushima','cedar','Moss'])
 maps=p.evaluate('''(()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let key of ['map','roughnessMap','normalMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,min=255,max=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){min=Math.min(min,d[i]);max=Math.max(max,d[i]);}out.push({key,width:im.width,height:im.height,range:max-min});}});return out})()''')
 assert len(maps)==3 and all(m['range']>0 and m['width']==512 and m['height']==512 for m in maps)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'greece-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);b.close()
im=Image.open(R/'poster.png').convert('RGB');assert max(im.getextrema()[0])-min(im.getextrema()[0])>80
out={'status':'PASS','decoded_maps':maps,'no_js_poster':True,'country_visible_and_accessible_copy':True,'source_poster_nonblack':True}
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
