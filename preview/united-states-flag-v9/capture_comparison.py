from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import math,json
R=Path(__file__).resolve().parent
ref=Path('C:/Users/futur/.hermes/profiles/telegram2/output/boxsv-usa-flag-fireworks/united-states-flag-fireworks.png')
entries=[('Marketing illustration',ref,(114,301,957,905))];bounds=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport=dict(width=1440,height=1080),device_scale_factor=1,reduced_motion='reduce');p=c.new_page()
 for version in ['v8','v9']:
  folder=R if version=='v9' else Path('C:/Users/futur/Desktop/bsv-vault-box/.worktrees/usa-flag-v8/preview/united-states-flag-v8')
  p.goto((folder/f'united-states-flag-{version}.html').as_uri());p.wait_for_function('pilot.ready');p.wait_for_timeout(300)
  rect=p.locator('canvas').bounding_box()
  box=p.evaluate('''()=>{let x0=1,y0=1,x1=-1,y1=-1;pilot.root.updateMatrixWorld(true);pilot.root.traverse(o=>{if(!o.isMesh)return;let a=o.geometry.attributes.position,v=pilot.root.position.clone();for(let i=0;i<a.count;i++){v.fromBufferAttribute(a,i).applyMatrix4(o.matrixWorld).project(pilot.camera);x0=Math.min(x0,v.x);x1=Math.max(x1,v.x);y0=Math.min(y0,v.y);y1=Math.max(y1,v.y)}});return [x0,y0,x1,y1]}''')
  crop=(math.floor(rect['x']+(box[0]+1)*rect['width']/2),math.floor(rect['y']+(1-box[3])*rect['height']/2),math.ceil(rect['x']+(box[2]+1)*rect['width']/2),math.ceil(rect['y']+(1-box[1])*rect['height']/2))
  dest=R/f'comparison-{version}-browser.png';p.screenshot(path=str(dest),full_page=True);entries.append((f'{version.upper()} actual browser',dest,crop));bounds.append(dict(version=version,pixel_crop=crop,projected_ndc=box))
  if version=='v9':
   for name,pos in [('front',[0,2.6,6]),('left',[-6,2.6,0]),('top',[0,8,.001])]:
    p.evaluate('(v)=>pilot.camera.position.set(...v)',pos);p.wait_for_timeout(300);p.locator('#stage').screenshot(path=str(R/f'v9-{name}-view.png'))
    if name!='top':
     p.locator('#open').click();p.wait_for_function('pilot.progress===1');p.wait_for_timeout(150);p.locator('#stage').screenshot(path=str(R/f'v9-{name}-open.png'));p.locator('#reset').click();p.wait_for_function('pilot.progress===0')
 c.close();b.close()
board=Image.new('RGB',(1920,600),(16,21,26));d=ImageDraw.Draw(board)
for i,(label,path,crop) in enumerate(entries):
 im=Image.open(path).convert('RGB').crop(crop);h=round(im.height*600/im.width);im=im.resize((600,h),Image.Resampling.LANCZOS);board.paste(im,(i*640+20,80));d.text((i*640+20,20),label,fill='white')
d.text((20,560),'Equal chest width (600 px); original aspect ratios preserved. Illustration is reference, not model output.',fill='white')
board.save(R/'primary-v8-v9-comparison.jpg',quality=94)
(R/'comparison-check.json').write_text(json.dumps(dict(reference_crop=[114,301,957,905],reference_native_size=Image.open(ref).size,actual_model_bounds=bounds,equal_width=600,warped=False),indent=2))
