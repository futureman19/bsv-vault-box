from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
out={}
im=Image.open(R/'poster.png').convert('RGBA');assert im.getchannel('A').getextrema()[1]>0;assert max(im.convert('RGB').getextrema()[0])>20
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':390,'height':844},is_mobile=True,has_touch=True);p=c.new_page();p.goto((R/'tanzania-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Tanzania' in p.locator('h1').inner_text();assert 'Tanzania' in p.locator('canvas').get_attribute('aria-label');assert 'Japan' not in p.locator('body').inner_text()
 out['runtime']=p.evaluate('''(()=>{let maps=[],terrain=0,wrong=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;let a=o;while(a&&!a.name.startsWith('Terrain'))a=a.parent;if(a){terrain++;let q=o;while(q&&q.name!=='Lid_Hinge')q=q.parent;if(!q)wrong.push(o.name);}for(let [key,channel] of [['map',0],['roughnessMap',1]]){let t=o.material[key];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,width:c.width,height:c.height,range:mx-mn});}});return {terrain,wrong,maps}})()''')
 assert out['runtime']['terrain']==3 and not out['runtime']['wrong']
 assert len(out['runtime']['maps'])==3
 assert all(m['range']>10 and m['width']==256 and m['height']==256 for m in out['runtime']['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'tanzania-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
out.update(status='PASS',no_js_poster=True,poster_nonempty=True,accessible_country_copy=True)
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
