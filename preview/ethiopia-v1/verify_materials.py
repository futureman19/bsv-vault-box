from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGB'));assert im.std()>15 and im.max()>150
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'ethiopia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Ethiopia / Simien Escarpment' in p.locator('h1').inner_text()
 assert 'Ethiopia' in p.locator('canvas').get_attribute('aria-label')
 assert not any(x in p.locator('body').inner_text() for x in ['Japan','Yakushima','cedar','Moss'])
 out=p.evaluate('''(()=>{let maps=[],wrong=[],terrains=new Set(),seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Escarpment')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);if(o.parent.name==='Lid_Hinge')terrains.add(o.name);}if(!o.isMesh)return;for(const [kind,t,channel] of [['color',o.material.map,0],['roughness',o.material.roughnessMap,1]]){if(!t||seen.has(t.uuid+kind))continue;seen.add(t.uuid+kind);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let data=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=channel;i<data.length;i+=4){mn=Math.min(mn,data[i]);mx=Math.max(mx,data[i]);}maps.push({kind,width:im.width,height:im.height,range:mx-mn});}});return {maps,wrong,terrainCount:terrains.size}})()''')
 assert out['terrainCount']==3 and not out['wrong'],out
 assert len(out['maps'])>=3 and all(m['range']>10 and max(m['width'],m['height'])<=512 for m in out['maps']),out
 b.close()
out['status']='PASS';out['poster_nonblank']=True
(R/'material-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
