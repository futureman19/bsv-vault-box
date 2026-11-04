from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.getextrema()[3][1]>0 and max(im.convert('RGB').getextrema()[0])>50
out={'poster_actual_render_nonempty':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'samoa-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Samoa / Siapo & Lava' in text and all(s not in text for s in ['Japan','Yakushima','Cedar','Moss'])
 out['features']=p.evaluate('''(()=>{let ornaments=[],maps=[],wrong=[],root=pilot.root;const seen=new Set();root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Siapo__lid')||o.name.startsWith('Lava__lid')){ornaments.push(o.name);let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}for(const [type,channel] of [['map',0],['roughnessMap',1]]){let tex=o.material[type];if(!tex||seen.has(tex.uuid+type))continue;seen.add(tex.uuid+type);let im=tex.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,type,channel,width:im.width,height:im.height,range:mx-mn});}});return {ornaments,maps,wrong}})()''')
 # GLTFLoader sanitizes slash/space: inspect based on semantic fragments, not source count equality.
 names=p.evaluate("(()=>{let a=[];pilot.root.traverse(o=>{if(o.isMesh)a.push(o.name)});return a})()")
 out['mesh_names']=names
 assert len(out['features']['ornaments'])==4 and not out['features']['wrong'],out['features']
 assert len(out['features']['maps'])==4
 assert all(x['range']>15 and max(x['width'],x['height'])<=512 for x in out['features']['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.locator('#reset').click();p.wait_for_function('pilot.progress===0')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'samoa-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
