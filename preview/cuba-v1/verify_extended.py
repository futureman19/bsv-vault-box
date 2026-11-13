from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.getchannel('A').getextrema()[1]>0;assert max(im.convert('RGB').getextrema()[0])>50
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'cuba-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Yakushima' not in p.locator('body').inner_text() and 'Japan' not in p.locator('body').inner_text()
 data=p.evaluate('''(()=>{let hills=new Set(),wrong=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Mogote')){let a=o;while(a&&!a.name.startsWith('Lid_Hinge'))a=a.parent;if(!a)wrong.push(o.name);if(o.parent.name==='Lid_Hinge')hills.add(o.name)}if(!o.isMesh)return;for(let kind of ['map','roughnessMap']){let t=o.material[kind];if(!t||seen.has(t.uuid+kind))continue;seen.add(t.uuid+kind);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,lo=255,hi=0;for(let i=kind==='roughnessMap'?1:0;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i])}maps.push({kind,width:c.width,height:c.height,range:hi-lo})}});return {hills:[...hills],wrong,maps}})()''')
 assert len(data['hills'])==3 and not data['wrong'];assert len(data['maps'])>=3
 assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in data['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(300);p.screenshot(path=str(R/'desktop-open-rear.png'));c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'cuba-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));c.close();b.close()
data.update(status='PASS',poster_nonempty=True,noJS=True);(R/'extended-check.json').write_text(json.dumps(data,indent=2));print(json.dumps(data))
