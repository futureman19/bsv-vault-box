from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
JS='''(()=>{let counts={lidScroll:0,bodyScroll:0,sideScroll:0,lattice:0,rim:0},maps=[],wrong=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;let key=o.name.startsWith('Lid_scroll')?'lidScroll':o.name.startsWith('Body_scroll')?'bodyScroll':o.name.startsWith('Side_scroll')?'sideScroll':o.name.startsWith('Lid_medallion')?(o.name.includes('lattice')?'lattice':'rim'):null;if(key)counts[key]++;if((key==='lidScroll'||key==='lattice'||key==='rim'||o.name.startsWith('Lid_felt'))&&o.parent.name!=='Lid_Hinge')wrong.push(o.name);for(let slot of ['map','roughnessMap']){let t=o.material[slot];if(!t||seen.has(t.uuid))continue;seen.add(t.uuid);let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let ctx=c.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,mn=255,mx=0;for(let i=(slot==='roughnessMap'?1:0);i<d.length;i+=4){mn=Math.min(mn,d[i]);mx=Math.max(mx,d[i]);}maps.push({slot,width:im.width,height:im.height,range:mx-mn});}});return {counts,maps,wrong}})()'''
def check(f):
 assert f['counts']==dict(lidScroll=8,bodyScroll=8,sideScroll=8,lattice=6,rim=1),f
 assert not f['wrong'],f
 assert len(f['maps'])==3 and all(m['range']>10 and max(m['width'],m['height'])<=512 for m in f['maps']),f
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page();p.goto((R/'kazakhstan-v1.html').as_uri());p.wait_for_function('pilot.ready')
 f=p.evaluate(JS);check(f)
 # Real scene mutation negative control: remove one required exported ornament.
 p.evaluate("let victim;pilot.root.traverse(o=>{if(o.name.startsWith('Lid_scroll'))victim=o});victim.removeFromParent()")
 negative=False
 try:check(p.evaluate(JS))
 except AssertionError:negative=True
 assert negative
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/'kazakhstan-v1.html').as_uri());assert p.locator('#fallback').is_visible();assert p.locator('#fallback').evaluate('(e)=>e.complete&&e.naturalWidth>0');p.screenshot(path=str(R/'mobile-nojs.png'),full_page=True);c.close();b.close()
 out={'status':'PASS','features':f,'removed_lid_scroll_negative_control_rejected':negative,'noJS_poster':True}
 (R/'theme-check.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
