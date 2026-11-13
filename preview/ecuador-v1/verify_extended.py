from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>128).mean()>.15;assert im[:,:,:3].max()>150
out={'poster_nonblank':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'ecuador-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Toquilla' in text and 'ECUADOR' in text;assert not any(s in text for s in ['Yakushima','JAPAN','cedar','Mossed'])
 result=p.evaluate('''(()=>{let islands=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Islet')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;islands.push({name:o.name,lid:!!a});}for(let slot of ['map','roughnessMap','normalMap']){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let x=c.getContext('2d');x.drawImage(im,0,0);let d=x.getImageData(0,0,c.width,c.height).data,lo=255,hi=0;for(let i=(slot==='roughnessMap'?1:0);i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}maps.push({slot,width:c.width,height:c.height,range:hi-lo});}});return {islands,maps}})()''')
 assert len(result['islands'])==3 and all(x['lid'] for x in result['islands'])
 assert len(result['maps'])>=4 and all(x['range']>0 and max(x['width'],x['height'])<=1024 for x in result['maps'])
 assert any(x['slot']=='roughnessMap' and x['range']>10 for x in result['maps'])
 out.update(result);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'ecuador-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
