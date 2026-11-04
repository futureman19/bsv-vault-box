from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'botswana-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let channels=0,islands=0,reeds=0,coils=0,maps=[],wrong=[],legacy=[],root=pilot.root;const seen=new Set();root.traverse(o=>{if(!o.isMesh)return;if(/Cedar|Granite|Moss/.test(o.name))legacy.push(o.name);if(o.name.startsWith('Delta')){if(o.name.includes('channel'))channels++;if(o.name.includes('island'))islands++;if(o.name.startsWith('Delta__reed')&&!o.name.includes('island'))reeds++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}if(o.name.startsWith('Coil'))coils++;for(let field of ['map','normalMap','roughnessMap']){let map=o.material[field];if(map&&!seen.has(map.uuid)){seen.add(map.uuid);let im=map.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=0;i<d.length;i+=4){const channel=field==='roughnessMap'?1:0;mn=Math.min(mn,d[i+channel]);mx=Math.max(mx,d[i+channel]);}maps.push({material:o.material.name,field,width:im.width,height:im.height,range:mx-mn});}}});return {channels,islands,reeds,coils,maps,wrong,legacy}})()''')
 f=out['features'];assert f['channels']==5 and f['islands']==8 and f['coils']==96 and not f['wrong'] and not f['legacy'],f
 assert len(f['maps'])>=3 and all(x['range']>0 and max(x['width'],x['height'])<=1024 for x in f['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'botswana-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS'
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
