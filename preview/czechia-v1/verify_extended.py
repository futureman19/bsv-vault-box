from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageStat
import json
R=Path(__file__).resolve().parent
im=Image.open(R/'poster.png').convert('RGB');assert max(ImageStat.Stat(im).stddev)>15
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'czechia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out=p.evaluate('''(()=>{let gems=[],maps=[];pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Cut_crystal')){gems.push({name:o.name,parent:o.parent.name});}let m=o.material;for(let [t,ch] of [[m.map,0],[m.roughnessMap,1]]){if(!t)continue;let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=ch;i<a.length;i+=4){mn=Math.min(mn,a[i]);mx=Math.max(mx,a[i]);}maps.push({range:mx-mn,width:im.width,height:im.height});}});return {gems,maps}})()''')
 assert len(out['gems'])==9 and all(g['parent']=='Lid_Hinge' for g in out['gems'])
 assert out['maps'] and all(m['range']>0 and max(m['width'],m['height'])<=256 for m in out['maps'])
 assert 'Czechia' in p.title() and 'Japan' not in p.locator('body').inner_text()
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'czechia-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));b.close()
out.update(status='PASS',no_js=True,poster_nonblank=True)
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS')
