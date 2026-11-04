from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.getchannel('A').getextrema()[1]>0;assert max(im.convert('RGB').getextrema()[0])>30
out={'poster_nonblank':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'zimbabwe-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Zimbabwe Granite and Kopjes' in p.locator('canvas').get_attribute('aria-label')
 assert 'Yakushima' not in p.locator('body').inner_text() and 'Japan' not in p.locator('body').inner_text()
 out['features']=p.evaluate('''(()=>{let rocks=0,blocks=0,wrong=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Kopje')){rocks++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}if(o.name.startsWith('Masonry'))blocks++;for(let [kind,tex,ch] of [['color',o.material.map,0],['roughness',o.material.roughnessMap,1]]){if(!tex||seen.has(tex.uuid+kind))continue;seen.add(tex.uuid+kind);let im=tex.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let cx=cv.getContext('2d');cx.drawImage(im,0,0);let d=cx.getImageData(0,0,cv.width,cv.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind,width:im.width,height:im.height,range:mx-mn});}});return {rocks,blocks,wrong,maps}})()''')
 f=out['features'];assert f['rocks']==4 and f['blocks']>=160 and not f['wrong'];assert len(f['maps'])>=3 and all(m['range']>15 and max(m['width'],m['height'])<=256 for m in f['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'zimbabwe-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));out['no_js_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
