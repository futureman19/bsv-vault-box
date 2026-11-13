from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'kenya-v1.html').as_uri());p.wait_for_function('pilot.ready')
 js='''(()=>{let lakes=[],terrain=[],wrong=[],maps=[];const seen=new Set();pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Lake'))lakes.push(o.name);if(o.name.startsWith('Terrain')){let a=o.geometry.attributes.position;for(let i=0;i<a.count;i++){let v=pilot.root.position.clone().fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld);terrain.push(v.y);}}if(/^(Lake|Shore|Terrain)/.test(o.name)&&o.parent.name!=='Lid_Hinge')wrong.push(o.name);if(o.material.map&&!seen.has(o.material.map.uuid)){seen.add(o.material.map.uuid);let im=o.material.map.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ct=cv.getContext('2d');ct.drawImage(im,0,0);let d=ct.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({width:im.width,height:im.height,range:mx-mn});}});return {lakes,terrain_max:Math.max(...terrain),wrong,maps}})()'''
 def validate(f):
  assert len(f['lakes'])==3,'three distinct lakes required'
  assert not f['wrong'],'all theme meshes must travel with lid'
  assert 2.1<f['terrain_max']<2.68,'relief envelope'
  assert len(f['maps'])>=2 and all(m['range']>30 and max(m['width'],m['height'])<=512 for m in f['maps']),'compact varying maps'
 f=p.evaluate(js);validate(f)
 # Real scene mutation negative control, not an invented result.
 p.evaluate("(()=>{let lake;pilot.root.traverse(o=>{if(o.name.startsWith('Lake')&&!lake)lake=o});lake.name='RemovedLake'})()")
 try:validate(p.evaluate(js))
 except AssertionError as e:negative=str(e)
 else:raise AssertionError('negative control failed to reject missing lake')
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'kenya-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);b.close()
 result={'status':'PASS','features':f,'negative_control_rejected':negative,'noJS_poster':True}
 (R/'theme-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
