from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>128).mean()>.15 and im[:,:,:3].max()>100
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'australia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Australia / Bungle Bungle' in text and not any(w in text for w in ['Japan','Yakushima','cedar','Moss'])
 result=p.evaluate('''(()=>{let domes=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Dome'))domes.push({name:o.name,parent:o.parent.name});for(const [slot,ch] of [['map',0],['roughnessMap',1],['normalMap',0]]){const tex=o.material[slot];if(!tex||seen.has(slot+tex.uuid))continue;seen.add(slot+tex.uuid);let im=tex.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,lo=255,hi=0;for(let i=ch;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}maps.push({slot,channel:ch,width:im.width,height:im.height,range:hi-lo});}});return {domes,maps}})()''')
 assert len(result['domes'])==5 and all(d['parent']=='Lid_Hinge' for d in result['domes'])
 assert len(result['maps'])==3 and all(m['range']>10 and m['width']==512 and m['height']==512 for m in result['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'australia-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
result.update(status='PASS',source_poster_pixels=True,noJS_poster=True,visible_copy_correct=True)
(R/'extended-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
