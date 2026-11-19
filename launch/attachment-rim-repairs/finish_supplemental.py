"""Final supplemental native browser gates; append-only evidence directory."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import json,numpy as np
R=Path(__file__).resolve().parents[2];D=R/'launch/attachment-rim-repairs/finish'
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for row in json.loads((D/'targets.json').read_text()):
  slug=row['id'];root=R/'preview'/f'{slug}-repair-v2' if slug!='iceland' else D/'iceland/verified';html=root/f'{slug}-repair-v2.html' if slug!='iceland' else root/'iceland-backright-v10.html'
  out=root/'supplemental';out.mkdir(exist_ok=False);result={}
  im=np.array(Image.open(root/'poster.png').convert('RGBA'));assert (im[:,:,3]>0).mean()>.1 and im[:,:,:3].max()>80;result['poster_nonempty']=True
  c=b.new_context(offline=True,viewport={'width':390,'height':844},is_mobile=True,has_touch=True,reduced_motion='reduce');p=c.new_page();p.goto(html.as_uri());p.wait_for_function('pilot.ready')
  result['maps']=p.evaluate('''(()=>{let maps=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(let type of ['map','normalMap','roughnessMap']){let t=o.material[type];if(!t||seen.has(t.uuid+type))continue;seen.add(t.uuid+type);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,ch=type==='roughnessMap'?1:0,mn=255,mx=0;for(let i=ch;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i])}maps.push({type,width:c.width,height:c.height,range:mx-mn,channel:ch})}});return maps})()''')
  assert result['maps'] and all(m['range']>0 for m in result['maps'])
  p.evaluate('window.snapFrames=[];window.snapActive=true;function record(){if(snapActive){snapFrames.push(pilot.progress);requestAnimationFrame(record)}};requestAnimationFrame(record)');p.locator('#open').tap();p.wait_for_function('pilot.progress===1');p.wait_for_timeout(80);p.locator('#reset').tap();p.wait_for_function('pilot.progress===0');p.wait_for_timeout(80)
  frames=p.evaluate('snapActive=false;snapFrames');assert 0 in frames and 1 in frames and all(x in (0,1) for x in frames);result['reduced_motion_frames']=frames;c.close()
  c=b.new_context(offline=True,viewport={'width':1440,'height':1080},reduced_motion='reduce');p=c.new_page();p.goto(html.as_uri());p.wait_for_function('pilot.ready');p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(out/'desktop-open-rear.png'),full_page=True);c.close()
  c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto(html.as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(out/'mobile-nojs.png'),full_page=True);result['noJS_poster']=True;c.close()
  (out/'check.json').write_text(json.dumps(result,indent=2));print(slug,'PASS',flush=True)
 b.close()
