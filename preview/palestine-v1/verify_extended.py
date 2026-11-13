from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'palestine-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Yakushima' not in p.locator('body').inner_text() and 'JAPAN' not in p.locator('body').inner_text()
 assert 'Crimson Stitch' in p.locator('canvas').get_attribute('aria-label')
 data=p.evaluate('''()=>{let threads=0,wrong=[],maps=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Stitch')){threads++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}for(let key of ['map','roughnessMap']){let tex=o.material[key];if(!tex||seen.has(tex.uuid))continue;seen.add(tex.uuid);let im=tex.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<a.length;i+=4){mn=Math.min(mn,a[i]);mx=Math.max(mx,a[i]);}maps.push({key,width:c.width,height:c.height,range:mx-mn});}});return {threads,wrong,maps}}''')
 assert data['threads']==96 and not data['wrong']
 assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in data['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'palestine-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));b.close()
(R/'extended-check.json').write_text(json.dumps({'status':'PASS','runtime':data,'noJS_poster':True,'copy_audit':True},indent=2));print('EXTENDED PASS')
