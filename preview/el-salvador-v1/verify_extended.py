from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert np.count_nonzero(im[:,:,3])>im.shape[0]*im.shape[1]*.1;assert im[:,:,:3].max()>60
color=np.asarray(Image.open(R/'maps/indigo-color.png').convert('RGB'))
def palette(a):assert a[:,:,2].mean()>1.5*a[:,:,0].mean()
palette(color)
try:palette(color[:,:,::-1]);raise RuntimeError('negative palette accepted')
except AssertionError:negative=True
out={'status':'PASS','poster_real_pixels':True,'palette_negative_control_rejected':negative}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'el-salvador-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'El Salvador' in text and all(s not in text for s in ['Japan','Yakushima','Cedar','Moss'])
 out['features']=p.evaluate('''(()=>{let terrain=[],maps=[],wrong=[],root=pilot.root;const seen=new Set();root.traverse(o=>{if(o.name.startsWith('Terrain')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);terrain.push(o.name);}if(!o.isMesh)return;for(const [slot,ch] of [['map',0],['roughnessMap',1]]){const t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,slot,channel:ch,width:im.width,height:im.height,range:mx-mn});}});return {terrain,maps,wrong}})()''')
 assert len(out['features']['terrain'])>=2 and not out['features']['wrong']
 assert len(out['features']['maps'])>=3
 assert all(x['range']>10 and max(x['width'],x['height'])<=256 for x in out['features']['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'el-salvador-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
