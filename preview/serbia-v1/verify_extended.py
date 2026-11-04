from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert np.mean(im[:,:,3]>0)> .25 and im[:,:,:3].max()>100
out={'poster_nonblank':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'serbia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Serbia' in p.locator('h1').inner_text();assert not any(x in p.locator('body').inner_text() for x in ['Japan','Yakushima','cedar','Mossed'])
 out['runtime']=p.evaluate('''(()=>{let relief=[],maps=[],bad=[];pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Pirot_relief')){relief.push(o.name);if(o.parent.name!=='Lid_Hinge')bad.push(o.name);}if(!o.material.name.startsWith('Pirot'))return;for(let key of ['map','roughnessMap','normalMap']){let tex=o.material[key];if(!tex||maps.some(x=>x.key===key))continue;let im=tex.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,lo=255,hi=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}maps.push({key,width:im.width,height:im.height,range:hi-lo});}});return {relief,maps,bad}})()''')
 r=out['runtime'];assert len(r['relief'])==6 and not r['bad'];assert len(r['maps'])==3 and all(x['range']>0 and max(x['width'],x['height'])<=512 for x in r['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'serbia-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
