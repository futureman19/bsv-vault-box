from pathlib import Path
import json
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.getchannel('A').getextrema()[1]>0;assert max(im.convert('RGB').getextrema()[0])>40
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'nicaragua-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['maps']=p.evaluate('''(()=>{let maps=[];pilot.root.traverse(o=>{if(!o.isMesh)return;for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||maps.some(x=>x.id===t.uuid))continue;let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,c.width,c.height).data,min=255,max=0;for(let i=key==='roughnessMap'?1:0;i<a.length;i+=4){min=Math.min(min,a[i]);max=Math.max(max,a[i]);}maps.push({id:t.uuid,key,width:c.width,height:c.height,range:max-min});}});return maps})()''')
 assert len(out['maps'])>=3 and all(m['range']>0 and max(m['width'],m['height'])<=256 for m in out['maps'])
 text=p.locator('body').inner_text();assert 'Nicaragua' in text and 'Japan' not in text and 'Yakushima' not in text
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'nicaragua-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));c.close();b.close()
out.update(status='PASS',poster_pixels=True,noJS_poster=True,country_copy=True)
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS')
