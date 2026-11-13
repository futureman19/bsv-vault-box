from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'ghana-v1.html').as_uri());p.wait_for_function('pilot.ready')
 probe='''(()=>{let strips=[],ornaments=[],maps=[],wrong=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Kente__lid_strip')||o.name.startsWith('Ornament')){(o.name.startsWith('Kente')?strips:ornaments).push(o.name);if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}if(o.material.map&&!seen.has(o.material.map.uuid)){seen.add(o.material.map.uuid);let im=o.material.map.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,width:im.width,height:im.height,range:mx-mn});}});return {strips,ornaments,maps,wrong}})()'''
 out=p.evaluate(probe)
 # glTF sanitizes spaces/slashes; retain actual names for diagnosis.
 def validate(v):
  assert len(v['strips'])==8 and len(v['ornaments'])==3,v
  assert not v['wrong'],v['wrong']
  assert len(v['maps'])==2 and all(m['range']>20 and max(m['width'],m['height'])<=512 for m in v['maps']),v
 validate(out)
 p.evaluate("(()=>{let o=pilot.root.getObjectByName(''+"+json.dumps(out['strips'][0])+");pilot.root.attach(o);})()")
 try:validate(p.evaluate(probe));raise RuntimeError('negative control was accepted')
 except AssertionError:out['detached_lid_strip_negative_rejected']=True
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'ghana-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
 out['status']='PASS';(R/'theme-check.json').write_text(json.dumps(out,indent=2));print('THEME PASS: eight moving strips, three ornaments, decoded maps, detached-strip negative, no-JS poster')
