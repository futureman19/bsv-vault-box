from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
out={}
im=np.array(Image.open(R/'poster.png').convert('RGB'));assert im.max()>150 and (im.max(axis=2)>25).mean()>.25
out['poster_nonblack_fraction']=float((im.max(axis=2)>25).mean())
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'vanuatu-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Vanuatu / Ash & Ember' in p.locator('h1').inner_text()
 assert not any(w in p.locator('body').inner_text() for w in ['Japan','Yakushima','Cedar','Moss'])
 out['features']=p.evaluate('''(()=>{let terrain=[],maps=[],wrong=[],root=pilot.root;const seen=new Set();root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Terrain')){terrain.push(o.name);let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}for(let key of ['map','roughnessMap','normalMap']){let tex=o.material[key];if(!tex||seen.has(tex.uuid+key))continue;seen.add(tex.uuid+key);let im=tex.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0,ch=key==='roughnessMap'?1:0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind:key,material:o.material.name,width:im.width,height:im.height,range:mx-mn});}});return {terrain,maps,wrong}})()''')
 assert len(out['features']['terrain'])==2 and not out['features']['wrong']
 assert len(out['features']['maps'])==3
 assert all(x['range']>0 and max(x['width'],x['height'])<=512 for x in out['features']['maps'])
 out['warm_emission']=p.evaluate("(()=>{let e;pilot.root.traverse(o=>{if(o.isMesh&&o.name.includes('Ember'))e=o.material.emissive.toArray()});return e})()")
 assert out['warm_emission'][0]>out['warm_emission'][1]*3 and out['warm_emission'][1]>out['warm_emission'][2]*3
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'vanuatu-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS'
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
