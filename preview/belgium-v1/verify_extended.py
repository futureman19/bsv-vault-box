from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent;out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'belgium-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Belgium / Petit Granit' in text and not any(w in text for w in ['Japan','Yakushima','Cedar','Moss'])
 assert 'Belgium' in p.locator('canvas').get_attribute('aria-label')
 out['features']=p.evaluate('''(()=>{let fossils=0,maps=[],wrong=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Fossil')){fossils++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0,sum=[0,0,0];for(let i=0;i<d.length;i+=4){let v=d[i+(key==='roughnessMap'?1:0)];mn=Math.min(mn,v);mx=Math.max(mx,v);for(let j=0;j<3;j++)sum[j]+=d[i+j];}maps.push({material:o.material.name,key,width:im.width,height:im.height,range:mx-mn,mean:sum.map(v=>v/(d.length/4))});}});return {fossils,maps,wrong}})()''')
 f=out['features'];assert f['fossils']==69 and not f['wrong'];assert len(f['maps'])==3
 assert all(x['range']>30 and max(x['width'],x['height'])<=512 for x in f['maps'])
 stone=next(x for x in f['maps'] if x['key']=='map' and 'honed' in x['material']);r,g,blue=stone['mean'];assert 45<r<95 and 55<g<105 and 65<blue<115 and r<g<blue
 out['copy_and_accessibility']='PASS';out['status']='PASS';c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'belgium-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
