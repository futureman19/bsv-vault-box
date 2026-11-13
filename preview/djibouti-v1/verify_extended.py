from pathlib import Path
import json,io,struct
from PIL import Image,ImageStat
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
b=(R/'djibouti.glb').read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);binary=b[28+n:];ranges=[]
for idx,img in enumerate(g['images']):
 v=g['bufferViews'][img['bufferView']];im=Image.open(io.BytesIO(binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']])).convert('RGB')
 rough=any(m.get('pbrMetallicRoughness',{}).get('metallicRoughnessTexture',{}).get('index')==ti for m in g['materials'] for ti,t in enumerate(g['textures']) if t.get('source')==idx)
 extrema=im.getextrema()[1 if rough else 0];assert extrema[1]>extrema[0];assert max(im.size)<=1024;ranges.append({'name':img.get('name'),'channel':1 if rough else 0,'range':extrema[1]-extrema[0]})
im=Image.open(R/'poster.png');assert max(ImageStat.Stat(im.convert('RGB')).stddev)>15
with sync_playwright() as pw:
 browser=pw.chromium.launch(channel='msedge',headless=True)
 c=browser.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'djibouti-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');assert p.locator('#open').is_disabled();p.screenshot(path=str(R/'no-js.png'));c.close()
 c=browser.new_context(offline=True);p=c.new_page();p.goto((R/'djibouti-v1.html').as_uri());p.wait_for_function('pilot.ready');text=p.locator('body').inner_text()+' '+p.locator('canvas').get_attribute('aria-label');assert not any(s in text.lower() for s in ['japan','cedar','moss','yakushima','truncated']);assert 'Assal Salt Rift' in text;c.close();browser.close()
r={'status':'PASS','portable_map_variation':ranges,'actual_source_poster_nonblank':True,'no_js_poster':True,'country_copy_and_accessible_label':True};(R/'extended-check.json').write_text(json.dumps(r,indent=2));print(r)
