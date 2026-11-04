from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.asarray(Image.open(R/'poster.png').convert('RGBA'))
assert (im[:,:,:3].max(axis=2)>25).mean()>.15 and (im[:,:,3]>0).mean()>.2
out={'source_poster_nonblank':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'trinidad-and-tobago-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Scarlet Rhythm' in text and 'Yakushima' not in text and 'Japan' not in text
 out['maps']=p.evaluate('''()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,min=255,max=0,r=0,g=0,b=0,channel=key==='roughnessMap'?1:0;for(let i=0;i<d.length;i+=4){min=Math.min(min,d[i+channel]);max=Math.max(max,d[i+channel]);r+=d[i];g+=d[i+1];b+=d[i+2];}out.push({name:o.material.name,key,width:c.width,height:c.height,range:max-min,redDominant:r>2*g&&r>2*b});}});return out}''')
 assert len(out['maps'])==3 and all(v['range']>0 and max(v['width'],v['height'])<=256 for v in out['maps'])
 assert any(v['key']=='map' and v['redDominant'] for v in out['maps'])
 out['ancestry']=p.evaluate('''()=>{let pans=[],bad=[];pilot.root.traverse(o=>{if(o.isMesh&&o.name.startsWith('Pan_')){pans.push(o.name);let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)bad.push(o.name)}});return {count:pans.length,bad}}''')
 assert out['ancestry']['count']==28 and not out['ancestry']['bad']
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'trinidad-and-tobago-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['no_js_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
