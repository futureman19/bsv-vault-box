from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
out={}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'lesotho-v1.html').as_uri());p.wait_for_function('pilot.ready')
 out['features']=p.evaluate('''(()=>{let ridge=0,grass=0,panel=0,maps=[],wrong=[],uvBad=0;const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Maloti'))ridge++;if(o.name.startsWith('Highland'))grass++;if(o.name.startsWith('Lid__woven'))panel++;if(o.name.startsWith('Maloti')||o.name.startsWith('Highland')||o.name.startsWith('Lid__woven')){if(o.parent.name!=='Lid_Hinge')wrong.push(o.name);}for(let m of (Array.isArray(o.material)?o.material:[o.material]))for(let key of ['map','roughnessMap']){let t=m[key];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let uv=o.geometry.attributes.uv;if(!uv)uvBad++;else for(let i=0;i<uv.count;i++)if(!Number.isFinite(uv.getX(i)+uv.getY(i)))uvBad++;let im=t.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=0;i<d.length;i+=4){let v=d[i+(key==='roughnessMap'?1:0)];mn=Math.min(mn,v);mx=Math.max(mx,v);}maps.push({material:m.name,channel:key,width:im.width,height:im.height,range:mx-mn});}});return {ridge,grass,panel,maps,wrong,uvBad}})()''')
 # Multi-material glTF ridge is a group with four primitive mesh children.
 out['ridge_group']=p.evaluate("(()=>{let r=pilot.root.getObjectByName('Maloti__three_peak_ridge');return r?{parent:r.parent.name,meshChildren:r.children.filter(x=>x.isMesh).length}:null})()")
 f=out['features'];assert out['ridge_group'] and out['ridge_group']['parent']=='Lid_Hinge' and out['ridge_group']['meshChildren']==4 and f['grass']==19 and f['panel']==1 and not f['wrong'] and not f['uvBad'],out
 assert len(f['maps'])==3 and all(x['range']>10 and max(x['width'],x['height'])<=512 for x in f['maps'])
 p.locator('#open').click();p.wait_for_function('pilot.progress===1')
 box=p.locator('canvas').bounding_box();x=box['x']+box['width']*.5;y=box['y']+box['height']*.5
 p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.wait_for_timeout(150);p.screenshot(path=str(R/'desktop-open-rear.png'),full_page=True)
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'lesotho-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);out['noJS_poster']=True;c.close();b.close()
out['status']='PASS';(R/'extended-check.json').write_text(json.dumps(out,indent=2));print('EXTENDED PASS',json.dumps(out))
