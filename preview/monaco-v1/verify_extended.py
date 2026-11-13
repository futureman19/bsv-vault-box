from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent;out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'monaco-v1.html').as_uri());p.wait_for_function('pilot.ready')
 assert 'Monaco / The Rock & Riviera' in p.locator('body').inner_text()
 assert not any(s in p.locator('body').inner_text() for s in ['Japan','Yakushima','cedar','Mossed'])
 out['features']=p.evaluate('''(()=>{let roofs=0,buildings=0,gardens=0,maps=[],wrong=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(/^(Riviera|Old_town|Garden|Rock)/.test(o.name)){let a=o.parent;while(a&&a.name!=='Lid_Hinge')a=a.parent;if(!a)wrong.push(o.name);}if(o.name.startsWith('Old_town')){if(o.name.includes('roof'))roofs++;if(o.name.includes('building'))buildings++;}if(o.name.startsWith('Garden'))gardens++;for(let [key,channel] of [['map',0],['roughnessMap',1],['normalMap',0]]){let t=o.material[key];if(!t||seen.has(t.uuid+key))continue;seen.add(t.uuid+key);let im=t.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=channel;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({key,channel,width:im.width,height:im.height,range:mx-mn});}});return {roofs,buildings,gardens,maps,wrong}})()''')
 p.emulate_media(reduced_motion='reduce')
 p.evaluate('window.snapSamples=[];window.snapActive=true;function sample(){snapSamples.push(pilot.progress);if(snapActive)requestAnimationFrame(sample)}requestAnimationFrame(sample)')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.locator('#reset').click();p.wait_for_function('pilot.progress===0')
 samples=p.evaluate('snapActive=false;snapSamples');assert samples and all(v in [0,1] for v in samples),samples
 out['reduced_motion_frame_samples']=samples
 f=out['features'];assert f['roofs']==7 and f['buildings']==7 and f['gardens']==6 and not f['wrong'],f
 assert len(f['maps'])==3 and all(x['range']>0 and max(x['width'],x['height'])<=256 for x in f['maps']),f
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'monaco-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
