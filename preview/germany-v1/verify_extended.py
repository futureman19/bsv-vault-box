from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
out={}
a=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (a[:,:,3]>0).mean()>.9 and a[:,:,:3].max()>100
color=np.array(Image.open(R/'maps/wood-color.png'));mean=color.mean(axis=(0,1));assert mean[0]>mean[1]>mean[2] and mean[0]>140
out['poster_real_pixels']=True;out['wood_mean_RGB']=mean.tolist()
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'germany-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Germany' in p.locator('canvas').get_attribute('aria-label')
 assert not any(word in p.locator('body').inner_text() for word in ['Japan','Yakushima','Cedar','Moss'])
 out['runtime']=p.evaluate('''(()=>{let trees=0,houses=0,roofs=0,wrong=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Village')){let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);if(o.name.includes('turned_tree'))trees++;if(o.name.includes('house'))houses++;if(o.name.includes('roof'))roofs++;}for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let data=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0,ch=key==='roughnessMap'?1:0;for(let i=ch;i<data.length;i+=4){mn=Math.min(mn,data[i]);mx=Math.max(mx,data[i]);}maps.push({material:o.material.name,kind:key,range:mx-mn,width:im.width,height:im.height});}});return {trees,houses,roofs,wrong,maps}})()''')
 r=out['runtime'];assert (r['trees'],r['houses'],r['roofs'])==(3,2,2) and not r['wrong'];assert len(r['maps'])>=3
 assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in r['maps'])
 p.emulate_media(reduced_motion='reduce')
 p.evaluate('''window.progressSamples=[];window.probe=true;function sampleProgress(){if(window.probe){progressSamples.push(pilot.progress);requestAnimationFrame(sampleProgress)}}requestAnimationFrame(sampleProgress)''')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.locator('#reset').click();p.wait_for_function('pilot.progress===0');p.evaluate('window.probe=false')
 vals=p.evaluate('progressSamples');assert vals and all(v in (0,1) for v in vals);out['reduced_motion_frame_samples']=sorted(set(vals))
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'germany-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
