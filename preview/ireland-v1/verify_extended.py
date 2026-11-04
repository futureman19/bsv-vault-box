from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'ireland-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let clints=0,wrong=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Pavement')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);if(o.name.includes('clint'))clints++;}for(let kind of ['map','roughnessMap']){let t=o.material[kind];if(!t||seen.has(t.uuid+kind))continue;seen.add(t.uuid+kind);let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let cx=cv.getContext('2d');cx.drawImage(im,0,0);let d=cx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0,s=[0,0,0];for(let i=0;i<d.length;i+=4){let v=d[i+(kind==='roughnessMap'?1:0)];mn=Math.min(mn,v);mx=Math.max(mx,v);for(let j=0;j<3;j++)s[j]+=d[i+j];}maps.push({material:o.material.name,kind,width:im.width,height:im.height,range:mx-mn,mean:s.map(v=>v/(im.width*im.height))});}});return {clints,wrong,maps};})()''')
 f=out['features'];assert f['clints']==20 and not f['wrong'];assert all(m['range']>5 and max(m['width'],m['height'])<=512 for m in f['maps'])
 marble=next(m for m in f['maps'] if 'Connemara' in m['material'] and m['kind']=='map');assert marble['mean'][1]>max(marble['mean'][0],marble['mean'][2])
 assert 'Ireland' in p.title() and 'Ireland' in p.locator('canvas').get_attribute('aria-label')
 assert all(x not in p.locator('body').inner_text() for x in ['Japan','Yakushima','cedar'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'ireland-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
