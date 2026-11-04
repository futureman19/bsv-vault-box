from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
out={}
im=Image.open(R/'poster.png').convert('RGBA');pixels=list(im.getdata());assert sum(p[3]>0 and max(p[:3])>25 for p in pixels)>len(pixels)*.05
out['source_poster_nonblank']=True
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'jamaica-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Jamaica / Blue & John Crow' in p.locator('body').inner_text()
 assert all(x not in p.locator('body').inner_text() for x in ['Japan','Yakushima','cedar'])
 out['features']=p.evaluate('''(()=>{let terrain=0,maps=[],wrong=[],root=pilot.root;const seen=new Set();root.traverse(o=>{if(o.name.startsWith('Terrain')){terrain++;let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}if(!o.isMesh)return;for(let key of ['map','roughnessMap']){let tex=o.material[key];if(!tex||seen.has(tex.uuid+key))continue;seen.add(tex.uuid+key);let im=tex.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,channel:key==='roughnessMap'?'green':'red',width:im.width,height:im.height,range:mx-mn});}});return {terrain,maps,wrong}})()''')
 assert out['features']['terrain']>=51 and not out['features']['wrong']
 assert len(out['features']['maps'])>=3 and all(x['range']>10 and max(x['width'],x['height'])<=512 for x in out['features']['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'jamaica-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
