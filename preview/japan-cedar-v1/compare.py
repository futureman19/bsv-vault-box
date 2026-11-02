from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
R=Path(__file__).resolve().parent
ref=R/'references/primary-japan.png'
# Uniform scaling only; normalize measured warm-wood silhouette width.
canvas=Image.new('RGB',(1500,950),(17,21,25));draw=ImageDraw.Draw(canvas);report=[]
for i,(path,label) in enumerate([(ref,'PRIMARY MARKETING CONCEPT'),(R/'matched-reference.png','ACTUAL AUTHORED 3D MODEL')]):
 im=Image.open(path).convert('RGB');a=np.asarray(im).astype(float);m=(a[:,:,0]>65)&(a[:,:,0]>a[:,:,1]*1.28)&(a[:,:,0]>a[:,:,2]*1.5);ys,xs=np.where(m);width=int(xs.max()-xs.min()+1);scale=650/width
 scaled=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);x=round(i*750+50-xs.min()*scale);y=round(780-ys.max()*scale);canvas.paste(scaled,(x,y));draw.text((i*750+45,30),label,fill=(222,207,178));report.append({'image':path.name,'wood_bounds':[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],'uniform_scale':scale,'target_wood_width':650})
draw.text((45,900),'Same front-left orientation; equal measured wood width. Perspective/lighting differ. No warping.',fill=(208,208,208));canvas.save(R/'reference-comparison.jpg',quality=93)
(R/'comparison-method.json').write_text(json.dumps(report,indent=2))
# Top-down camera is +Z with +Y upward; label physical rather than screen corners.
top=Image.open(R/'top-down-source.png').convert('RGB');d=ImageDraw.Draw(top)
d.text((350,30),'BACK +Y / REAR HINGES',fill=(245,225,160));d.text((350,855),'FRONT -Y / LATCH',fill=(245,225,160));d.text((725,450),'RIGHT +X',fill=(245,225,160))
x=450+.62*900/4.7;y=450-.78*900/4.7;d.ellipse((x-14,y-14,x+14,y+14),outline=(255,215,60),width=3);d.text((x+22,y-12),'Trunk (+0.62, +0.78)',fill=(255,225,170));top.save(R/'top-down-diagnostic.png')
