from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(channel='msedge',headless=True)
 c=b.new_context(offline=True);page=c.new_page();page.goto((R/'bulgaria-v1.html').as_uri());page.wait_for_function('pilot.ready')
 result=page.evaluate('''()=>{const out=[];const seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;for(const m of (Array.isArray(o.material)?o.material:[o.material])){for(const slot of ['map','roughnessMap']){const t=m[slot];if(!t||seen.has(t.uuid+slot))continue;seen.add(t.uuid+slot);const canvas=document.createElement('canvas');canvas.width=t.image.width;canvas.height=t.image.height;const ctx=canvas.getContext('2d');ctx.drawImage(t.image,0,0);const d=ctx.getImageData(0,0,canvas.width,canvas.height).data;let min=255,max=0;for(let i=slot==='roughnessMap'?1:0;i<d.length;i+=4){min=Math.min(min,d[i]);max=Math.max(max,d[i]);}out.push({material:m.name,slot,width:canvas.width,height:canvas.height,range:max-min});}}});return out;}''')
 assert len(result)>=4
 assert all(0<x['range'] and x['width']<=512 and x['height']<=512 for x in result)
 text=page.locator('body').inner_text();assert 'Rose Valley' in text and 'Yakushima' not in text and 'Japan' not in text
 assert 'Bulgaria' in page.locator('canvas').get_attribute('aria-label')
 b.close()
(R/'material-check.json').write_text(json.dumps({'status':'PASS','decoded_actual_loader_maps':result,'copy_and_aria':'PASS'},indent=2));print('MATERIAL_CHECK PASS')
