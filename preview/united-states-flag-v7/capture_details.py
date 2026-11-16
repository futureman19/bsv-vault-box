from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageDraw
import io,json
R=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--allow-file-access-from-files'])
 c=b.new_context(offline=True,viewport=dict(width=1600,height=1200),device_scale_factor=2,reduced_motion='reduce');p=c.new_page()
 for version in ['v6','v7']:
  p.goto(((R/'baseline-v6' if version=='v6' else R)/f'united-states-flag-{version}.html').as_uri());p.wait_for_function('pilot.ready')
  for name,pos in [('front',[0,3,7.5]),('left',[-8.2,3,0]),('top',[0,9,.001]),('edge',[-6,6.5,9])]:
   p.evaluate('(v)=>pilot.camera.position.set(...v)',pos);p.wait_for_timeout(200)
   p.locator('#stage').screenshot(path=str(R/f'{version}-{name}-view.png'))
   if name in ['front','left']:
    # Actual browser pixels cropped to projected physical top-edge region.
    region=p.evaluate('''(face)=>{let points=face==='front'?[[-1.71,1.76,1.25],[-.28,2.02,1.25],[-1.71,2.02,.88],[-.28,1.76,.88]]:[[-1.9,1.76,-1.08],[-1.9,2.02,1.08],[-1.53,2.02,-1.08],[-1.53,1.76,1.08]];let a=points.map(p=>pilot.root.position.clone().set(...p).project(pilot.camera)),r=pilot.renderer.domElement.getBoundingClientRect();return {x:r.x+(Math.min(...a.map(p=>p.x))+1)/2*r.width-25,y:r.y+(1-Math.max(...a.map(p=>p.y)))/2*r.height-25,width:(Math.max(...a.map(p=>p.x))-Math.min(...a.map(p=>p.x)))/2*r.width+50,height:(Math.max(...a.map(p=>p.y))-Math.min(...a.map(p=>p.y)))/2*r.height+50}}''',name)
    p.screenshot(path=str(R/f'{version}-{name}-edge-detail.png'),clip=region)
  if version=='v7':
   for name in ['front','left']:
    Image.open(R/f'v7-{name}-view.png').save(R/f'band-{name}-close.png')
 b.close()
for face in ['front','left']:
 imgs=[Image.open(R/f'{v}-{face}-edge-detail.png').convert('RGB') for v in ['v6','v7']]
 width=max(i.width for i in imgs);height=sum(i.height+35 for i in imgs);out=Image.new('RGB',(width,height),(16,21,26));d=ImageDraw.Draw(out);y=0
 for v,im in zip(['V6 - separate small body stars, blank physical lid edge','V7 - same-scale continuous top / bevel / vertical edge stars'],imgs):
  d.text((12,y+8),v,fill='white');out.paste(im,(0,y+35));y+=im.height+35
 out.save(R/f'{face}-edge-comparison.png')
print('Actual browser top/front/left/edge and matching V6 crops captured')
