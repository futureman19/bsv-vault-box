from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'nepal-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Nepal' in p.locator('h1').inner_text()
 assert 'Nepal' in p.locator('canvas').get_attribute('aria-label')
 assert not any(w in p.locator('body').inner_text() for w in ['Japan','Yakushima','Cedar','Moss'])
 out['maps']=p.evaluate('''(()=>{const maps=[];let seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let kind of ['map','roughnessMap']){let t=o.material[kind];if(!t||seen.has(t.uuid+kind))continue;seen.add(t.uuid+kind);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=kind==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind,width:c.width,height:c.height,range:mx-mn});}});return maps})()''')
 assert len(out['maps'])>=3 and all(m['range']>0 and max(m['width'],m['height'])<=256 for m in out['maps'])
 out['copy_and_portable_maps']='PASS';c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'nepal-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));out['nojs_poster']='PASS';c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
