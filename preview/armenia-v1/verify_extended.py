from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
out={}
im=Image.open(R/'poster.png').convert('RGBA');assert im.getextrema()[3][1]>0 and max(im.convert('RGB').getextrema()[0])>30
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'armenia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let arches=0,piers=0,maps=[],wrong=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Arcade')){if(o.name.includes('arch'))arches++;if(o.name.includes('pier'))piers++;let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}for(let [kind,tex,channel] of [['color',o.material.map,0],['roughness',o.material.roughnessMap,1]]){if(!tex||seen.has(tex.uuid))continue;seen.add(tex.uuid);let im=tex.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind,width:im.width,height:im.height,range:mx-mn});}});return {arches,piers,maps,wrong}})()''')
 f=out['features'];assert f['arches']==3 and f['piers']==6 and not f['wrong'];assert len(f['maps'])>=3 and all(x['range']>0 and max(x['width'],x['height'])<=256 for x in f['maps'])
 text=p.locator('body').inner_text();assert 'Armenia / Rose Tuff Arcade' in text and not any(x in text for x in ['Japan','Yakushima','Cedar','Moss'])
 assert 'Armenia' in p.locator('canvas').get_attribute('aria-label')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'armenia-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';out['poster_nonempty']=True;out['copy_and_aria_country']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
