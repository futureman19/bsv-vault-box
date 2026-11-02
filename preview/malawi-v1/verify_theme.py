from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent

def validate(d):
 assert d['boulders']==4 and d['bodies']==3 and d['tails']==3,d
 assert d['lake']==1 and d['shore']==1 and not d['wrong'] and not d['obsolete'],d
 assert len(d['maps'])==3 and all(max(m['width'],m['height'])<=512 and m['range']>0 for m in d['maps']),d
 assert 3.7<d['width']<4.0 and 1.8<d['height']<3.1,d

with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'malawi-v1.html').as_uri());p.wait_for_function('pilot.ready')
 d=p.evaluate('''(()=>{let d={boulders:0,bodies:0,tails:0,lake:0,shore:0,wrong:[],obsolete:[],maps:[]};let seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;let n=o.name;if(n.startsWith('Shore_boulder'))d.boulders++;if(n.startsWith('Cichlid__body'))d.bodies++;if(n.startsWith('Cichlid__tail'))d.tails++;if(n.startsWith('Lake__enamel'))d.lake++;if(n.startsWith('Shore__sandy'))d.shore++;if(/^(Shore|Cichlid|Lake)/.test(n)&&o.parent.name!=='Lid_Hinge')d.wrong.push(n);if(/Cedar|foliage|moss/i.test(n))d.obsolete.push(n);for(let key of ['map','normalMap','roughnessMap']){let t=o.material[key];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let a=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=key==='roughnessMap'?1:0;i<a.length;i+=4){mn=Math.min(mn,a[i]);mx=Math.max(mx,a[i])}d.maps.push({key,width:c.width,height:c.height,range:mx-mn})}});d.width=pilot.asset.bounds.max[0]-pilot.asset.bounds.min[0];d.height=pilot.asset.bounds.max[1]-pilot.asset.bounds.min[1];return d})()''')
 (R/'theme-observed.json').write_text(json.dumps(d,indent=2));validate(d)
 bad=dict(d,boulders=0)
 try:validate(bad)
 except AssertionError:negative=True
 else:raise AssertionError('Negative control wrongly passed')
 p.locator('#open').click();p.wait_for_function('pilot.progress===1');box=p.locator('canvas').bounding_box();x=box['x']+box['width']/2;y=box['y']+box['height']/2;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+box['height']*.5,y,steps=30);p.mouse.up();p.screenshot(path=str(R/'desktop-open-rear.png'));c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'malawi-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));c.close();b.close()
(R/'theme-check.json').write_text(json.dumps({'status':'PASS','observed':d,'missing_boulders_negative_control_rejected':negative,'no_js_poster':True},indent=2));print('THEME PASS; negative control rejected; NO-JS PASS')
