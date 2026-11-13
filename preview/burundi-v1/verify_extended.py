from pathlib import Path
from playwright.sync_api import sync_playwright
import json,copy
R=Path(__file__).resolve().parent

def accept(f):
 assert f['coils']==18 and f['panels']==4, 'Missing coil or woven panel'
 assert not f['wrong'], 'Ornament detached from lid'
 assert len(f['maps'])==3, 'Missing color, roughness or normal map'
 assert all(m['width']==512 and m['height']==512 and m['range']>0 for m in f['maps']), 'Flat or oversized maps'
 assert f['maxY']<2.30, 'Lid ornament too tall'

with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'burundi-v1.html').as_uri());p.wait_for_function('pilot.ready')
 query='''(()=>{let coils=0,panels=0,wrong=[],maps=[],maxY=-Infinity;const seen=new Set();pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Lid_coil')){coils++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);let pos=o.geometry.attributes.position,v=pilot.root.position.clone();for(let i=0;i<pos.count;i++){v.fromBufferAttribute(pos,i).applyMatrix4(o.matrixWorld);maxY=Math.max(maxY,v.y);}}if(o.name.startsWith('Woven_panel'))panels++;for(let key of ['map','roughnessMap','normalMap']){let t=o.material[key];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({slot:key,width:im.width,height:im.height,range:mx-mn});}});return {coils,panels,wrong,maps,maxY}})()'''
 f=p.evaluate(query);accept(f)
 # Genuine runtime mutation: detach one parsed coil, confirm gate rejects, restore.
 p.evaluate("window.detached=pilot.root.getObjectByName('Lid_coil__00');window.oldParent=detached.parent;pilot.root.attach(detached)")
 bad=p.evaluate(query)
 try:accept(bad)
 except AssertionError as e:negative={'mutation':'actual loaded coil reparented to scene root','rejected':True,'reason':str(e),'features':bad}
 else:raise AssertionError('Gate accepted detached ornament')
 p.evaluate('oldParent.attach(detached)');accept(p.evaluate(query))
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'burundi-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
 result={'status':'PASS','features':f,'runtime_negative_control':negative,'restored_pass':True,'noJS_poster':True}
 (R/'extended-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
