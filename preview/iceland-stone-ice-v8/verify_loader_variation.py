from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files']);c=b.new_context(offline=True);p=c.new_page();p.goto((R/'iceland-stone-ice-v8.html').as_uri());p.wait_for_function('pilot.ready')
 data=p.evaluate('''(()=>{let maps=[],colors=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;const m=o.material;if(m.name.startsWith('Basalt /'))for(let k of ['map','normalMap','roughnessMap']){let t=m[k];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let c=document.createElement('canvas');c.width=t.image.width;c.height=t.image.height;let x=c.getContext('2d');x.drawImage(t.image,0,0);let a=x.getImageData(0,0,c.width,c.height).data,lo=[255,255,255],hi=[0,0,0];for(let i=0;i<a.length;i+=4)for(let j=0;j<3;j++){lo[j]=Math.min(lo[j],a[i+j]);hi[j]=Math.max(hi[j],a[i+j]);}maps.push({kind:k,width:c.width,height:c.height,min:lo,max:hi});}if(m.name.startsWith('Glacier /')){let a=o.geometry.attributes.color;if(a){let lo=[1,1,1],hi=[0,0,0];for(let i=0;i<a.count;i++){let v=[a.getX(i),a.getY(i),a.getZ(i)];for(let j=0;j<3;j++){lo[j]=Math.min(lo[j],v[j]);hi[j]=Math.max(hi[j],v[j]);}}colors.push({min:lo,max:hi,transmission:m.transmission})}}});return {maps,colors}})()''')
 assert {x['kind'] for x in data['maps']}=={'map','normalMap','roughnessMap'}
 assert all(x['width']==512 and x['height']==512 and max(b-a for a,b in zip(x['min'],x['max']))>15 for x in data['maps'])
 assert data['colors'] and all(x['transmission']>.3 and x['max'][0]-x['min'][0]>.4 for x in data['colors'])
 (R/'loader-variation-check.json').write_text(json.dumps(data,indent=2));b.close()
print('REAL_DECODED_MAP_AND_VERTEX_COLOR_VARIATION_PASS')
