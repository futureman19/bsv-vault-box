from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np
R=Path(__file__).resolve().parent; (R/'maps').mkdir(exist_ok=True)
n=512; im=Image.new('RGB',(n,n),(239,233,216));d=ImageDraw.Draw(im)
# Original four-petal medallion and corner scrolls, not a copied historic pattern.
d.rectangle((0,0,511,511),outline=(202,193,171),width=9)
d.rectangle((18,18,493,493),outline=(35,78,132),width=5)
for box in [(190,100,322,280),(190,232,322,412),(100,190,280,322),(232,190,412,322)]:
 d.ellipse(box,fill=(29,72,127),outline=(19,52,98),width=7)
for box in [(215,128,297,267),(215,245,297,384),(128,215,267,297),(245,215,384,297)]:d.ellipse(box,fill=(222,229,221))
d.ellipse((220,220,292,292),fill=(24,61,114));d.ellipse((240,240,272,272),fill=(237,232,213))
for x,y in [(55,55),(457,55),(55,457),(457,457)]:
 d.ellipse((x-25,y-25,x+25,y+25),outline=(29,72,127),width=9)
 d.arc((x-48,y-48,x+48,y+48),0,280,fill=(47,94,149),width=5)
a=np.array(im).astype(float); rng=np.random.default_rng(420);noise=rng.normal(0,1.2,(n,n,1));a=np.clip(a+noise,0,255).astype('uint8');Image.fromarray(a).save(R/'maps/tile-color.png')
r=np.full((n,n),70,dtype=float)+rng.normal(0,2,(n,n));r[:9,:]=150;r[-9:,:]=150;r[:,:9]=150;r[:,-9:]=150;Image.fromarray(r.clip(0,255).astype('uint8')).convert('RGB').save(R/'maps/tile-roughness.png')
h=np.ones((n,n));h[:9,:]=0;h[-9:,:]=0;h[:,:9]=0;h[:,-9:]=0;h=np.array(Image.fromarray((h*255).astype('uint8')).filter(ImageFilter.GaussianBlur(3))).astype(float)/255
gy,gx=np.gradient(h);normal=np.stack([-gx*.6,-gy*.6,np.ones_like(h)],axis=-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True);Image.fromarray(((normal*.5+.5)*255).astype('uint8')).save(R/'maps/tile-normal.png')
print('MAPS PASS: original 512px ceramic color/roughness/normal')
