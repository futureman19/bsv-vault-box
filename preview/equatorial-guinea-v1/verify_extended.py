from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'equatorial-guinea-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let canopies=0,terrain=0,maps=[],wrong=[],root=pilot.root;const seen=new Set();root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Canopy'))canopies++;if(o.name.startsWith('Terrain'))terrain++;if((o.name.startsWith('Canopy')||o.name.startsWith('Terrain'))&&o.parent.name!=='Lid_Hinge')wrong.push(o.name);for(const kind of ['map','roughnessMap','normalMap']){const tex=o.material[kind];if(!tex||seen.has(tex.uuid))continue;seen.add(tex.uuid);let im=tex.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;const channel=kind==='roughnessMap'?1:0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind,width:im.width,height:im.height,range:mx-mn});}});return {canopies,terrain,maps,wrong}})()''')
 f=out['features'];assert f['canopies']==72 and f['terrain']==1 and not f['wrong'];assert {m['kind'] for m in f['maps']}=={'map','roughnessMap','normalMap'}
 assert all(m['range']>0 and m['width']==512 and m['height']==256 for m in f['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'equatorial-guinea-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
