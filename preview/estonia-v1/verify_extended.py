from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.array(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.2 and im[:,:,:3].max()>30
rgb=np.array(Image.open(R/'maps/limestone-color.png'));assert np.all(np.abs(rgb.mean(axis=(0,1))-np.array([174,177,164]))<30)
out={'status':'PASS','poster_actual_pixels':True,'limestone_mean_rgb':rgb.mean(axis=(0,1)).tolist()}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':390,'height':844},is_mobile=True,has_touch=True);p=c.new_page();p.goto((R/'estonia-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Estonia / Limestone & Bog' in p.inner_text('body')
 assert 'Estonia' in p.locator('canvas').get_attribute('aria-label')
 assert not any(w in p.inner_text('body') for w in ['Japan','Cedar','Yakushima'])
 out['runtime']=p.evaluate('''(()=>{let water=0,planks=0,wrong=[],maps=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Bog_')||o.name.startsWith('Boardwalk_')){let a=o;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);if(o.name.startsWith('Bog__water'))water++;if(o.name.startsWith('Boardwalk__plank'))planks++;}for(const [key,ch] of [['map',0],['roughnessMap',1],['normalMap',0]]){const t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);const im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;const ctx=c.getContext('2d');ctx.drawImage(im,0,0);const d=ctx.getImageData(0,0,c.width,c.height).data;let min=255,max=0;for(let i=ch;i<d.length;i+=4){min=Math.min(min,d[i]);max=Math.max(max,d[i]);}maps.push({key,range:max-min,width:c.width,height:c.height});}});return {water,planks,wrong,maps}})()''')
 # Names follow Three sanitization; count exact imported names separately.
 names=p.evaluate("(()=>{let a=[];pilot.root.traverse(o=>{if(o.isMesh)a.push(o.name)});return a})()")
 out['runtime']['water']=len([n for n in names if n.startswith('Bog') and 'water' in n]);out['runtime']['planks']=len([n for n in names if n.startswith('Boardwalk') and 'plank' in n])
 assert out['runtime']['water']==3 and out['runtime']['planks']==18 and not out['runtime']['wrong']
 assert len(out['runtime']['maps'])>=3 and all(m['range']>0 and max(m['width'],m['height'])<=256 for m in out['runtime']['maps'])
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'estonia-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
