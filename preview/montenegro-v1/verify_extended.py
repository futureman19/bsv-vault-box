from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
result={}
a=np.array(Image.open(R/'poster.png').convert('RGB'));assert a.mean()>15 and a.max()>150
result['source_poster_nonblack']=True
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'montenegro-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Montenegro / Durmitor & Tara' in text and not any(s in text for s in ['Japan','Yakushima','cedar','Mossed granite'])
 features=p.evaluate('''()=>{let ornaments=[],maps=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(/^(Karst|Forest|Tara)_/.test(o.name)){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;ornaments.push({name:o.name,lid:!!a});}for(let slot of ['map','roughnessMap']){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0,s=[0,0,0];for(let i=0;i<d.length;i+=4){let value=d[i+(slot==='roughnessMap'?1:0)];mn=Math.min(mn,value);mx=Math.max(mx,value);for(let j=0;j<3;j++)s[j]+=d[i+j];}maps.push({material:o.material.name,slot,width:im.width,height:im.height,range:mx-mn,mean:s.map(x=>x/(d.length/4))});}});return {ornaments,maps};}''')
 assert len(features['ornaments'])==25 and all(o['lid'] for o in features['ornaments']),features
 assert all(m['range']>10 and max(m['width'],m['height'])<=512 for m in features['maps'])
 limestone=[m for m in features['maps'] if 'Limestone' in m['material'] and m['slot']=='map'][0]
 assert all(140<v<180 for v in limestone['mean'])
 result['runtime_features']=features
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'montenegro-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);result['noJS_poster']=True;c.close();b.close()
result['status']='PASS';(R/'extended-check.json').write_text(json.dumps(result,indent=2));print('PASS runtime theme, palette, map variation, lid ancestry, no-JS and source poster')
