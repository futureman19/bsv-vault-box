from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
out={}
im=np.asarray(Image.open(R/'maps/stone-color.png'));means=im.mean(axis=(0,1));assert 45<means[0]<95 and 55<means[1]<105
poster=Image.open(R/'poster.png').convert('RGBA');a=np.asarray(poster);assert np.mean(a[:,:,3]>0)>.2 and a[:,:,:3].max()>100
out['palette_mean']=means.tolist();out['poster_nonempty']=True
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'costa-rica-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['runtime']=p.evaluate('''(()=>{let canopy=0,cone=0,wrong=[],maps=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Rainforest')||o.name.startsWith('Arenal')){if(o.name.includes('canopy'))canopy++;if(o.name.includes('cone'))cone++;let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}for(const [key,ch] of [['map',0],['roughnessMap',1]]){let t=o.material[key];if(!t||seen.has(t.uuid+ch))continue;seen.add(t.uuid+ch);let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,channel:ch,width:im.width,height:im.height,range:mx-mn});}});return {canopy,cone,wrong,maps}})()''')
 r=out['runtime'];assert r['canopy']==24 and r['cone']==1 and not r['wrong'];assert all(m['range']>20 and max(m['width'],m['height'])<=512 for m in r['maps'])
 assert 'Yakushima' not in p.locator('body').inner_text() and 'Japan' not in p.locator('body').inner_text()
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.screenshot(path=str(R/'desktop-open-rear.png'));c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'costa-rica-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
