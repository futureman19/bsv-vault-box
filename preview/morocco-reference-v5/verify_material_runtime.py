from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import json,numpy as np
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files']);c=b.new_context(offline=True);p=c.new_page();p.goto((R/'morocco-reference-v5.html').as_uri());p.wait_for_function('pilot.ready')
 result=p.evaluate('''(()=>{let out=[];pilot.root.traverse(o=>{if(!o.isMesh||!o.name.startsWith('Rose_stone'))return;let uv=o.geometry.attributes.uv;for(let i=0;i<uv.count;i++)if(!Number.isFinite(uv.getX(i))||!Number.isFinite(uv.getY(i)))throw Error('nonfinite uv');let m=o.material,im=m.normalMap.image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let d=ctx.getImageData(0,0,im.width,im.height).data,min=100,max=0;for(let i=0;i<d.length;i+=4){let length=Math.hypot(d[i]/127.5-1,d[i+1]/127.5-1,d[i+2]/127.5-1);min=Math.min(min,length);max=Math.max(max,length);}out.push({name:o.name,uvFinite:true,normalLengthMin:min,normalLengthMax:max,normalScale:m.normalScale.toArray(),roughnessMap:!!m.roughnessMap,baseMap:!!m.map});});return out})()''')
 assert len(result)==5
 for x in result:assert .98<x['normalLengthMin']<x['normalLengthMax']<1.02 and x['roughnessMap'] and x['baseMap'] and abs(x['normalScale'][0]-.8)<1e-6
 b.close()
(R/'runtime-material-check.json').write_text(json.dumps(result,indent=2));print(result)
# Comparison boards are produced by review.py from actual browser screenshots.
