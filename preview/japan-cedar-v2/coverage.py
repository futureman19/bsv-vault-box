from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,sys
R=Path(__file__).resolve().parent
baseline='--baseline' in sys.argv;folder=R.parent/'japan-cedar-v1' if baseline else R
out={};tag='before' if baseline else 'after'
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for name,w,h,m in [('desktop',1440,1080,False),('mobile',390,844,True)]:
  c=b.new_context(offline=True,viewport={'width':w,'height':h},device_scale_factor=1,is_mobile=m,has_touch=m);p=c.new_page();p.goto((folder/('japan-cedar-v1.html' if baseline else 'japan-cedar-v2.html')).as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(200)
  p.screenshot(path=str(R/f'{tag}-{name}.png'),full_page=True)
  for feature in ['foliage','moss']:
   p.evaluate('''feature=>{const root=pilot.root;root.parent.traverse(o=>{if(o.isMesh)o.visible=false});root.traverse(o=>{if(!o.isMesh)return;const selected=feature==='foliage'?o.name.includes('foliage'):o.name.startsWith('Terrain')&&o.name.includes('moss');o.visible=selected;if(selected){o.material=o.material.clone();o.material.color.set(0xffffff);o.material.emissive.set(0xffffff);o.material.emissiveIntensity=1;o.material.map=null;o.material.toneMapped=false;o.castShadow=false;o.receiveShadow=false;}});pilot.renderer.setClearColor(0x000000,1);}''',feature);p.wait_for_timeout(100)
   dest=R/f'{tag}-{name}-{feature}-mask.png';p.locator('canvas').screenshot(path=str(dest));im=Image.open(dest).convert('RGB');out[f'{name}_{feature}_pixels']=sum(min(v)>240 for v in im.getdata())
  c.close()
 b.close()
(R/f'{tag}-coverage.json').write_text(json.dumps(out,indent=2));print(out)
if not baseline:
 old=json.loads((R/'before-coverage.json').read_text());ratios={k:out[k]/old[k] for k in old};(R/'coverage-check.json').write_text(json.dumps({'method':'Same-camera white emissive isolated mesh raster coverage; silhouette union, not occlusion-aware ecosystem realism or biological density. Desktop and native mobile viewport.','baseline':old,'candidate':out,'ratios':ratios},indent=2));assert all(v>=(1.65 if 'foliage' in k else 1.8) for k,v in ratios.items()),ratios
