from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'maps/adnet-color.png').convert('RGB'));med=np.median(im,axis=(0,1));white=(im[:,:,1]>150).mean()
assert 110<med[0]<185 and med[0]-med[1]>30 and .03<white<.22
poster=Image.open(R/'poster.png').convert('RGBA');a=np.array(poster);assert (a[:,:,3]>0).mean()>.2 and a[:,:,:3].max()>100
out={'palette_median':med.tolist(),'ivory_fraction':float(white),'poster_nontransparent_fraction':float((a[:,:,3]>0).mean())}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'austria-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Austria' in p.locator('h1').inner_text()
 assert 'Austria' in p.locator('canvas').get_attribute('aria-label')
 assert not any(x in p.locator('body').inner_text() for x in ['Japan','Yakushima','cedar','Mossed'])
 features=p.evaluate('''(()=>{let maps=[],wrong=[],terrain=0,seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Terrain')){terrain++;let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}if(!o.isMesh)return;for(let [kind,im,ch] of [['color',o.material.map?.image,0],['roughness',o.material.roughnessMap?.image,1]]){if(!im||seen.has(im))continue;seen.add(im);let c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({kind,width:im.width,height:im.height,range:mx-mn});}});return {maps,wrong,terrain}})()''')
 assert features['terrain']>=1 and not features['wrong']
 assert len(features['maps'])>=3 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in features['maps'])
 out['runtime_features']=features;c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'austria-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
