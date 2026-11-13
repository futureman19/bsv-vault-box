from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.4 and im[:,:,:3].max()>100
out={'poster_nonblack':True,'poster_nontransparent':True}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'southern-ocean-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Southern Ocean' in p.locator('body').inner_text();assert not any(t in p.locator('body').inner_text() for t in ['Japan','Yakushima','Cedar','Moss'])
 data=p.evaluate('''(()=>{const maps=[],parts=[],seen=new Set();pilot.root.traverse(o=>{if(o.name.startsWith('Pack_floe')||o.name.startsWith('Tabular_iceberg')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;parts.push({name:o.name,lid:!!a});}if(!o.isMesh)return;for(let [kind,t,ch] of [['color',o.material.map,0],['roughness',o.material.roughnessMap,1],['normal',o.material.normalMap,0]]){if(!t||seen.has(t.uuid+kind))continue;seen.add(t.uuid+kind);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,lo=255,hi=0,means=[0,0,0];for(let i=0;i<d.length;i+=4){lo=Math.min(lo,d[i+ch]);hi=Math.max(hi,d[i+ch]);for(let k=0;k<3;k++)means[k]+=d[i+k]/(d.length/4);}maps.push({kind,width:c.width,height:c.height,range:hi-lo,means});}});return{maps,parts}})()''')
 assert len(data['parts'])>=10 and all(x['lid'] for x in data['parts'])
 assert {x['kind'] for x in data['maps']}=={'color','roughness','normal'}
 assert all(x['range']>0 and max(x['width'],x['height'])<=1024 for x in data['maps'])
 color=next(x for x in data['maps'] if x['kind']=='color');assert color['means'][2]>color['means'][1]>color['means'][0]
 out['runtime']=data;c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'southern-ocean-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
