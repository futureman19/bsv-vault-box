"""Real offline Edge GLTFLoader texture decoding, matched cameras and macro capture."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import json,struct,hashlib
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 browser=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 ctx=browser.new_context(viewport={'width':1440,'height':1080},offline=True,device_scale_factor=1)
 page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 cameras={}
 for label,path in [('before',R.parent/'iceland-pilot/iceland-pilot.html'),('after',R/'iceland-realism-v2.html')]:
  page.goto(path.as_uri());page.wait_for_function('pilot.ready===true');page.wait_for_timeout(300)
  cameras[label]={}
  for state in ['closed','open']:
   if state=='open':page.locator('#open').click();page.wait_for_function('pilot.progress===1');page.wait_for_timeout(100)
   cameras[label][state]=page.evaluate('({position:pilot.camera.position.toArray(),quaternion:pilot.camera.quaternion.toArray(),fov:pilot.camera.fov})')
   page.locator('#stage').screenshot(path=str(R/f'{label}-{state}-stage.png'))
  if label=='after':
   page.locator('#reset').click();page.wait_for_timeout(100)
   textures=page.evaluate("""(()=>{
    const out=[],seen=new Set();pilot.root.traverse(o=>{if(!o.isMesh)return;if(!o.geometry.attributes.uv)throw Error('Missing UV');let m=o.material;if(seen.has(m.uuid))return;seen.add(m.uuid);
    for(const k of ['map','normalMap','roughnessMap']){let t=m[k];if(!t)continue;let im=t.image,c=document.createElement('canvas');c.width=im.width;c.height=im.height;let x=c.getContext('2d',{willReadFrequently:true});x.drawImage(im,0,0);let a=x.getImageData(0,0,c.width,c.height).data;let sum=[0,0,0],sq=[0,0,0],n=a.length/4;for(let i=0;i<a.length;i+=4)for(let j=0;j<3;j++){sum[j]+=a[i+j];sq[j]+=a[i+j]**2;}out.push({material:m.name,slot:k,width:im.width,height:im.height,std:sum.map((s,j)=>Math.sqrt(sq[j]/n-(s/n)**2))});}
    });return out;})()""")
   assert len(textures)==12,textures
   for t in textures:
    assert t['width']>=1024 and t['height']>=1024
    if t['slot']=='normalMap':assert min(t['std'][:2])>1,t
    if t['slot']=='roughnessMap':assert t['std'][1]>3,t
   for name,pos,target in [('basalt-brass',[.65,1.75,3.6],[.05,.95,1.0]),('lid',[2.3,3.5,2.7],[0,1.55,0]),('hinge',[3.8,2.2,-3.0],[1.1,1.5,-1.2])]:
    page.evaluate('''([pos,target])=>{pilot.controls.minDistance=.3;pilot.camera.position.fromArray(pos);pilot.controls.target.fromArray(target);pilot.controls.update();}''',[pos,target]);page.wait_for_timeout(200)
    page.locator('#stage').screenshot(path=str(R/f'detail-{name}.png'))
 for state in ['closed','open']:
  for field in ['position','quaternion']:
   assert max(abs(a-b) for a,b in zip(cameras['before'][state][field],cameras['after'][state][field]))<1e-10,cameras
  assert cameras['before'][state]['fov']==cameras['after'][state]['fov']
 assert not errors
 browser.close()
for state in ['closed','open']:
 a=Image.open(R/f'before-{state}-stage.png').convert('RGB');b=Image.open(R/f'after-{state}-stage.png').convert('RGB');out=Image.new('RGB',(a.width+b.width,a.height+50),'#10151a');out.paste(a,(0,50));out.paste(b,(a.width,50));d=ImageDraw.Draw(out);d.text((25,16),'BEFORE / v1 - same camera',fill='white');d.text((a.width+25,16),'AFTER / v2 - actual textured GLB',fill='white');out.save(R/f'comparison-{state}.jpg',quality=94)
# Container inventory proves image bytes embedded rather than external URI dependencies.
b=(R/'iceland.glb').read_bytes();length=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+length]);assert len(g['images'])==12 and all('bufferView' in i and 'uri' not in i for i in g['images'])
report={'matched_cameras':cameras,'decoded_runtime_maps':textures,'embedded_images':len(g['images']),'texture_source_bytes':sum(p.stat().st_size for p in (R/'textures').glob('*.png')),'embedded_image_bytes':sum(g['bufferViews'][i['bufferView']]['byteLength'] for i in g['images']),'errors':errors,'scope':'Native Edge desktop and emulated mobile elsewhere, not a physical phone; procedural maps, not scans.'}
(R/'pbr-check.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
