from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'latvia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Latvia' in p.locator('canvas').get_attribute('aria-label')
 assert not any(s in p.locator('body').inner_text() for s in ['Japan','Yakushima','Mossed','Cedar'])
 features=p.evaluate('''(()=>{const stones=[],panels=[],maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Amber__cabochon'))stones.push(o.name);if(o.name.startsWith('Linen__raised'))panels.push(o.name);for(const kind of ['map','roughnessMap']){let t=o.material[kind];if(!t||seen.has(t.uuid+kind))continue;seen.add(t.uuid+kind);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,lo=255,hi=0;for(let i=kind==='roughnessMap'?1:0;i<d.length;i+=4){lo=Math.min(lo,d[i]);hi=Math.max(hi,d[i]);}maps.push({material:o.material.name,kind,width:c.width,height:c.height,range:hi-lo});}});return {stones,panels,maps}})()''')
 # Names are exporter-sanitized; use exact runtime discovery below rather than source spelling.
 names=p.evaluate("(()=>{let a=[];pilot.root.traverse(o=>{if(o.isMesh)a.push(o.name)});return a})()")
 stones=[n for n in names if n.startswith('Amber') and 'cabochon' in n];panels=[n for n in names if n.startswith('Linen') and 'raised' in n]
 assert len(stones)==3 and len(panels)==1,(stones,panels)
 assert len(features['maps'])>=6 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in features['maps'])
 ownership=p.evaluate("(()=>{let bad=[];pilot.root.traverse(o=>{if(!o.isMesh||!(/^(Amber|Linen)/.test(o.name)))return;let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)bad.push(o.name)});return bad})()")
 assert not ownership
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'latvia-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));c.close();b.close()
arr=np.array(Image.open(R/'maps/linen-color.png').convert('RGB'),dtype=np.float32);red=(arr[:,:,0]>arr[:,:,1]*2);cream=(arr[:,:,0]>150)&(arr[:,:,1]>140)
assert .18<red.mean()<.25 and cream.mean()>.70
poster=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (poster[:,:,:3].max(axis=2)>30).mean()>.1
out={'status':'PASS','runtime_maps':features['maps'],'runtime_cabochons':stones,'runtime_panels':panels,'all_ornaments_lid_owned':True,'linen_red_fraction':float(red.mean()),'linen_cream_fraction':float(cream.mean()),'noJS_poster':True,'source_render_nonblack':True,'country_copy_and_accessibility':True}
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
