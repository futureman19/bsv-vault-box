from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'qatar-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out=p.evaluate('''(()=>{const maps=[],wrong=[],seen=new Set();let dunes=0,water=0;pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Dune')||o.name.startsWith('Tidal_inlet')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);if(o.name.startsWith('Dune'))dunes++;else water++;}for(const key of ['map','roughnessMap','normalMap']){const t=o.material[key];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);const im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;const ctx=c.getContext('2d');ctx.drawImage(im,0,0);const d=ctx.getImageData(0,0,c.width,c.height).data;let mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,width:c.width,height:c.height,range:mx-mn});}});return {dunes,water,wrong,maps}})()''')
 assert out['dunes']==3 and out['water']==1 and not out['wrong']
 assert len(out['maps'])==3 and all(x['range']>0 and max(x['width'],x['height'])<=512 for x in out['maps'])
 assert 'Japan' not in p.locator('body').inner_text();assert 'Qatar' in p.locator('canvas').get_attribute('aria-label')
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'qatar-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
