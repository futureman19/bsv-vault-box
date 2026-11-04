from pathlib import Path
import json
from PIL import Image,ImageStat
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True)
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'eritrea-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Eritrea' in p.locator('canvas').get_attribute('aria-label')
 assert 'Japan' not in p.locator('body').inner_text()
 data=p.evaluate('''(()=>{let out=[];pilot.root.traverse(o=>{if(!o.isMesh||!o.material.roughnessMap||out.length)return;let im=o.material.roughnessMap.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,c.width,c.height).data,lo=255,hi=0;for(let i=1;i<a.length;i+=4){lo=Math.min(lo,a[i]);hi=Math.max(hi,a[i])}out.push({min:lo,max:hi,range:hi-lo,channel:'green'})});return out})()''')
 assert len(data)==1 and data[0]['range']>5
 b.close()
im=Image.open(R/'poster.png').convert('RGBA');assert im.size==(880,800)
assert ImageStat.Stat(im).mean[3]>200 and max(ImageStat.Stat(im.convert('RGB')).stddev)>20
r=dict(status='PASS',roughness=data,poster_size=im.size,poster_nonblank=True,country_copy=True)
(R/'material-check.json').write_text(json.dumps(r,indent=2));print('MATERIAL_POSTER_PASS',r)
