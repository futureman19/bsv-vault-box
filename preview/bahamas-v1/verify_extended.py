from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'bahamas-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let banks=0,holes=0,maps=[],wrong=[],root=pilot.root;const seen=new Set();root.traverse(o=>{if(!o.isMesh)return;if(/^(Pink_shore|Blue_hole|Lagoon)/.test(o.name)){if(o.name.startsWith('Pink_shore'))banks++;if(o.name.startsWith('Blue_hole'))holes++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}for(const [slot,ch] of [['map',0],['roughnessMap',1]]){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,slot,channel:ch,width:im.width,height:im.height,range:mx-mn});}});return {banks,holes,maps,wrong}})()''')
 assert out['features']['banks']==2 and out['features']['holes']==2 and not out['features']['wrong']
 assert len(out['features']['maps'])>=3 and all(x['range']>15 and max(x['width'],x['height'])<=256 for x in out['features']['maps'])
 text=p.locator('body').inner_text();assert 'Bahamas / Pink Sands & Blue Hole' in text and not any(s in text for s in ['Japan','Yakushima','cedar','Mossed'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'bahamas-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS'
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
