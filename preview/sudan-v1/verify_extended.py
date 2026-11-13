from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'sudan-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let pyramids=[],terrain=[],maps=[],wrong=[],root=pilot.root;const seen=new Set();root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Pyramid')){pyramids.push(o.name);if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}if(o.name.startsWith('Terrain')){terrain.push(o.name);if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}for(const channel of ['map','normalMap','roughnessMap']){let tex=o.material[channel];if(!tex||seen.has(tex.uuid))continue;seen.add(tex.uuid);let im=tex.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0,mean=[0,0,0];for(let i=0;i<d.length;i+=4){const sample=d[i+(channel==='roughnessMap'?1:0)];mn=Math.min(mn,sample);mx=Math.max(mx,sample);for(let k=0;k<3;k++)mean[k]+=d[i+k]/(d.length/4);}maps.push({material:o.material.name,channel,width:im.width,height:im.height,range:mx-mn,mean});}});return {pyramids,terrain,maps,wrong}})()''')
 f=out['features'];assert len(f['pyramids'])==3 and len(f['terrain'])==1 and not f['wrong']
 assert {x['channel'] for x in f['maps']}=={'map','normalMap','roughnessMap'}
 assert all(x['range']>0 and max(x['width'],x['height'])<=512 for x in f['maps'])
 def palette(mean):
  r,g,bl=mean;assert 155<r<215 and 105<g<165 and 45<bl<105 and r>g>bl,'Ochre palette required'
 for x in f['maps']:
  if x['channel']=='map':palette(x['mean'])
 try:palette([50,150,50])
 except AssertionError:out['wrong_palette_negative_control']='PASS: green palette rejected'
 else:raise AssertionError('Wrong palette accepted')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'sudan-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
