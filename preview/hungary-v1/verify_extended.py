from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageStat
import json
R=Path(__file__).resolve().parent
out={}
im=Image.open(R/'poster.png').convert('RGBA');assert max(ImageStat.Stat(im).mean[:3])>15;assert ImageStat.Stat(im).mean[3]>100
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'hungary-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['maps']=p.evaluate('''(()=>{let out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let kind of ['map','roughnessMap']){let t=o.material[kind];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=kind==='roughnessMap'?1:0;i<a.length;i+=4){mn=Math.min(mn,a[i]);mx=Math.max(mx,a[i]);}out.push({kind,width:c.width,height:c.height,range:mx-mn});}});return out})()''')
 assert len(out['maps'])>=3 and all(m['range']>10 and max(m['width'],m['height'])<=256 for m in out['maps'])
 text=p.locator('body').inner_text()+p.locator('canvas').get_attribute('aria-label');assert 'Hungary' in text and not any(w in text for w in ['Japan','Cedar','Yakushima','Moss'])
 out['copy_audit']=True;c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'hungary-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
