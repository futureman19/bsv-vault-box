from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
out={}
im=np.asarray(Image.open(R/'maps/stone-color.png').convert('RGB'));mean=im.mean(axis=(0,1));assert 175<=mean[0]<=220 and 155<=mean[1]<=205 and 115<=mean[2]<=175
poster=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert np.mean(poster[:,:,3]>0)>.5 and np.mean(poster[:,:,:3])>10
out['stone_color_mean']=mean.tolist();out['poster_nonempty']=True
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'france-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let tiles=0,wrong=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Glazed_tile')){tiles++;let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}for(let [key,channel] of [['map',0],['roughnessMap',1]]){let t=o.material[key];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,cv.width,cv.height).data,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,channel,width:cv.width,height:cv.height,range:mx-mn});}});return {tiles,wrong,maps}})()''')
 f=out['features'];assert f['tiles']==160 and not f['wrong'];assert len(f['maps'])>=3 and all(m['range']>0 and max(m['width'],m['height'])<=256 for m in f['maps'])
 assert 'France Burgundy' in p.locator('canvas').get_attribute('aria-label')
 assert not any(x in p.locator('body').inner_text() for x in ['Japan','Yakushima','Mossed','cedar'])
 out['country_copy']=True
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'france-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
