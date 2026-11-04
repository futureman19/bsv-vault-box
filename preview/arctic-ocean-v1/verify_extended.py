from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.getchannel('A').getbbox();assert max(im.convert('RGB').getextrema()[0])>80
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'arctic-ocean-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Yakushima' not in p.locator('body').inner_text() and 'Japan' not in p.locator('body').inner_text()
 maps=p.evaluate('''()=>{const out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(const key of ['map','roughnessMap','normalMap']){const t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);const im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;const ctx=c.getContext('2d');ctx.drawImage(im,0,0);const d=ctx.getImageData(0,0,c.width,c.height).data;let lo=255,hi=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}out.push({key,width:c.width,height:c.height,range:hi-lo});}});return out;}''')
 assert len(maps)==3 and all(m['range']>0 and m['width']==512 and m['height']==512 for m in maps),maps
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'arctic-ocean-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);b.close()
out=dict(status='PASS',maps=maps,poster_nonempty=True,noJS_poster=True,theme_copy=True)
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(out)
