from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent;out={}
im=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.1 and im[:,:,:3].max()>50
out['source_poster_nonempty']=True
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'haiti-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Haiti / Cut Steel & Garden' in p.inner_text('body')
 assert not any(s in p.inner_text('body') for s in ['Japan','Yakushima','Cedar','Iceland'])
 out['features']=p.evaluate('''(()=>{let leaves=0,wrong=[],maps=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Garden')){if(o.name.includes('leaf'))leaves++;if(o.parent.name!=='Lid_Hinge')wrong.push(o.name)}for(const [kind,t,ch] of [['color',o.material.map,0],['roughness',o.material.roughnessMap,1],['normal',o.material.normalMap,0]]){if(!t||seen.has(kind+t.uuid))continue;seen.add(kind+t.uuid);let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i])}maps.push({kind,width:im.width,height:im.height,range:mx-mn})}});return {leaves,wrong,maps}})()''')
 f=out['features'];assert f['leaves']==12 and not f['wrong'];assert {x['kind'] for x in f['maps']}=={'color','roughness','normal'}
 assert all(x['range']>0 and max(x['width'],x['height'])<=512 for x in f['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'haiti-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
