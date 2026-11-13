from pathlib import Path
from playwright.sync_api import sync_playwright
import json,math
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'syria-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate("""(()=>{let rosettes=0,borders=0,front=0,wrong=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Inlay__rosette'))rosettes++;if(o.name.startsWith('Inlay__lid_border'))borders++;if(o.name.startsWith('Inlay__front_band'))front++;if(o.name.startsWith('Inlay')&&!o.name.includes('front_band')&&o.parent.name!=='Lid_Hinge')wrong.push(o.name);for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,width:c.width,height:c.height,range:mx-mn})}});return {rosettes,borders,front,wrong,maps}})()""")
 print(out)
 assert out['features']['rosettes']==24 and out['features']['borders']==34 and out['features']['front']==38 and not out['features']['wrong']
 assert all(x['range']>0 and max(x['width'],x['height'])<=512 for x in out['features']['maps'])
 assert len(out['features']['maps'])>=4
 assert 'Syria / Walnut & Pearl' in p.inner_text('body') and 'Yakushima' not in p.inner_text('body')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.wait_for_timeout(100)
 # Back view confirms the lid-borne ornament remains present at full opening.
 p.evaluate('''(()=>{let c=pilot.camera;c.position.set(5,4,-8);c.lookAt(0,1.9,0);c.updateMatrixWorld();})()''')
 # OrbitControls owns look direction; rotate using real pointer drag for captured rear view.
 p.locator('#reset').click();p.wait_for_timeout(100);p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'syria-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
