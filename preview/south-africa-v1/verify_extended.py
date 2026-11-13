from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'south-africa-v1.html').as_uri());p.wait_for_function('pilot.ready')
 result=p.evaluate('''()=>{let maps=[],wrong=[],mesa=0,plants=0;const seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Terrain')||o.name.startsWith('Fynbos')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);if(o.name.includes('mesa'))mesa++;if(o.name.startsWith('Fynbos'))plants++;}if(!o.isMesh)return;for(const [kind,t,ch] of [['color',o.material.map,0],['roughness',o.material.roughnessMap,1]]){if(!t||seen.has(t.uuid+kind))continue;seen.add(t.uuid+kind);let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let cx=cv.getContext('2d');cx.drawImage(im,0,0);let d=cx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind,material:o.material.name,width:im.width,height:im.height,range:mx-mn});}});return {maps,wrong,mesa,plants}}''')
 assert result['mesa']>=1 and result['plants']>=25 and not result['wrong']
 assert len(result['maps'])>=3 and all(m['range']>10 and max(m['width'],m['height'])<=512 for m in result['maps'])
 assert 'Japan' not in p.locator('body').inner_text();assert 'Japan' not in p.locator('canvas').get_attribute('aria-label')
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'south-africa-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));c.close();b.close()
result.update(status='PASS',no_js_poster=True);(R/'extended-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
