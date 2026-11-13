from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'egypt-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let pyramids=0,terrain=0,maps=[],wrong=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Pyramid_')){pyramids++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}if(o.name.startsWith('Terrain_')){terrain++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}for(const key of ['map','roughnessMap']){const tex=o.material[key];if(tex&&!seen.has(tex.uuid)){seen.add(tex.uuid);let im=tex.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=0;i<d.length;i+=4){const channel=key==='roughnessMap'?1:0;mn=Math.min(mn,d[i+channel]);mx=Math.max(mx,d[i+channel]);}maps.push({material:o.material.name,key,width:im.width,height:im.height,range:mx-mn});}}});return {pyramids,terrain,maps,wrong}})()''')
 (R/'extended-measurements.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
 f=out['features'];assert f['pyramids']==3 and f['terrain']==1 and not f['wrong'];assert len(f['maps'])==3
 assert all(x['range']>10 and max(x['width'],x['height'])<=1024 for x in f['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'egypt-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out,indent=2))
