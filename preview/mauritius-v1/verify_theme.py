from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'mauritius-v1.html').as_uri());p.wait_for_function('pilot.ready')
 data=p.evaluate('''(()=>{let dunes=[],maps=[],seen=new Set();pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Dune')){let a=o.geometry.attributes.position,v=o.position.clone(),ys=[];for(let i=0;i<a.count;i++){v.fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld);ys.push(v.y);}dunes.push({name:o.name,parent:o.parent.name,color:o.material.color.getHexString(),min:Math.min(...ys),max:Math.max(...ys)});}if(o.material.map&&!seen.has(o.material.map.uuid)){seen.add(o.material.map.uuid);let im=o.material.map.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=0;i<a.length;i+=4){mn=Math.min(mn,a[i]);mx=Math.max(mx,a[i]);}maps.push({width:im.width,height:im.height,range:mx-mn});}});return {dunes,maps};})()''')
 def validate(d):
  assert len(d['dunes'])==7
  assert len(set(x['color'] for x in d['dunes']))==7
  assert all(x['parent']=='Lid_Hinge' and x['max']-x['min']>.03 and 1.98<x['min']<2.02 and x['max']<2.4 for x in d['dunes'])
  assert len(d['maps'])>=2 and all(m['range']>30 and max(m['width'],m['height'])<=512 for m in d['maps'])
 validate(data)
 bad=json.loads(json.dumps(data));bad['dunes'].pop()
 try:validate(bad)
 except AssertionError:negative=True
 else:raise AssertionError('Missing-ribbon negative control was accepted')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'mauritius-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
 data.update(status='PASS',missing_ribbon_negative_control_rejected=negative,nojs_poster=True)
 (R/'theme-check.json').write_text(json.dumps(data,indent=2));print('THEME PASS; missing-ribbon negative control rejected; NOJS PASS')
