"""Independent portable-material, normal and same-presentation comparison gates."""
from pathlib import Path
import json,struct,hashlib,base64,re
from PIL import Image,ImageDraw,ImageFont
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parent
old=R.parent/'iceland-reference-v5'
def gltf(p):
 b=p.read_bytes();n=struct.unpack_from('<I',b,12)[0];return json.loads(b[20:20+n])
g=gltf(R/'iceland.glb');mats={m['name']:m for m in g['materials']}
assert abs(mats['Glacier translucent cyan']['extensions']['KHR_materials_transmission']['transmissionFactor']-.68)<1e-6
assert mats['Polished black obsidian']['pbrMetallicRoughness']['roughnessFactor']<.1
assert (R/'motion.mjs').read_bytes()==(old/'motion.mjs').read_bytes()
# Actual baseline GLB under the candidate camera, lights and runtime, not an old differently lit poster.
h=(R/'iceland-polished-v6.html').read_text(encoding='utf8');b64=base64.b64encode((R/'iceland.glb').read_bytes()).decode();h=h.replace(b64,base64.b64encode((old/'iceland.glb').read_bytes()).decode());control=R/'baseline-control.html';control.write_text(h,encoding='utf8')
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport={'width':1440,'height':1080});p=c.new_page()
 for label,path in [('v5',control),('v6',R/'iceland-polished-v6.html')]:
  p.goto(path.as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(500)
  normals=p.evaluate('''(()=>{let count=0,bad=0;pilot.root.traverse(o=>{if(!o.isMesh)return;let n=o.geometry.attributes.normal;for(let i=0;i<n.count;i++){let l=Math.hypot(n.getX(i),n.getY(i),n.getZ(i));count++;if(!Number.isFinite(l)||Math.abs(l-1)>.001)bad++}});return {count,bad}})()''');assert normals['bad']==0
  p.locator('#stage').screenshot(path=str(R/(label+'-matched.png')))
  if label=='v6':
   p.evaluate('pilot.camera.position.sub({x:0,y:.95,z:0}).multiplyScalar(.65).add({x:0,y:.95,z:0});pilot.camera.updateMatrixWorld()');p.wait_for_timeout(200);p.locator('#stage').screenshot(path=str(R/'closeup.png'))
 c.close();b.close()
control.unlink()
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',24)
board=Image.new('RGB',(1800,820),'#10151a');d=ImageDraw.Draw(board)
for i,label in enumerate(['v5','v6']):
 im=Image.open(R/(label+'-matched.png')).convert('RGB');im.thumbnail((880,720));board.paste(im,(i*900+10,60));d.text((i*900+20,20),label.upper()+' / actual GLB, identical camera and lighting',font=font,fill='white')
d.text((20,770),'V6: taller body, fine crevice growth, thinner rounded guards, finer clearer ice. Original motion.',font=font,fill='white');board.save(R/'before-after.jpg',quality=93)
# Replace inherited annotations with candid v6 notes.
ref=Image.open('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-iceland-promotional/iceland-promotional.png').convert('RGB').crop((140,270,890,810));actual=Image.open(R/'actual-model-crop.png').convert('RGB')
board=Image.new('RGB',(1600,850),'#10151a');d=ImageDraw.Draw(board)
for i,(im,title) in enumerate([(ref,'PROMO / AI concept'),(actual,'V6 / actual offline model')]):
 im=im.resize((740,round(im.height*740/im.width)));board.paste(im,(30+800*i,90));d.text((30+800*i,30),title,font=font,fill='white')
for i,line in enumerate(['Equal object width; perspective estimated, not calibrated. Body raised 0.168; width unchanged.','Fine moss replaces beads; ice transmission 0.68; thinner, rounded sheet guards.','Still stylized: angular basalt, sparse growth, simplified river cascade and studio reflections.']):d.text((25,710+i*38),line,font=font,fill='white')
board.save(R/'reference-comparison.jpg',quality=93)
(R/'polish-check.json').write_text(json.dumps({'normal_checks':normals,'material_records':mats,'motion_byte_identical_v5':True,'same_camera_lighting_AB':True,'body_rise':.168,'width_unchanged':True,'reference_note':'equal-width visual assessment, not metric camera recovery'},indent=2))
print('POLISH_PASS',normals)
