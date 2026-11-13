from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
probe="""(()=>{let lid=[],body=[],maps=[],materials=[],wrong=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(o.name.startsWith('Lid_relief')){lid.push(o.name);if(o.parent.name!=='Lid_Hinge')wrong.push(o.name)}if(o.name.startsWith('Body_relief'))body.push(o.name);materials.push(o.material.name);if(o.material.map&&!seen.has(o.material.map.uuid)){seen.add(o.material.map.uuid);let im=o.material.map.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,c.width,c.height).data,mn=255,mx=0;for(let i=0;i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i])}maps.push({width:c.width,height:c.height,range:mx-mn})}});return {lid,body,maps,materials:[...new Set(materials)],wrong}})()"""
def check(d):
 assert len(d['lid'])==9 and len(d['body'])>=12 and not d['wrong'], 'Relief missing or detached'
 assert len(d['maps'])==3 and all(m['range']>10 and max(m['width'],m['height'])<=1024 for m in d['maps'])
 assert all(any(key in m for m in d['materials']) for key in ['Terracotta','Kaolin','Charcoal','Ochre','Brass'])
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True)
 c=b.new_context(offline=True);p=c.new_page();p.goto((R/'rwanda-v1.html').as_uri());p.wait_for_function('pilot.ready')
 d=p.evaluate(probe);check(d)
 assert 'Yakushima' not in p.locator('body').inner_text() and 'JAPAN' not in p.locator('body').inner_text()
 # Real runtime negative: remove one actual lid ornament and rerun same assertions.
 p.evaluate("(()=>{let target;pilot.root.traverse(o=>{if(o.name.startsWith('Lid_relief'))target=o});target.removeFromParent()})()")
 try:check(p.evaluate(probe));raise RuntimeError('Negative control failed to reject missing ornament')
 except AssertionError as e:negative=str(e)
 c.close();c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'rwanda-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'));c.close();b.close()
(R/'theme-check.json').write_text(json.dumps(dict(status='PASS',features=d,negative_control=negative,noJS_poster=True),indent=2));print('THEME PASS; missing-ornament negative rejected; NOJS PASS')
