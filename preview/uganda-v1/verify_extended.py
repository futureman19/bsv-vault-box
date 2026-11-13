from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'uganda-v1.html').as_uri());p.wait_for_function('pilot.ready')
 result=p.evaluate('''()=>{let maps=[],seen=new Set(),cloth=[];pilot.root.traverse(o=>{if(o.name.startsWith('Mutuba')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;cloth.push({name:o.name,lid:!!a});}if(!o.isMesh)return;for(let [kind,t,ch] of [['color',o.material.map,0],['roughness',o.material.roughnessMap,1]]){if(!t||seen.has(t.uuid+kind))continue;seen.add(t.uuid+kind);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind,range:mx-mn,width:c.width,height:c.height});}});return {maps,cloth,text:document.body.innerText,aria:document.querySelector('canvas').getAttribute('aria-label')}}''')
 assert result['cloth'] and all(x['lid'] for x in result['cloth'])
 assert all(x['range']>0 and x['width']<=512 and x['height']<=512 for x in result['maps'])
 assert any(x['kind']=='roughness' for x in result['maps'])
 assert 'Uganda' in result['text'] and 'Uganda' in result['aria'] and 'Japan' not in result['text']+result['aria']
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'uganda-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);result['nojs_poster']=True;c.close();b.close()
result['status']='PASS';(R/'extended-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
