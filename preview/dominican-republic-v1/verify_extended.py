from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,:3].max(axis=2)>20).mean()>.4 and (im[:,:,3]>0).mean()>.9
c=np.array(Image.open(R/'maps/larimar-color.png'));white=(c[:,:,0]>180).mean();assert c[:,:,2].mean()>c[:,:,0].mean() and .05<white<.4
out={'poster_nonblack':True,'white_vein_fraction':float(white)}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 ctx=b.new_context(offline=True);p=ctx.new_page();p.goto((R/'dominican-republic-v1.html').as_uri());p.wait_for_function('pilot.ready')
 features=p.evaluate('''(()=>{let ornaments=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Ornament'))ornaments.push({name:o.name,parent:o.parent.name});for(let [kind,tex,ch] of [['color',o.material.map,0],['roughness',o.material.roughnessMap,1],['normal',o.material.normalMap,0]]){if(!tex||seen.has(tex.uuid+kind))continue;seen.add(tex.uuid+kind);let im=tex.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let x=c.getContext('2d');x.drawImage(im,0,0);let d=x.getImageData(0,0,c.width,c.height).data,lo=255,hi=0;for(let i=ch;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}maps.push({kind,range:hi-lo,width:c.width,height:c.height});}});return {ornaments,maps}})()''')
 assert len(features['ornaments'])==4 and all(o['parent']=='Lid_Hinge' for o in features['ornaments'])
 assert {'color','roughness','normal'}<={m['kind'] for m in features['maps']}
 assert all(m['range']>0 and max(m['width'],m['height'])<=512 for m in features['maps'])
 assert 'Yakushima' not in p.locator('body').inner_text() and 'Japan' not in p.locator('body').inner_text()
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(300);p.screenshot(path=str(R/'desktop-open-rear.png'));out['features']=features;ctx.close()
 ctx=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=ctx.new_page();p.goto((R/'dominican-republic-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));out['no_js_poster']=True;ctx.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
