from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.getchannel('A').getextrema()[1]==255;assert max(im.convert('RGB').getextrema()[0])>100
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True)
 c=b.new_context(java_script_enabled=False,offline=True,viewport={'width':390,'height':844});p=c.new_page();requests=[];p.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
 p.goto((R/'croatia-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(i)=>i.complete && i.naturalWidth>0');assert not requests;p.screenshot(path=str(R/'mobile-nojs.png'));c.close()
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'croatia-v1.html').as_uri());p.wait_for_function('window.pilot?.ready');text=p.locator('body').inner_text();assert 'Croatia / Plitvice Tufa' in text;assert not any(s in text for s in ['Japan','Yakushima','Cedar']);assert 'Croatia' in p.locator('canvas').get_attribute('aria-label')
 maps=p.evaluate('''async()=>{const out=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(const key of ['map','roughnessMap']){const t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);const im=t.image;const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const ctx=c.getContext('2d');ctx.drawImage(im,0,0);const a=ctx.getImageData(0,0,c.width,c.height).data;let lo=255,hi=0;for(let i=key==='roughnessMap'?1:0;i<a.length;i+=4){lo=Math.min(lo,a[i]);hi=Math.max(hi,a[i]);}out.push({key,width:c.width,height:c.height,range:hi-lo});}});return out;}''')
 assert len(maps)>=3 and all(m['range']>5 for m in maps)
 c.close();b.close()
r={'PASS':True,'no_js_poster':True,'poster_alpha_and_brightness':True,'country_copy':True,'decoded_texture_variation':maps};(R/'extended-check.json').write_text(json.dumps(r,indent=2));print('EXTENDED PASS',r)
