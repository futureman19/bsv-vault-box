from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'eswatini-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let body=0,lid=0,maps=[],wrong=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Body_coil'))body++;if(o.name.startsWith('Lid_coil')){lid++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}if(o.material.map&&!seen.has(o.material.map.uuid)){seen.add(o.material.map.uuid);let im=o.material.map.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0,sum=[0,0,0];for(let i=0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);for(let j=0;j<3;j++)sum[j]+=d[i+j];}maps.push({material:o.material.name,width:im.width,height:im.height,range:mx-mn,mean:sum.map(x=>x/(im.width*im.height))});}});return {body,lid,maps,wrong}})()''')
 f=out['features'];assert f['body']==12 and f['lid']==12 and not f['wrong']
 assert all(x['range']>20 and max(x['width'],x['height'])<=512 for x in f['maps'])
 straw=next(x for x in f['maps'] if 'Lutindzi' in x['material']);r,g,bl=straw['mean'];assert r>g>bl and r>150 and bl<130
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'eswatini-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
