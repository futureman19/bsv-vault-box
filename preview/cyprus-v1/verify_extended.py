from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
out={}
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.9 and im[:,:,:3].max()>100
out['poster_nonempty']=True
color=np.array(Image.open(R/'maps/linen-color.png'));median=np.median(color,axis=(0,1));assert np.max(abs(median-[115,78,47]))<5;out['color_median']=median.tolist()
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'cyprus-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Cyprus / Lefkara Linen' in p.locator('h1').inner_text()
 assert 'Cyprus' in p.locator('canvas').get_attribute('aria-label')
 assert not any(w in p.locator('body').inner_text() for w in ['Japan','Yakushima','Mossed','cedar'])
 out['features']=p.evaluate('''(()=>{let diamonds=0,wrong=[],maps=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Cutwork_diamond')){diamonds++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name)}for(let key of ['map','roughnessMap','normalMap']){let t=o.material[key];if(!t||seen.has(key+t.uuid))continue;seen.add(key+t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0,channel=key==='roughnessMap'?1:0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind:key,width:c.width,height:c.height,range:mx-mn})}});return {diamonds,wrong,maps}})()''')
 assert out['features']['diamonds']==12 and not out['features']['wrong']
 assert {m['kind'] for m in out['features']['maps']}=={'map','roughnessMap','normalMap'}
 assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in out['features']['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'cyprus-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
