from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent

def validate(f):
 assert f['trunks']==3 and f['roots']>=6 and f['canopies']==3 and f['channels']==2,f
 assert not f['wrong'],f['wrong']
 assert len(f['maps'])>=2 and all(m['range']>30 and max(m['width'],m['height'])<=512 for m in f['maps'])

with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files','--use-angle=d3d11','--enable-gpu'],timeout=120000)
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'gambia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 f=p.evaluate('''(()=>{let trunks=0,roots=0,canopies=0,channels=0,maps=[],wrong=[];let seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Mangrove')){if(o.name.includes('trunk'))trunks++;if(o.name.includes('prop_root'))roots++;if(o.name.includes('canopy'))canopies++;}if(o.name.startsWith('Estuary'))channels++;if(/^(Mangrove|Bank|Estuary)/.test(o.name)&&o.parent.name!=='Lid_Hinge')wrong.push(o.name);if(o.material.map&&!seen.has(o.material.map.uuid)){seen.add(o.material.map.uuid);let im=o.material.map.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,width:im.width,height:im.height,range:mx-mn});}});return {trunks,roots,canopies,channels,maps,wrong}})()''')
 validate(f)
 negative=dict(f);negative['roots']=0
 try:validate(negative)
 except AssertionError:negative_rejected=True
 else:raise AssertionError('Missing root negative control passed')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'gambia-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
out={'status':'PASS','features':f,'missing_roots_negative_control_rejected':negative_rejected,'noJS_poster':True}
(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
