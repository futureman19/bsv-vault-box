from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json
R=Path(__file__).resolve().parent
canvas=Image.new('RGB',(1500,1000),(17,21,25));report=[]
for i,(path,label) in enumerate([(R/'references/primary-morocco.png','PRIMARY CONCEPT'),(R/'matched-reference.png','ACTUAL AUTHORED 3D MODEL')]):
 im=Image.open(path).convert('RGB');a=np.asarray(im).astype(float);m=(a[:,:,0]>55)&(a[:,:,0]>a[:,:,1]*1.18)&(a[:,:,0]>a[:,:,2]*1.35);ys,xs=np.where(m);width=int(xs.max()-xs.min()+1);scale=650/width
 scaled=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);x=round(50-xs.min()*scale);y=round(820-ys.max()*scale)
 panel=Image.new('RGB',(750,1000),(17,21,25));panel.paste(scaled,(x,y));ImageDraw.Draw(panel).text((45,30),label,fill=(222,207,178));canvas.paste(panel,(i*750,0));report.append({'image':path.name,'warm_object_bounds':[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],'uniform_scale':scale,'target_object_width':650})
ImageDraw.Draw(canvas).text((45,950),'Equal warm-object silhouette width, uniform scaling only. Perspective and lighting differ; no warping.',fill=(208,208,208));canvas.save(R/'reference-comparison.jpg',quality=93)
(R/'comparison-method.json').write_text(json.dumps(report,indent=2))
top=Image.open(R/'top-down-source.png').convert('RGB');d=ImageDraw.Draw(top);d.text((340,30),'BACK +Y / REAR HINGES',fill=(245,225,160));d.text((340,855),'FRONT -Y / LATCH',fill=(245,225,160));d.text((740,450),'RIGHT +X',fill=(245,225,160));x=450+.10*900/4.7;y=450-1.04*900/4.7;d.ellipse((x-15,y-15,x+15,y+15),outline=(255,215,60),width=3);d.text((x+22,y-12),'Atlas centre (+.10,+1.04)',fill=(255,225,170));top.save(R/'top-down-diagnostic.png')
