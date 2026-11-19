from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'mozambique-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out=p.evaluate('''(()=>{let dunes=[],maps=[],seen=new Set();pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Dune')){let pos=o.geometry.attributes.position,v=pilot.root.position.clone(),lo=99,hi=-99;for(let i=0;i<pos.count;i++){v.fromBufferAttribute(pos,i).applyMatrix4(o.matrixWorld);lo=Math.min(lo,v.y);hi=Math.max(hi,v.y);}dunes.push({name:o.name,parent:o.parent.name,minY:lo,maxY:hi});}for(let key of ['map','roughnessMap','normalMap']){let t=o.material[key];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({material:o.material.name,kind:key,width:im.width,height:im.height,range:mx-mn});}});return {dunes,maps}})()''')
 def contract(v):
  assert len(v['dunes'])==3
  assert all(d['parent']=='Lid_Hinge' and .12<d['maxY']-d['minY']<.50 for d in v['dunes'])
  assert len(v['maps'])>=4 and all(m['range']>0 and max(m['width'],m['height'])<=512 for m in v['maps'])
 (R/'theme-observed.json').write_text(json.dumps(out,indent=2))
 contract(out)
 bad=dict(out,dunes=out['dunes'][:2])
 try:contract(bad)
 except AssertionError:out['missing_dune_negative_control']='REJECTED'
 else:raise AssertionError('Contract accepted missing dune')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']/2,y,steps=30);p.mouse.up();p.wait_for_timeout(300);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True);c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'mozambique-v1.html').as_uri());assert p.locator('#fallback').is_visible() and p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['result']='PASS';(R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
