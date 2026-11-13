from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.1 and im[:,:,:3].max()>80
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'atlantic-ocean-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Yakushima' not in p.locator('body').inner_text() and 'Japan' not in p.locator('body').inner_text()
 out['maps']=p.evaluate('''(()=>{let out=[];pilot.root.traverse(o=>{if(!o.isMesh||!o.material.name.startsWith('Abyss'))return;for(let [key,ch] of [['map',0],['roughnessMap',1],['normalMap',0]]){let t=o.material[key];if(!t||out.some(x=>x.kind===key))continue;let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0,blue=0,red=0;for(let i=0;i<d.length;i+=4){mn=Math.min(mn,d[i+ch]);mx=Math.max(mx,d[i+ch]);red+=d[i];blue+=d[i+2]}out.push({kind:key,range:mx-mn,width:c.width,height:c.height,blueGreaterRed:blue>red})}});return out})()''')
 assert len(out['maps'])==3
 for t in out['maps']:assert t['range']>0 and t['width']==256 and t['height']==256
 assert next(t for t in out['maps'] if t['kind']=='map')['blueGreaterRed']
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'atlantic-ocean-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
out.update(status='PASS',source_poster_nonempty=True,no_js_poster=True,no_inherited_country_copy=True)
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
