from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent;out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'bosnia-and-herzegovina-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Bosnia and Herzegovina' in p.locator('canvas').get_attribute('aria-label')
 assert not any(s in p.locator('body').inner_text() for s in ['Japan','Yakushima','cedar','Mossed'])
 out['features']=p.evaluate('''(()=>{const petals=[],wrong=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Ornament')||o.name.startsWith('Border')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);if(o.name.startsWith('Ornament__petal')||o.name.includes('petal'))petals.push(o.name);}for(const [type,channel] of [['map',0],['roughnessMap',1],['normalMap',0]]){let t=o.material[type];if(!t||seen.has(t.uuid+type))continue;seen.add(t.uuid+type);let im=t.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({type,channel,width:im.width,height:im.height,range:mx-mn});}});return {petals,wrong,maps}})()''')
 assert len(out['features']['petals'])==8 and not out['features']['wrong']
 assert len(out['features']['maps'])==3
 assert all(m['range']>0 and m['width']==256 and m['height']==256 for m in out['features']['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'bosnia-and-herzegovina-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
