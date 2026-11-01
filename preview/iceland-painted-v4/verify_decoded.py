from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files']);c=b.new_context(offline=True);p=c.new_page();p.goto((R/'iceland-painted-v4.html').as_uri());p.wait_for_function('pilot.ready')
 result=p.evaluate('''(()=>{let seen=new Set(),out=[];pilot.root.traverse(o=>{if(!o.isMesh||!o.material.map)return;let m=o.material,uv=o.geometry.attributes.uv;for(let i=0;i<uv.count;i++){if(!Number.isFinite(uv.getX(i))||uv.getX(i)<0||uv.getX(i)>1||uv.getY(i)<0||uv.getY(i)>1)throw Error('invalid UV');}if(seen.has(m.name))return;seen.add(m.name);let canvas=document.createElement('canvas');canvas.width=m.map.image.width;canvas.height=m.map.image.height;let ctx=canvas.getContext('2d');ctx.drawImage(m.map.image,0,0);let d=ctx.getImageData(0,0,canvas.width,canvas.height).data,min=255,max=0,green=0;for(let i=0;i<d.length;i+=4){min=Math.min(min,d[i]);max=Math.max(max,d[i]);if(d[i+1]>d[i]*1.12&&d[i+1]>d[i+2]*1.3)green++;}out.push({name:m.name,width:canvas.width,height:canvas.height,redMin:min,redMax:max,greenPixels:green,uvChecked:true});});return out;})()''')
 assert len(result)==6 and all(x['width']==1024 and x['redMax']-x['redMin']>80 and x['greenPixels']>1000 for x in result)
 b.close()
(R/'decoded-map-check.json').write_text(json.dumps(result,indent=2));print('PASS actual browser-decoded map pixels + every textured primitive UV')
