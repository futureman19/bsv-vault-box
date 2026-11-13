"""Actual GLTFLoader feature checks and a deliberate missing-tower negative control."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files','--use-angle=d3d11','--enable-gpu'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'algeria-v1.html').as_uri());p.wait_for_function('pilot.ready')
 script='''(()=>{let towers=[],aprons=0,flutes=0,maps=[],wrong=[],obsolete=[],seen=new Set();pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(!o.isMesh)return;if(/Cedar|Moss|Granite|glacier|foliage/i.test(o.name))obsolete.push(o.name);if(o.name.startsWith('Tassili')){let a=o.geometry.attributes.position,vs=[],v=pilot.root.position.clone();for(let i=0;i<a.count;i++){v.fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld);vs.push(v.toArray());}towers.push({name:o.name,min:[0,1,2].map(k=>Math.min(...vs.map(v=>v[k]))),max:[0,1,2].map(k=>Math.max(...vs.map(v=>v[k])))});if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}if(o.name.startsWith('Terrain')){aprons++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}if(o.name.startsWith('Erosion'))flutes++;for(let slot of ['map','roughnessMap']){let tex=o.material[slot];if(tex&&!seen.has(tex.uuid)){seen.add(tex.uuid);let im=tex.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0,sums=[0,0,0];for(let i=0;i<d.length;i+=4){let channel=slot==='roughnessMap'?1:0;mn=Math.min(mn,d[i+channel]);mx=Math.max(mx,d[i+channel]);for(let k=0;k<3;k++)sums[k]+=d[i+k];}maps.push({material:o.material.name,slot,width:im.width,height:im.height,range:mx-mn,mean:sums.map(x=>x/(d.length/4))});}}});return {towers,aprons,flutes,maps,wrong,obsolete};})()'''
 def accept(f):
  assert len(f['towers'])==7,'expected 7 towers'
  assert f['aprons']==1 and f['flutes']>=40 and not f['wrong'] and not f['obsolete']
  for t in f['towers']:
   assert -.001< t['max'][1]-t['min'][1]-.25 <.55, t
   assert t['min'][0]>-1.65 and t['max'][0]<1.65 and t['min'][2]>-.95 and t['max'][2]<.95,t
   assert 1.99<t['min'][1]<2.05,t
  assert len(f['maps'])==3
  assert all(m['range']>20 and max(m['width'],m['height'])<=512 for m in f['maps'])
  color=next(m for m in f['maps'] if m['slot']=='map' and 'desert' in m['material'])
  assert color['mean'][0]>color['mean'][1]>color['mean'][2]
 f=p.evaluate(script);accept(f)
 p.evaluate("window.removedTower=pilot.root.getObjectByName('Tassili__tower_00');if(!removedTower){pilot.root.traverse(o=>{if(o.isMesh&&o.name.startsWith('Tassili')&&!window.removedTower)window.removedTower=o;});}removedTower.parent.remove(removedTower)")
 negative=False
 try:accept(p.evaluate(script))
 except AssertionError:negative=True
 assert negative,'missing tower was not rejected'
 p.evaluate("pilot.root.getObjectByName('Lid_Hinge').add(removedTower)");accept(p.evaluate(script))
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'algeria-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
 out={'status':'PASS','features':f,'missing_tower_negative_control_rejected':negative,'noJS_poster':True,'note':'Negative control after implementation, not test-first TDD; mobile is emulated.'}
 (R/'theme-check.json').write_text(json.dumps(out,indent=2));print('THEME PASS; MISSING_TOWER_NEGATIVE PASS; NO_JS PASS')
