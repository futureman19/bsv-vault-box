from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent

def accept(f):
 assert f['canopies']>=18,'missing canopy'
 assert f['rivers']==1 and f['riverVertices']>=130,'missing continuous river'
 assert f['wrong']==[],'ornament is not lid-borne'
 assert 3.7<=f['slabWidth']<=3.73 and 2.37<=f['slabDepth']<=2.39,'wrong silhouette'
 assert f['reliefHeight']<=.65 and f['reliefHeight']>.2,'wrong relief height'
 assert len(f['maps'])>=3,'missing portable maps'
 assert all(m['range']>0 and m['width']==512 and m['height']==512 for m in f['maps']),'invalid map'
 assert any(m['range']>100 for m in f['maps']),'missing woven contrast'
 assert not f['legacy'],'unwanted prior theme'

with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'dr-congo-v1.html').as_uri());p.wait_for_function('pilot.ready')
 f=p.evaluate('''(()=>{let canopies=0,rivers=0,riverVertices=0,wrong=[],maps=[],legacy=[],slabWidth=0,slabDepth=0,top=0;const seen=new Set();pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(!o.isMesh)return;if(/Cedar|Granite|Finger/.test(o.name))legacy.push(o.name);if(o.name.startsWith('Canopy'))canopies++;if(o.name.startsWith('River')){rivers++;riverVertices=o.geometry.attributes.position.count;}if(/^(Canopy|River|Terrain)/.test(o.name)){if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);let a=o.geometry.attributes.position,v=pilot.root.position.clone();for(let i=0;i<a.count;i++){v.fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld);top=Math.max(top,v.y);}}if(o.name==='Lid__polished_slab'){o.geometry.computeBoundingBox();let b=o.geometry.boundingBox;slabWidth=b.max.x-b.min.x;slabDepth=b.max.z-b.min.z;}for(let key of ['map','roughnessMap','normalMap']){let t=o.material[key];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=0;i<d.length;i+=4){mn=Math.min(mn,d[i+(key==='roughnessMap'?1:0)]);mx=Math.max(mx,d[i+(key==='roughnessMap'?1:0)]);}maps.push({key,width:im.width,height:im.height,range:mx-mn});}});return {canopies,rivers,riverVertices,wrong,maps,slabWidth,slabDepth,reliefHeight:top-1.978,legacy}})()''')
 # Exported mesh positions retain Blender local XYZ but object rotation converts to Y up.
 if f['slabDepth']<1:
  f['slabDepth']=p.evaluate("(()=>{let o=pilot.root.getObjectByName('Lid__polished_slab');let b=o.geometry.boundingBox;return b.max.y-b.min.y})()")
 (R/'theme-observed.json').write_text(json.dumps(f,indent=2))
 accept(f)
 negatives=[]
 for label,patch in [('missing canopy',{'canopies':0}),('missing river',{'rivers':0}),('detached ornament',{'wrong':['Canopy']}),('oversized relief',{'reliefHeight':1}),('flat texture',{'maps':[{'range':0,'width':512,'height':512}]*3})]:
  try:accept({**f,**patch})
  except AssertionError as e:negatives.append({'control':label,'rejected':True,'reason':str(e)})
  else:raise AssertionError('Negative control incorrectly accepted '+label)
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'dr-congo-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
(R/'theme-check.json').write_text(json.dumps({'status':'PASS','actual_loader_features':f,'negative_controls':negatives,'no_js_poster':True},indent=2))
print('THEME PASS; 5 negative controls rejected; no-JS PASS')
