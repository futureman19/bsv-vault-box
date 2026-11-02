from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'georgia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 data=p.evaluate('''(()=>{let tower=[],terrain=[],maps=[],wrong=[],seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Terrain'))terrain.push(o.name);if(o.isMesh&&o.name.startsWith('Tower'))tower.push(o.name);if((o.name.startsWith('Tower')||o.name.startsWith('Terrain'))&&!(()=>{let q=o.parent;while(q){if(q.name==='Lid_Hinge')return true;q=q.parent;}return false;})())wrong.push(o.name);if(!o.isMesh)return;for(let slot of ['map','normalMap','roughnessMap']){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,ca=document.createElement('canvas');ca.width=im.width;ca.height=im.height;let ctx=ca.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=0;i<d.length;i+=4){let channel=slot==='roughnessMap'?1:0;mn=Math.min(mn,d[i+channel]);mx=Math.max(mx,d[i+channel]);}maps.push({slot,width:im.width,height:im.height,range:mx-mn});}});return {tower,terrain,maps,wrong}})()''')
 def check(d):
  assert len(d['tower'])==5 and len(d['terrain'])>=1 and not d['wrong']
  assert {x['slot'] for x in d['maps']}=={'map','normalMap','roughnessMap'}
  assert all(x['range']>0 and max(x['width'],x['height'])<=1024 for x in d['maps'])
 print(json.dumps(data));check(data)
 # Real loaded-scene mutation; original hierarchy restored after negative control.
 bad=p.evaluate("(()=>{let o=pilot.root.getObjectByName('Tower__tapered_stone');if(!o)o=(()=>{let found;pilot.root.traverse(n=>{if(n.name.includes('tapered'))found=n});return found})();let parent=o.parent;pilot.root.attach(o);let failed=o.parent.name!=='Lid_Hinge';parent.attach(o);return failed})()")
 assert bad
 altered=dict(data,wrong=['detached tower']);rejected=False
 try:check(altered)
 except AssertionError:rejected=True
 assert rejected
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'georgia-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);b.close()
 data.update(status='PASS',detached_tower_negative_control_rejected=rejected,actual_scene_detachment_detected=bad,noJS_poster=True)
 (R/'theme-check.json').write_text(json.dumps(data,indent=2));print('THEME PASS',json.dumps(data))
