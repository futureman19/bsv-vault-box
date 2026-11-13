from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'eritrea-v1.html').as_uri());p.wait_for_function('pilot.ready')
 data=p.evaluate('''(()=>{let islands=[],maps=[],wrong=[],seen=new Set();pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(!o.isMesh)return;if(/Cedar|Granite|Moss/.test(o.name))wrong.push(o.name);if(o.name.startsWith('Island')){let a=o.geometry.attributes.position,lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];for(let i=0;i<a.count;i++){let v=pilot.root.position.clone().fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld);[v.x,v.y,v.z].forEach((n,j)=>{lo[j]=Math.min(lo[j],n);hi[j]=Math.max(hi[j],n)})}islands.push({name:o.name,parent:o.parent.name,size:hi.map((n,j)=>n-lo[j])})}if(o.material.map&&!seen.has(o.material.map.uuid)){seen.add(o.material.map.uuid);let im=o.material.map.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,im.width,im.height).data,lo=255,hi=0;for(let i=0;i<a.length;i+=4){lo=Math.min(lo,a[i]);hi=Math.max(hi,a[i])}maps.push({material:o.material.name,width:im.width,height:im.height,range:hi-lo})}});return {islands,maps,wrong}})()''')
 assert len(data['islands'])==7 and not data['wrong']
 assert all(i['parent']=='Lid_Hinge' and .05<i['size'][1]<.35 and i['size'][0]>i['size'][1] for i in data['islands'])
 assert len(data['maps'])==2 and all(m['range']>5 and max(m['width'],m['height'])<=512 for m in data['maps'])
 assert any('limestone' in m['material'] and m['range']>40 for m in data['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'eritrea-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
 data.update(status='PASS',noJS_poster=True)
 (R/'theme-check.json').write_text(json.dumps(data,indent=2));print('THEME_AND_NOJS_PASS',json.dumps(data))
