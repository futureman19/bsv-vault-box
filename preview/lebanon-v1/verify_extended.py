from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'lebanon-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out=p.evaluate('''(()=>{let wrong=[],pads=0,maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Lebanon_cedar')||o.name.startsWith('Terrain')){let q=o.parent;while(q&&q.name!=='Lid_Hinge')q=q.parent;if(!q)wrong.push(o.name);if(o.name.includes('canopy')||o.name.includes('crown'))pads++;}for(let slot of ['map','roughnessMap']){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=slot==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,slot,width:c.width,height:c.height,range:mx-mn});}});return {wrong,pads,maps}})()''')
 assert not out['wrong'] and out['pads']==16
 assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in out['maps'])
 assert any('Limestone' in m['material'] for m in out['maps'])
 assert 'Lebanon' in p.inner_text('h1') and 'Japan' not in p.inner_text('body')
 assert 'Limestone' in p.locator('canvas').get_attribute('aria-label')
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'lebanon-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
