from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw,ImageFont
import json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page()
 for version,folder in [('v8',R.parent/'iceland-stone-ice-v8'),('v9',R)]:
  p.goto((folder/(folder.name+'.html')).as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(700)
  p.locator('#stage').screenshot(path=str(R/(version+'-matched.png')))
  if version=='v9':
   result=p.evaluate('''(()=>{let corners=[],ice=[],materials={},maps=[];let V=pilot.root.position.constructor;pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(!o.isMesh)return;let m=o.material;materials[m.name]={color:m.color.toArray(),roughness:m.roughness,transmission:m.transmission||0,ior:m.ior,thickness:m.thickness||0,attenuationDistance:m.attenuationDistance,attenuationColor:m.attenuationColor?.toArray()};if(o.name.startsWith('Corner_strap')&&o.name.includes('folded_top')||o.name.startsWith('Corner strap')&&o.name.includes('folded top')){let a=o.geometry.attributes.position,v=new V(),center=new V();for(let i=0;i<a.count;i++){v.fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld);center.add(v)}center.divideScalar(a.count);corners.push({name:o.name,world:center.toArray(),ndc:center.clone().project(pilot.camera).toArray()})}if(o.name.startsWith('Glacier')){let a=o.geometry.attributes.position;for(let i=0;i<a.count;i++)ice.push(new V().fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld).project(pilot.camera).toArray())}for(let k of ['map','normalMap','roughnessMap'])if(m[k]&&!maps.some(t=>t.uuid===m[k].uuid)){let im=m[k].image,canvas=document.createElement('canvas');canvas.width=im.width;canvas.height=im.height;let ctx=canvas.getContext('2d');ctx.drawImage(im,0,0);let data=ctx.getImageData(0,0,im.width,im.height).data,min=255,max=0;for(let i=0;i<data.length;i++){if(i%4===3)continue;min=Math.min(min,data[i]);max=Math.max(max,data[i])}maps.push({uuid:m[k].uuid,kind:k,width:im.width,height:im.height,min,max})}});return {corners,iceBounds:{min:[0,1].map(j=>Math.min(...ice.map(v=>v[j]))),max:[0,1].map(j=>Math.max(...ice.map(v=>v[j])))},materials,maps,camera:pilot.camera.position.toArray(),exposure:pilot.renderer.toneMappingExposure}})()''')
   assert len(result['corners'])==4,result['corners']
   ice=result['iceBounds'];right=max(result['corners'],key=lambda q:q['ndc'][0]);icex=(ice['min'][0]+ice['max'][0])/2
   # Center lies within the rightmost quarter of projected corner span.
   left=min(q['ndc'][0] for q in result['corners']);fraction=(icex-left)/(right['ndc'][0]-left);assert fraction>.8,fraction
   result['projected_glacier_fraction_left_to_right']=fraction;result['nearest_screen_corner']=right
   mat=result['materials']['Glacier / blue depth'];assert mat['transmission']>.95 and mat['roughness']<.04 and mat['thickness']>.1 and abs(mat['ior']-1.31)<.001
   assert all(max(m['color'])<.4 for n,m in result['materials'].items() if n.startswith('Basalt /'))
   assert len(result['maps'])>=3 and all(m['max']>m['min'] for m in result['maps'])
   box=p.evaluate('''(()=>{let a=[1,1],b=[-1,-1],v=pilot.root.position.clone();pilot.root.traverse(o=>{if(!o.isMesh)return;let p=o.geometry.attributes.position;for(let i=0;i<p.count;i++){v.fromBufferAttribute(p,i).applyMatrix4(o.matrixWorld).project(pilot.camera);a[0]=Math.min(a[0],v.x);a[1]=Math.min(a[1],v.y);b[0]=Math.max(b[0],v.x);b[1]=Math.max(b[1],v.y)}});return {a,b}})()''')
   image=Image.open(R/'v9-matched.png');w,h=image.size;a=box['a'];z=box['b'];image.crop((int((a[0]+1)*w/2)-8,int((1-z[1])*h/2)-8,int((z[0]+1)*w/2)+8,int((1-a[1])*h/2)+8)).save(R/'actual-model-crop.png')
   (R/'v9-runtime-check.json').write_text(json.dumps(result,indent=2))
  # Same pose/camera/exposure for both versions; zoom for actual material/corner detail.
  p.evaluate('pilot.camera.position.set(-3.3,3.0,4.7);pilot.camera.lookAt(0,1.5,0)');p.wait_for_timeout(500);p.locator('#stage').screenshot(path=str(R/(version+'-detail.png')))
  p.evaluate('pilot.camera.position.set(4,3.2,-5);pilot.camera.lookAt(0,1.4,0)');p.wait_for_timeout(500);p.locator('#stage').screenshot(path=str(R/(version+'-rear.png')))
  p.evaluate('window.requestAnimationFrame=()=>0');p.wait_for_timeout(150)
  p.evaluate('pilot.camera.position.set(2.1,2.85,2.7);pilot.camera.lookAt(1.2,2.05,.8);pilot.renderer.render(pilot.root.parent,pilot.camera)');p.locator('#stage').screenshot(path=str(R/(version+'-glacier-macro.png')))
 c.close()
 c=b.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844});p=c.new_page();p.goto((R/(R.name+'.html')).as_uri());assert p.locator('#fallback').is_visible() and p.locator('#open').is_disabled();assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');p.screenshot(path=str(R/'no-js.png'),full_page=True);c.close();b.close()
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',22)
for view in ['matched','detail','rear']:
 a=Image.open(R/('v8-'+view+'.png')).convert('RGB');z=Image.open(R/('v9-'+view+'.png')).convert('RGB');a.thumbnail((800,650));z.thumbnail((800,650));board=Image.new('RGB',(1600,740),'#10151a');d=ImageDraw.Draw(board)
 for i,(im,label) in enumerate([(a,'V8 / actual offline model'),(z,'V9 / actual offline model')]):board.paste(im,(i*800,50));d.text((i*800+20,16),label,font=font,fill='white')
 d.text((20,690),'Same camera, lighting and exposure. V9 glass does not cast opaque shadow-map shadows.',font=font,fill='white');board.save(R/('before-after-'+view+'.jpg'),quality=92)
ref=Image.open('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-iceland-promotional/iceland-promotional.png').convert('RGB').crop((140,270,890,810));im=Image.open(R/'actual-model-crop.png').convert('RGB')
board=Image.new('RGB',(1600,800),'#10151a');d=ImageDraw.Draw(board)
for i,(img,label) in enumerate([(ref,'Primary / AI promotional artwork'),(im,'V9 / actual offline browser model')]):
 img=img.resize((740,round(img.height*740/img.width)),Image.Resampling.LANCZOS);board.paste(img,(20+i*800,70));d.text((20+i*800,20),label,font=font,fill='white')
d.text((20,730),'User-directed FAR RIGHT placement overrides central glacier in promotional artwork.',font=font,fill='white');board.save(R/'reference-comparison.jpg',quality=92)
print('V9_RUNTIME_VIEWS_PASS',result['projected_glacier_fraction_left_to_right'])
