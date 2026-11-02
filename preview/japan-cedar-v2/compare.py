from pathlib import Path
from PIL import Image,ImageDraw
import json,numpy as np
R=Path(__file__).resolve().parent
# Identical unmodified default camera/light/viewport; crops have equal native pixels.
canvas=Image.new('RGB',(1440,640),(16,21,26));draw=ImageDraw.Draw(canvas)
for i,tag in enumerate(['before','after']):
 im=Image.open(R/f'{tag}-desktop.png').convert('RGB');crop=im.crop((360,275,1080,865));canvas.paste(crop,(i*720,45));draw.text((i*720+25,15),('V1 / APPROVED BASELINE' if i==0 else 'V2 / FULLER CEDAR + MOSS'),fill=(235,220,185))
canvas.save(R/'before-after.jpg',quality=94)
canvas=Image.new('RGB',(780,884),(16,21,26));d=ImageDraw.Draw(canvas)
for i,tag in enumerate(['before','after']):canvas.paste(Image.open(R/f'{tag}-mobile.png').convert('RGB'),(390*i,40));d.text((390*i+15,12),'V1 baseline' if i==0 else 'V2 refinement',fill=(235,220,185))
canvas.save(R/'mobile-before-after.jpg',quality=94)
# Reference vs actual at equal measured wood width; explicit different lighting/camera.
canvas=Image.new('RGB',(1500,950),(17,21,25));draw=ImageDraw.Draw(canvas);report=[]
for i,(path,label) in enumerate([(R/'references/primary-japan.png','PRIMARY MARKETING CONCEPT'),(R/'matched-reference.png','ACTUAL V2 MODEL / BLENDER RENDER')]):
 im=Image.open(path).convert('RGB');a=np.asarray(im).astype(float);m=(a[:,:,0]>65)&(a[:,:,0]>a[:,:,1]*1.28)&(a[:,:,0]>a[:,:,2]*1.5);ys,xs=np.where(m);width=int(xs.max()-xs.min()+1);scale=650/width
 scaled=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);canvas.paste(scaled,(round(i*750+50-xs.min()*scale),round(780-ys.max()*scale)));draw.text((i*750+45,30),label,fill=(222,207,178));report.append({'image':path.name,'wood_bounds':[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],'uniform_scale':scale,'target_wood_width':650})
draw.text((45,900),'Same front-left direction; equal measured wood width. Camera/lighting differ. Not a same-camera proof.',fill=(208,208,208));canvas.save(R/'reference-comparison.jpg',quality=93)
(R/'comparison-method.json').write_text(json.dumps({'before-after':'native equal crops, identical default browser camera and lighting, no scaling','reference-comparison':report},indent=2))
