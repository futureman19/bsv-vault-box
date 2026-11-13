from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,:3].max(axis=2)>20).mean()>.1 and im[:,:,3].max()==255
out={'poster_nonblank':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'united-states-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['maps']=p.evaluate('''()=>{let seen=new Set(),maps=[];pilot.root.traverse(o=>{if(!o.isMesh)return;for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,c.width,c.height).data,lo=255,hi=0;for(let i=key==='roughnessMap'?1:0;i<a.length;i+=4){lo=Math.min(lo,a[i]);hi=Math.max(hi,a[i]);}maps.push({key,range:hi-lo,width:c.width,height:c.height});}});return maps}''')
 assert len(out['maps'])>=3 and all(m['range']>0 and max(m['width'],m['height'])<=1024 for m in out['maps'])
 out['ancestry']=p.evaluate('''()=>{let count=0,bad=[];pilot.root.traverse(o=>{if(o.name.startsWith('Canyon_rim')||o.name.startsWith('River_')){count++;let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)bad.push(o.name)}});return {count,bad}}''');assert out['ancestry']['count']>=7 and not out['ancestry']['bad']
 assert 'Japan' not in p.locator('body').inner_text() and 'Yakushima' not in p.locator('body').inner_text()
 p.emulate_media(reduced_motion='reduce');p.evaluate("window.samples=[];function sample(){samples.push(pilot.progress);if(samples.length<30)requestAnimationFrame(sample)};requestAnimationFrame(sample)");p.locator('#open').click();p.wait_for_function('samples.length===30');assert all(x in [0,1] for x in p.evaluate('samples'));out['reduced_motion_endpoints_only']=True;c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'united-states-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('e=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['PASS']=True;(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
