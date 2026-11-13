from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.size==(900,820);assert im.getextrema()[3][1]>0;assert max(im.convert('RGB').getextrema()[0])>40
out={'poster_actual_source_dimensions':list(im.size)}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'iran-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let counts={star:0,jewel:0,diamond:0},wrong=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Mosaic')){if(o.name.includes('star'))counts.star++;if(o.name.includes('jewel'))counts.jewel++;if(o.name.includes('diamond'))counts.diamond++;let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}for(let [key,ch] of [['map',0],['roughnessMap',1]]){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,channel:ch,width:im.width,height:im.height,range:mx-mn});}});return {counts,wrong,maps}})()''')
 f=out['features'];assert f['counts']=={'star':15,'jewel':15,'diamond':8} and not f['wrong'];assert len(f['maps'])==2;assert all(m['range']>15 and max(m['width'],m['height'])<=512 for m in f['maps'])
 assert 'Iran' in p.locator('canvas').get_attribute('aria-label')
 assert all(s not in p.locator('body').inner_text() for s in ['Japan','Yakushima','Cedar','Moss'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'iran-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
