from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageStat
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.getbbox();assert max(ImageStat.Stat(im.convert('RGB')).mean)>10
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'moldova-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let flowers=0,wrong=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Flower')){flowers++;let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}for(let type of ['map','roughnessMap','normalMap']){let t=o.material[type];if(!t||seen.has(t.uuid+type))continue;seen.add(t.uuid+type);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=type==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({type,range:mx-mn,width:c.width,height:c.height});}});return {flowers,wrong,maps}})()''')
 f=out['features'];assert f['flowers']==33 and not f['wrong'];assert len(f['maps'])>=4;assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in f['maps'])
 text=p.locator('body').inner_text();assert 'Moldova' in text and all(s not in text for s in ['Japan','Yakushima','Cedar','Moss'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'moldova-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
out['noJS_poster']=True;out['source_poster_nonblack']=True;out['status']='PASS'
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
