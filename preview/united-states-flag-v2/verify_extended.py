"""Additional real Edge tests: decoded portable maps, fireworks geometry/motion,
all burst phases framing, reduced motion, no JS. No network used."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
im=np.asarray(Image.open(R/'poster.png').convert('RGBA'));assert (im[:,:,:3].max(axis=2)>20).mean()>.1
out={'poster_nonblank':True,'devices':[]}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 for width,height in [(1440,1080),(390,844)]:
  c=b.new_context(offline=True,viewport={'width':width,'height':height});p=c.new_page();p.goto((R/'united-states-flag-v2.html').as_uri());p.wait_for_function('pilot.ready')
  maps=p.evaluate('''()=>{let seen=new Set(),maps=[];pilot.root.traverse(o=>{if(!o.isMesh)return;for(let key of ['map','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,c.width,c.height).data,lo=255,hi=0;for(let i=key==='roughnessMap'?1:0;i<a.length;i+=4){lo=Math.min(lo,a[i]);hi=Math.max(hi,a[i]);}maps.push({key,channel:key==='roughnessMap'?'GREEN':'RED',range:hi-lo,width:c.width,height:c.height});}});return maps}''')
  assert len(maps)>=3 and all(m['range']>0 for m in maps)
  assert not p.evaluate("(()=>{let bad=[];pilot.root.traverse(o=>{if(/canyon|river|gorge|strata|limestone/i.test(o.name+' '+(o.material?.name||'')))bad.push(o.name)});return bad})()")
  assert not p.evaluate("pilot.root.getObjectByName('Presentation_fireworks_NOT_collectible')")
  p.emulate_media(reduced_motion='reduce');p.wait_for_timeout(100)
  static=p.evaluate('Array.from(pilot.fireworks.systems[0].positions)');p.wait_for_timeout(150);assert static==p.evaluate('Array.from(pilot.fireworks.systems[0].positions)')
  p.evaluate("window.samples=[];function sample(){samples.push(pilot.progress);if(samples.length<30)requestAnimationFrame(sample)};requestAnimationFrame(sample)");p.locator('#open').click();p.wait_for_function('samples.length===30');assert all(x in [0,1] for x in p.evaluate('samples'))
  maxima=[]
  for opened in [True,False]:
   if not opened:p.locator('#reset').click();p.wait_for_function('pilot.progress===0')
   v=p.evaluate('''()=>{const f=pilot.fireworks;let max=0,depthMin=99,depthMax=-99;for(let t=0;t<=3.6;t+=.05){f.update(t,false);f.group.updateMatrixWorld(true);f.group.traverse(o=>{if(!o.geometry)return;const a=o.geometry.attributes.position,v=pilot.root.position.clone();for(let i=0;i<a.count;i++){v.fromBufferAttribute(a,i);depthMin=Math.min(depthMin,v.z);depthMax=Math.max(depthMax,v.z);v.applyMatrix4(o.matrixWorld).project(pilot.camera);max=Math.max(max,Math.abs(v.x),Math.abs(v.y));}})}f.update(0,true);return {max,depthRange:depthMax-depthMin,particles:f.particleCount,trailSegments:f.trailSegments}}''')
   print('FIREWORK_BOUNDS',width,opened,v,flush=True)
   assert v['max']<1 and v['depthRange']>1 and v['particles']==216;maxima.append(v)
  p.emulate_media(reduced_motion='no-preference');a=p.evaluate('Array.from(pilot.fireworks.systems[0].positions)');p.wait_for_timeout(200);assert a!=p.evaluate('Array.from(pilot.fireworks.systems[0].positions)')
  p.screenshot(path=str(R/f'fireworks-{width}-animated.png'),full_page=True)
  p.emulate_media(reduced_motion='reduce');p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.screenshot(path=str(R/f'fireworks-{width}-open-static.png'),full_page=True)
  out['devices'].append(dict(width=width,maps=maps,firework_framing=maxima,animated_3d=True,reduced_static=True,reduced_pose_endpoints=True));c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'united-states-flag-v2.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('e=>e.complete&&e.naturalWidth>0');assert p.locator('#open').is_disabled();p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['PASS']=True;(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
