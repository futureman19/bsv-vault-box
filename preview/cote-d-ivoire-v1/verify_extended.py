from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGB'));assert np.mean(im)>10 and np.std(im)>15
out={'poster_nonblack':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'cote-d-ivoire-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert not any(w in p.locator('body').inner_text().lower() for w in ['yakushima','japan','mossed'])
 assert 'Indigo Stripweave' in p.locator('canvas').get_attribute('aria-label')
 out['runtime']=p.evaluate('''(()=>{let strips=0,joins=0,wrong=[],maps=[];let seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Textile_lid_strip')){strips++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name)}if(o.name.startsWith('Textile_raised_join'))joins++;if(!o.isMesh)return;for(let key of ['map','roughnessMap']){let tex=o.material[key];if(!tex||seen.has(tex.uuid+key))continue;seen.add(tex.uuid+key);let im=tex.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i])}maps.push({key,range:mx-mn,width:im.width})}});return {strips,joins,wrong,maps}})()''')
 assert out['runtime']['strips']==9 and out['runtime']['joins']==8 and not out['runtime']['wrong']
 assert all(x['range']>0 and x['width']<=256 for x in out['runtime']['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'cote-d-ivoire-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
