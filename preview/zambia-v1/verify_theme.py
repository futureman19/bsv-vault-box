from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'zambia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 features=p.evaluate('''(()=>{let gorge=[],water=[],maps=[],wrong=[],stale=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(/Cedar|Finger|foliage/i.test(o.name))stale.push(o.name);let semantic=o.name.startsWith('Zambezi')?o:(o.parent?.name.startsWith('Zambezi')?o.parent:o);if(/Gorge|Zambezi|Falls/.test(semantic.name)){gorge.push(o.name);if(semantic.parent.name!=='Lid_Hinge')wrong.push(o.name);}if(/Zambezi/.test(semantic.name))water.push(o.name);if(o.material.map&&!seen.has(o.material.map.uuid)){seen.add(o.material.map.uuid);let im=o.material.map.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,lo=255,hi=0;for(let i=0;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}maps.push({width:im.width,height:im.height,range:hi-lo});}});return {gorge,water,maps,wrong,stale}})()''')
 def accept(f):
  assert len(f['gorge'])>=38 and len(f['water'])>=1, 'missing gorge/water geometry'
  assert not f['wrong'] and not f['stale'], 'wrong hierarchy or inherited theme'
  assert f['maps'] and all(m['range']>20 and max(m['width'],m['height'])<=1024 for m in f['maps']), 'texture variation/budget'
 (R/'theme-observed.json').write_text(json.dumps(features,indent=2))
 accept(features)
 # Real runtime mutation negative control: detach physical water from lid.
 p.evaluate("pilot.root.traverse(o=>{if(o.name.startsWith('Zambezi'))window.waterControl=o});pilot.root.attach(window.waterControl)")
 wrong=p.evaluate("window.waterControl.parent.name!=='Lid_Hinge'")
 bad=dict(features,wrong=['detached water'] if wrong else [])
 try:accept(bad)
 except AssertionError as e:negative={'rejected':True,'reason':str(e),'mutation':'actual loaded water detached from moving lid'}
 else:raise AssertionError('negative control accepted')
 p.evaluate("pilot.root.getObjectByName('Lid_Hinge').attach(window.waterControl)")
 assert p.evaluate("window.waterControl.parent.name==='Lid_Hinge'")
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(200);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'zambia-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
out={'status':'PASS','features':features,'negative_control':negative,'no_js_poster':True}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print('THEME PASS; actual detached-water negative control rejected; NO-JS PASS')
