from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'angola-v1.html').as_uri());p.wait_for_function('pilot.ready')
 data=p.evaluate('''(()=>{let cliffs=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Cliff')){let a=o.geometry.attributes.position,lo=Infinity,hi=-Infinity;for(let i=0;i<a.count;i++){let v=o.position.clone().fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld);lo=Math.min(lo,v.y);hi=Math.max(hi,v.y);}cliffs.push({name:o.name,parent:o.parent.name,vertices:a.count,relief:hi-lo});}if(o.material.map&&!seen.has(o.material.map.uuid)){seen.add(o.material.map.uuid);let im=o.material.map.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,c.width,c.height).data,lo=255,hi=0;for(let i=0;i<a.length;i+=4){lo=Math.min(lo,a[i]);hi=Math.max(hi,a[i]);}maps.push({width:c.width,height:c.height,range:hi-lo});}});return {cliffs,maps};})()''')
 assert len(data['cliffs'])==3 and all(x['parent']=='Lid_Hinge' and .15<x['relief']<.65 for x in data['cliffs']),data
 assert len(data['maps'])>=2 and all(x['range']>30 and max(x['width'],x['height'])<=1024 for x in data['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'angola-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
data['noJS_poster']=True;data['status']='PASS';(R/'extended-check.json').write_text(json.dumps(data,indent=2));print(json.dumps(data,indent=2))
