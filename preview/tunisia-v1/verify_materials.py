from pathlib import Path
from PIL import Image
from io import BytesIO
import json,struct,numpy as np
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
b=(R/'tunisia.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);binary=b[28+n:]
checks=[]
for m in g['materials']:
 p=m.get('pbrMetallicRoughness',{})
 for field,ch in [('baseColorTexture',0),('metallicRoughnessTexture',1)]:
  if field not in p:continue
  image=g['images'][g['textures'][p[field]['index']]['source']];v=g['bufferViews'][image['bufferView']];a=np.asarray(Image.open(BytesIO(binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']])).convert('RGB'));delta=int(np.ptp(a[:,:,ch]));assert delta>0
  assert max(a.shape[:2])<=512
  checks.append({'material':m['name'],'field':field,'channel':ch,'range':delta})
assert len(checks)>=3
poster=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert np.count_nonzero(poster[:,:,3])>poster.shape[0]*poster.shape[1]*.15;assert poster[:,:,:3].max()>100
with sync_playwright() as pw:
 browser=pw.chromium.launch(channel='msedge',headless=True)
 page=browser.new_page(offline=True);page.goto((R/'tunisia-v1.html').as_uri());page.wait_for_function('pilot.ready')
 assert 'Tunisia / Sejnane Clay' in page.inner_text('body')
 assert 'Tunisia' in page.locator('canvas').get_attribute('aria-label')
 assert not any(w in page.inner_text('body') for w in ['Japan','Yakushima','Moss','granite'])
 ancestry=page.evaluate("""()=>{let out=[];pilot.root.traverse(o=>{if(o.name.startsWith('Sejnane')){let p=o;while(p&&p.name!=='Lid_Hinge')p=p.parent;out.push({name:o.name,lid:!!p})}});return out}""")
 assert len(ancestry)==13 and all(x['lid'] for x in ancestry)
 browser.close()
r={'status':'PASS','decoded_maps':checks,'poster_nonempty':True,'runtime_ornament_ancestry':ancestry,'country_copy_and_accessibility':True}
(R/'material-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
