from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'kuwait-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let dunes=[],panels=[],maps=[],wrong=[],badUV=0;const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Dune')){dunes.push(o.name);if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}if(o.name.startsWith('Sadu'))panels.push(o.name);let uv=o.geometry.attributes.uv;if(uv)for(let i=0;i<uv.count;i++)if(!Number.isFinite(uv.getX(i))||!Number.isFinite(uv.getY(i)))badUV++;for(let field of ['map','roughnessMap']){let t=o.material[field];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=0;i<d.length;i+=4){mn=Math.min(mn,d[i+(field==='roughnessMap'?1:0)]);mx=Math.max(mx,d[i+(field==='roughnessMap'?1:0)]);}maps.push({field,material:o.material.name,width:im.width,height:im.height,range:mx-mn});}});return {dunes,panels,maps,wrong,badUV}})()''')
 f=out['features'];assert len(f['dunes'])==1 and len(f['panels'])==8 and not f['wrong'] and f['badUV']==0
 print(json.dumps(f));(R/'extended-check.json').write_text(json.dumps(out,indent=2))
 assert len(f['maps'])>=4 and all(x['range']>10 and max(x['width'],x['height'])<=512 for x in f['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'kuwait-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
