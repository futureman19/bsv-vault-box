from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageStat
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png');assert im.width>=900 and max(ImageStat.Stat(im.convert('RGB')).stddev)>20
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'slovakia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Slovakia' in text and not any(w in text for w in ['Japan','Yakushima','Iceland'])
 result=p.evaluate('''(()=>{let maps=[],relief=0,wrong=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Lime_relief')){relief++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}for(const [slot,channel] of [['map',0],['roughnessMap',1],['normalMap',1]]){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({slot,channel,width:c.width,height:c.height,range:mx-mn});}});return {relief,wrong,maps};})()''')
 assert result['relief']==60 and not result['wrong'];assert all(m['range']>0 and max(m['width'],m['height'])<=1024 for m in result['maps']);assert {'map','roughnessMap','normalMap'}<=set(m['slot'] for m in result['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'slovakia-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
result.update(status='PASS',no_js_poster=True,poster_pixels=True,identity_copy=True)
(R/'extended-check.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
