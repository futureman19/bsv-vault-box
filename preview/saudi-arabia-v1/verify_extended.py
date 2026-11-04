from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'saudi-arabia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 body=p.locator('body').inner_text();assert 'AlUla' in body and not any(x in body for x in ['Japan','Yakushima','Mossed'])
 result=p.evaluate('''()=>{let rocks=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('AlUla__outcrop')||o.name.startsWith('AlUla_outcrop'))rocks.push({name:o.name,parent:o.parent.name});if(!o.isMesh)return;for(let [kind,t] of [['color',o.material.map],['roughness',o.material.roughnessMap]]){if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=kind==='roughness'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind,width:c.width,height:c.height,range:mx-mn});}});return {rocks,maps}}''')
 # GLTFLoader sanitizes slash and spaces; discover literal exported names robustly.
 if len(result['rocks'])!=3:
  result['rocks']=p.evaluate("()=>{let a=[];pilot.root.traverse(o=>{if(o.name.includes('outcrop'))a.push({name:o.name,parent:o.parent.name})});return a}")
 assert len(result['rocks'])==3 and all(x['parent']=='Lid_Hinge' for x in result['rocks'])
 assert len(result['maps'])>=3 and all(x['range']>10 and max(x['width'],x['height'])<=512 for x in result['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'saudi-arabia-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('e=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);result['noJS_poster']=True;c.close();b.close()
result['status']='PASS';(R/'extended-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
