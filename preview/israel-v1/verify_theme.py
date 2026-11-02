from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'israel-v1.html').as_uri());p.wait_for_function('pilot.ready')
 result=p.evaluate('''(()=>{let terrain=[],maps=[],names=[],seen=new Set();pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(!o.isMesh)return;names.push(o.name);let theme=o;while(theme&&!theme.name.startsWith('Terrain'))theme=theme.parent;if(theme){let a=o.geometry.attributes.position,v=pilot.root.position.clone(),lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];for(let i=0;i<a.count;i++){v.fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld);v.toArray().forEach((x,k)=>{lo[k]=Math.min(lo[k],x);hi[k]=Math.max(hi[k],x)})}let ancestor=o.parent;while(ancestor&&ancestor.name!=='Lid_Hinge')ancestor=ancestor.parent;terrain.push({name:o.name,lid:!!ancestor,lo,hi});}for(let slot of ['map','roughnessMap','normalMap']){let t=o.material[slot];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,lo=255,hi=0;for(let i=0;i<d.length;i+=4){lo=Math.min(lo,d[i+(slot==='roughnessMap'?1:0)]);hi=Math.max(hi,d[i+(slot==='roughnessMap'?1:0)])}maps.push({slot,width:im.width,height:im.height,range:hi-lo});}});return {terrain,maps,names}})()''')
 assert result['terrain'] and all(t['lid'] for t in result['terrain'])
 lo=[min(t['lo'][k] for t in result['terrain']) for k in range(3)];hi=[max(t['hi'][k] for t in result['terrain']) for k in range(3)]
 assert hi[1]-lo[1]>.14 and (hi[0]-lo[0])/(hi[2]-lo[2])>1.5
 assert lo[1]<1.978 and lo[1]>1.8
 assert len(result['maps'])>=3 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in result['maps'])
 assert not any('cedar' in n.lower() or 'tree' in n.lower() for n in result['names'])
 # Negative control: actual loaded terrain is temporarily detached, the same parent gate must reject it.
 rejected=p.evaluate('''(()=>{let o=pilot.root.getObjectByName('Lid_Hinge');let t; o.traverse(n=>{if(n.name.startsWith('Terrain'))t=n});let parent=t.parent;pilot.root.attach(t);let a=t.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;let rejected=!a;parent.attach(t);return rejected})()''');assert rejected
 result['detached_terrain_negative_control_rejected']=rejected
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'israel-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);result['noJS_poster']=True;c.close();b.close()
result['status']='PASS';(R/'theme-check.json').write_text(json.dumps(result,indent=2));print('THEME / DECODED MAPS / NO-JS / NEGATIVE CONTROL PASS')
