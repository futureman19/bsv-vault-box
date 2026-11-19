from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.getextrema()[3][1]>0;assert max(x[1] for x in im.getextrema()[:3])>30
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'tonga-v1.html').as_uri());p.wait_for_function('pilot.ready')
 maps=p.evaluate('''()=>{const out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(const [key,channel] of [['map',0],['roughnessMap',1]]){const t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}out.push({key,material:o.material.name,width:c.width,height:c.height,range:mx-mn});}});return out}''')
 assert len(maps)>=3 and all(m['range']>10 and max(m['width'],m['height'])<=512 for m in maps)
 assert 'Tonga / Ngatu & Ochre' in p.locator('body').inner_text()
 assert not any(s in p.locator('body').inner_text() for s in ['Japan','Yakushima','Mossed'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'tonga-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));c.close();b.close()
r={'status':'PASS','maps':maps,'no_js_poster':True,'source_poster_nonempty':True,'country_copy':True}
(R/'extended-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
