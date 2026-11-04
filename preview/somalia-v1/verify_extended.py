from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
out={}
im=Image.open(R/'poster.png').convert('RGBA');assert im.width>=900
assert sum(1 for r,g,b,a in im.getdata() if max(r,g,b)>25 and a>0)>im.width*im.height*.1
out['source_poster_nonblank']=True
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'somalia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Somalia' in p.locator('canvas').get_attribute('aria-label')
 assert not any(s in p.locator('body').inner_text() for s in ['Japan','Yakushima','Cedar','Moss'])
 out['maps']=p.evaluate('''(()=>{let result=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let channel of ['map','roughnessMap']){let tex=o.material[channel];if(!tex||seen.has(tex.uuid+channel))continue;seen.add(tex.uuid+channel);let im=tex.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=channel==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}result.push({material:o.material.name,channel,width:c.width,height:c.height,range:mx-mn});}});return result})()''')
 assert len(out['maps'])>=3 and all(m['range']>10 and max(m['width'],m['height'])<=256 for m in out['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'somalia-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['no_js_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
