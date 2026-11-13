from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.1 and im[:,:,:3].max()>100
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'vietnam-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Japan' not in p.locator('body').inner_text();assert 'Vietnam' in p.locator('canvas').get_attribute('aria-label')
 features=p.evaluate('''(()=>{let islands=new Set(),wrong=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Karst_island')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);if(o.parent.name==='Lid_Hinge')islands.add(o.name)}if(!o.isMesh)return;for(let [key,ch] of [['map',0],['roughnessMap',1]]){let t=o.material[key];if(!t||seen.has(t.uuid+ch))continue;seen.add(t.uuid+ch);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i])}maps.push({key,channel:ch,width:c.width,height:c.height,range:mx-mn})}});return {islands:islands.size,wrong,maps}})()''')
 assert features['islands']==5 and not features['wrong'];assert len(features['maps'])>=3 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in features['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'vietnam-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
r={'status':'PASS','features':features,'poster_nonempty':True,'no_js_poster':True,'country_visible_and_accessible_copy':True};(R/'extended-check.json').write_text(json.dumps(r,indent=2));print('EXTENDED PASS',json.dumps(r))
