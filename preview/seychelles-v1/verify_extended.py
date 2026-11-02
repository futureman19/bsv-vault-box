from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'seychelles-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out=p.evaluate('''(()=>{let terrain=[],maps=[],badUV=0;const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Terrain'))terrain.push({name:o.name,parent:o.parent.name});const uv=o.geometry.attributes.uv;if(uv)for(let i=0;i<uv.count;i++)if(!Number.isFinite(uv.getX(i))||!Number.isFinite(uv.getY(i)))badUV++;for(const slot of ['map','normalMap','roughnessMap']){const t=o.material[slot];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);const im=t.image,can=document.createElement('canvas');can.width=im.width;can.height=im.height;const ctx=can.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;let channel=slot==='roughnessMap'?1:0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({slot,width:im.width,height:im.height,range:mx-mn});}});return {terrain,maps,badUV};})()''')
 assert len(out['terrain'])==5 and all(t['parent']=='Lid_Hinge' for t in out['terrain'])
 assert sum('boulder' in t['name'] for t in out['terrain'])==3
 assert out['badUV']==0 and {m['slot'] for m in out['maps']}=={'map','normalMap','roughnessMap'}
 assert all(m['range']>0 and m['width']<=512 and m['height']<=512 for m in out['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'seychelles-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
