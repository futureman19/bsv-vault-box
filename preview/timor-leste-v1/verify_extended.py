from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'timor-leste-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let runner=0,fringe=0,maps=[],wrong=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Runner')||o.name.startsWith('Fringe')){if(o.name.startsWith('Runner'))runner++;else fringe++;let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}for(const channel of ['map','roughnessMap']){let t=o.material[channel];if(!t||seen.has(t.uuid+channel))continue;seen.add(t.uuid+channel);let im=t.image,can=document.createElement('canvas');can.width=im.width;can.height=im.height;let ctx=can.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=channel==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({channel,material:o.material.name,width:im.width,height:im.height,range:mx-mn});}});return {runner,fringe,maps,wrong}})()''')
 f=out['features'];assert f['runner']==1 and f['fringe']==56 and not f['wrong'];assert len(f['maps'])>=3;assert all(m['range']>10 and max(m['width'],m['height'])<=512 for m in f['maps'])
 assert 'Japan' not in p.locator('body').inner_text();assert 'Timor-Leste' in p.locator('canvas').get_attribute('aria-label')
 out['copy_and_accessibility']=True;c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'timor-leste-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
