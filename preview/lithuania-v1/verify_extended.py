from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.5 and im[:,:,:3].max()>150
out={'poster_nonempty':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'lithuania-v1.html').as_uri());p.wait_for_function('pilot.ready')
 probe='''()=>{let maps=[],wrong=[],ornaments=0,seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(/^(Dune|Vegetation|Lagoon)/.test(o.name)){ornaments++;let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}for(let k of ['map','roughnessMap']){let t=o.material[k];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,ca=document.createElement('canvas');ca.width=im.width;ca.height=im.height;let ctx=ca.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,ca.width,ca.height).data,mn=255,mx=0,ch=k==='roughnessMap'?1:0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind:k,width:ca.width,height:ca.height,range:mx-mn});}});return {maps,wrong,ornaments}}'''
 def valid(r):return r['ornaments']==24 and not r['wrong'] and len(r['maps'])>=3 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in r['maps'])
 r=p.evaluate(probe);assert valid(r),r;out['runtime']=r
 # Real negative control: detach the imported dune from its lid in-memory.
 p.evaluate("()=>{let o;pilot.root.traverse(x=>{if(x.name.startsWith('Dune'))o=x});pilot.root.attach(o)}")
 bad=p.evaluate(probe);assert not valid(bad);out['detached_dune_negative_control']={'rejected':True,'wrong':bad['wrong']}
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'lithuania-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['nojs_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
