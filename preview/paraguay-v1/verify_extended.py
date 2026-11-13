from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGBA');assert im.getextrema()[3][1]>0;assert max(im.convert('RGB').getextrema()[i][1] for i in range(3))>80
out={'poster_pixels_nonempty':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'paraguay-v1.html').as_uri());p.wait_for_function('pilot.ready')
 text=p.locator('body').inner_text();assert 'Paraguay' in text and all(s not in text for s in ['Japan','Yakushima','Mossed','JAPAN'])
 out['runtime']=p.evaluate('''(()=>{let ornaments=0,wrong=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Sunlace')){ornaments++;let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}for(let [slot,ch] of [['map',0],['roughnessMap',1]]){let t=o.material[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let x=c.getContext('2d');x.drawImage(im,0,0);let d=x.getImageData(0,0,c.width,c.height).data,min=255,max=0;for(let i=ch;i<d.length;i+=4){min=Math.min(min,d[i]);max=Math.max(max,d[i]);}maps.push({material:o.material.name,slot,channel:ch,width:im.width,height:im.height,range:max-min});}});return {ornaments,wrong,maps};})()''')
 assert out['runtime']['ornaments']==152 and not out['runtime']['wrong']
 assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in out['runtime']['maps'])
 assert len(out['runtime']['maps'])>=4
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'paraguay-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
