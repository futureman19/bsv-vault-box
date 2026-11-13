from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.15 and im[:,:,:3].max()>100
out={'poster_nontransparent_fraction':float((im[:,:,3]>0).mean())}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'mexico-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Talavera & Agave' in text and not any(s in text for s in ['Japan','Yakushima','Cedar','Moss'])
 out['runtime']=p.evaluate('''(()=>{let maps=[],leaves=0,wrong=[];const seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Agave')){if(o.name.includes('leaf'))leaves++;let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}if(!o.isMesh)return;for(const [slot,channel] of [['map',0],['roughnessMap',1]]){const t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,slot,channel,width:im.width,height:im.height,range:mx-mn});}});return {maps,leaves,wrong}})()''')
 assert out['runtime']['leaves']==24 and not out['runtime']['wrong']
 assert len(out['runtime']['maps'])==3 and all(x['range']>5 and max(x['width'],x['height'])<=512 for x in out['runtime']['maps'])
 p.emulate_media(reduced_motion='reduce');p.evaluate('''window.samples=[];window.recording=true;function sample(){if(!recording)return;samples.push(pilot.progress);requestAnimationFrame(sample)}requestAnimationFrame(sample)''');p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.locator('#reset').click();p.wait_for_function('pilot.progress===0');out['reduced_motion_samples']=p.evaluate('recording=false;samples');assert set(out['reduced_motion_samples'])<={0,1}
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'mexico-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['nojs_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
