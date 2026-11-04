from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files','--use-angle=d3d11','--enable-gpu'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'cabo-verde-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let terrain=[],maps=[],wrong=[],root=pilot.root;const seen=new Set();root.traverse(o=>{if(!o.isMesh)return;if(/^(Caldera|Fogo|Cultivation)_/.test(o.name)){terrain.push(o.name);let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}for(let channel of ['map','normalMap','roughnessMap']){let tx=o.material[channel];if(tx&&!seen.has(tx.uuid)){seen.add(tx.uuid);let im=tx.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=(channel==='roughnessMap'?1:0);i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({channel,material:o.material.name,width:im.width,height:im.height,range:mx-mn});}}});return {terrain,maps,wrong}})()''')
 assert any('cratered' in n for n in out['features']['terrain'])
 assert any('horseshoe' in n for n in out['features']['terrain'])
 assert len(out['features']['terrain'])>=17 and not out['features']['wrong']
 assert len(out['features']['maps'])>=3
 assert all(x['range']>0 and max(x['width'],x['height'])<=512 for x in out['features']['maps'])
 # Actual source terrain must remain present when viewed from rear, lid open.
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 p.locator('#reset').click();p.wait_for_function('pilot.progress===0');p.evaluate('''(()=>{pilot.camera.position.set(0,7,.001);pilot.camera.lookAt(0,1,0);pilot.camera.updateMatrixWorld()})()''');p.wait_for_timeout(100);p.screenshot(path=str(R/'terrain-top-view.png'),full_page=True)
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'cabo-verde-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS'
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out,indent=2))
