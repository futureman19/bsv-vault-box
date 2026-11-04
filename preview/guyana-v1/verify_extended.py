from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageStat
import json
R=Path(__file__).resolve().parent;out={}
im=Image.open(R/'poster.png').convert('RGB');st=ImageStat.Stat(im);assert max(st.stddev)>15 and max(st.mean)>10;out['poster_nonblank']={'size':im.size,'mean':st.mean,'stddev':st.stddev}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'guyana-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Guyana' in text and 'Japan' not in text and 'Yakushima' not in text
 out['maps']=p.evaluate('''()=>{let out=[];let seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let key of ['map','roughnessMap','normalMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data;let lo=255,hi=0,ch=key==='roughnessMap'?1:0;for(let i=ch;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}out.push({key,width:im.width,height:im.height,range:hi-lo,channel:ch});}});return out;}''')
 assert {m['key'] for m in out['maps']}=={'map','roughnessMap','normalMap'}
 assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in out['maps'])
 out['theme_ancestry']=p.evaluate('''()=>{let found=0,bad=[];pilot.root.traverse(o=>{if(!o.isMesh||!['Terrain','Water','Canopy'].some(s=>o.name.startsWith(s)))return;found++;let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)bad.push(o.name);});return {found,bad}}''');assert out['theme_ancestry']['found']>=17 and not out['theme_ancestry']['bad']
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'guyana-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['PASS']=True;(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED_PASS',json.dumps(out))
