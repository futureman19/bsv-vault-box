"""Real runtime feature gates and deliberately rejected ancestry regression."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
probe='''(()=>{const root=pilot.root,features={islands:[],wrong:[],maps:[],nonfiniteUV:0};const seen=new Set();root.traverse(o=>{if(o.name.startsWith('Delta__island')&&!o.isMesh)features.islands.push(o.name);if(o.name.startsWith('Delta')){let a=o,ok=false;while(a.parent){a=a.parent;if(a.name==='Lid_Hinge')ok=true;}if(!ok)features.wrong.push(o.name);}if(!o.isMesh)return;const uv=o.geometry.attributes.uv;if(uv)for(let i=0;i<uv.count;i++)if(!Number.isFinite(uv.getX(i))||!Number.isFinite(uv.getY(i)))features.nonfiniteUV++;for(const slot of ['map','roughnessMap','normalMap']){const t=o.material[slot];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);const im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;const ctx=c.getContext('2d');ctx.drawImage(im,0,0);const d=ctx.getImageData(0,0,im.width,im.height).data;let mn=255,mx=0,ivory=0,teal=0;for(let i=0;i<d.length;i+=4){mn=Math.min(mn,d[i+(slot==='roughnessMap'?1:0)]);mx=Math.max(mx,d[i+(slot==='roughnessMap'?1:0)]);if(d[i]>180&&d[i+1]>150&&d[i+2]<220)ivory++;if(d[i]<80&&d[i+1]>50&&d[i+2]>50)teal++;}features.maps.push({material:o.material.name,slot,width:im.width,height:im.height,range:mx-mn,ivory,teal});}});return features})()'''
def accept(f):
 assert len(f['islands'])==4,f['islands']
 assert not f['wrong'],f['wrong']
 assert f['nonfiniteUV']==0
 assert len(f['maps'])==4
 assert all(max(m['width'],m['height'])<=512 and m['range']>0 for m in f['maps'])
 woven=[m for m in f['maps'] if m['material'].startswith('Jamdani') and m['slot']=='map'];assert len(woven)==1
 assert woven[0]['ivory']>10000 and woven[0]['teal']>100000
 assert any(m['slot']=='normalMap' for m in f['maps'])
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'bangladesh-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate(probe);accept(out['features'])
 # Actual live asset mutation demonstrates the ancestry gate can reject a regression.
 p.evaluate("(()=>{const o=pilot.root.getObjectByName('Delta__island_1');window.detached=o;window.originalParent=o.parent;pilot.root.attach(o);})()")
 bad=p.evaluate(probe)
 try:accept(bad)
 except AssertionError as e:out['negative_control']={'result':'EXPECTED FAIL','mutation':'detach actual island 1 from lid in loaded scene','rejected':str(e)}
 else:raise AssertionError('Negative control was not rejected')
 p.evaluate('originalParent.attach(detached)');accept(p.evaluate(probe));out['restored']='PASS'
 # Top-facing diagnostic using real pointer drag, no synthetic geometry.
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x,y+160,steps=30);p.mouse.up();p.wait_for_timeout(100);p.screenshot(path=str(R/'desktop-lid-detail.png'),full_page=True)
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'bangladesh-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['no_js_poster']='PASS';c.close();b.close()
out['result']='PASS';(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
