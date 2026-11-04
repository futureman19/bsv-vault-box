from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGB');assert max(im.getextrema()[0])>100
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'san-marino-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Yakushima' not in p.locator('body').inner_text() and 'Japan' not in p.locator('body').inner_text()
 maps=p.evaluate('''()=>{const out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(const [slot,ch] of [['map',0],['normalMap',0],['roughnessMap',1]]){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}out.push({slot,width:c.width,height:c.height,range:mx-mn});}});return out;}''')
 assert len(maps)>=3 and all(m['range']>0 and max(m['width'],m['height'])<=1024 for m in maps)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'san-marino-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
r={'status':'PASS','actual_loader_maps':maps,'noJS_poster':True,'country_copy':True,'source_poster_nonblack':True}
(R/'extended-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
