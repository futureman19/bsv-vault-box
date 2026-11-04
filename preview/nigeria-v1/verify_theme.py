from pathlib import Path
import json
from playwright.sync_api import sync_playwright
from PIL import Image
R=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True);page=c.new_page();page.goto((R/'nigeria-v1.html').as_uri());page.wait_for_function('pilot.ready')
 data=page.evaluate('''()=>{let discs=[],rings=[],maps=[];pilot.root.traverse(o=>{if(o.name.startsWith('Resist')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)throw Error('Detached ornament');if(o.name.includes('raised'))discs.push(o.name);if(o.name.includes('brass_ring'))rings.push(o.name)}if(o.isMesh&&o.material.map&&!maps.length){for(let [key,ch] of [['map',0],['roughnessMap',1],['normalMap',0]]){let t=o.material[key];if(!t)throw Error('Missing map');let im=t.image,cv=document.createElement('canvas');cv.width=im.width;cv.height=im.height;let ctx=cv.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,cv.width,cv.height).data,min=255,max=0,blue=0,pale=0;for(let i=0;i<d.length;i+=4){min=Math.min(min,d[i+ch]);max=Math.max(max,d[i+ch]);if(d[i+2]>d[i]*1.4)blue++;if(d[i]>130&&d[i+1]>150)pale++}maps.push({key,width:im.width,height:im.height,range:max-min,blue:blue/(d.length/4),pale:pale/(d.length/4)})}}});return {discs,rings,maps}}''')
 assert len(data['discs'])==3 and len(data['rings'])==3,data
 assert len(data['maps'])==3
 for m in data['maps']:assert m['width']==512 and m['height']==512 and m['range']>0,m
 color=data['maps'][0];assert color['range']>30 and color['blue']>.4 and color['pale']>.02,color
 c.close();c=b.new_context(offline=True,java_script_enabled=False);page=c.new_page();page.goto((R/'nigeria-v1.html').as_uri());assert page.locator('#fallback').is_visible();page.screenshot(path=str(R/'no-js.png'));c.close();b.close()
im=Image.open(R/'poster.png').convert('RGB');assert max(im.getextrema()[0])-min(im.getextrema()[0])>30
(R/'theme-check.json').write_text(json.dumps(dict(status='PASS',runtime=data,no_js_poster=True,poster_nonblack=True),indent=2));print('THEME_PASS')
