"""Generated atmospheric painting, compact wrap repair, conservative maps. No NASA pixels."""
from pathlib import Path
from PIL import Image,ImageFilter,ImageEnhance,ImageDraw
import numpy as np,json
R=Path(__file__).resolve().parent;M=R/'maps';M.mkdir(exist_ok=True)
master=Image.open(R/'references/generated-cloud-master.png').convert('RGB')
a=np.asarray(master.resize((1024,256),Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(.65)),dtype=float)
# One targeted post-model correction: advect the painted clouds through sparse
# elliptical shear cells. This warps existing imagery, not synthetic stripe/noise generation.
Y,X=np.mgrid[:256,:1024];sx=X.astype(float);sy=Y.astype(float)
for cx,cy,rx,ry,turn in [(480,99,116,50,1.15),(615,171,85,33,-1.1),(265,144,130,46,.85),(810,63,115,39,-.8)]:
 dx=(X-cx)/rx;dy=(Y-cy)/ry;q=dx*dx+dy*dy;theta=turn*np.exp(-q*1.5)
 sx+=(dx*np.cos(theta)-dy*np.sin(theta)-dx)*rx
 sy+=(dx*np.sin(theta)+dy*np.cos(theta)-dy)*ry
sx=np.clip(sx,0,1022.999);sy=np.clip(sy,0,254.999)
x0=sx.astype(int);y0=sy.astype(int);fx=(sx-x0)[...,None];fy=(sy-y0)[...,None]
a=(a[y0,x0]*(1-fx)+a[y0,x0+1]*fx)*(1-fy)+(a[y0+1,x0]*(1-fx)+a[y0+1,x0+1]*fx)*fy
# Two bounded swatches of the same generated painting: quiet and stronger zonal contrast.
# Emphasize broad row structure instead of introducing any repeated sine/noise bands.
row=np.asarray(Image.fromarray(np.uint8(a)).resize((1,256),Image.Resampling.BOX).filter(ImageFilter.GaussianBlur(2)),dtype=float)
candidates=[]
for name,strength in [('A',.10),('B',.48)]:
 c=a+(row-row.mean(axis=0,keepdims=True))*strength
 # Repair horizontal seam over 96 pixels with a smooth endpoint blend.
 target=(c[:,:1]+c[:,-1:])/2
 for i in range(96):
  t=(1-i/95)**2*(1+2*i/95)
  c[:,i]=c[:,i]*(1-t)+target[:,0]*t
  c[:,-1-i]=c[:,-1-i]*(1-t)+target[:,0]*t
 c=np.uint8(np.clip(c,0,255));c[:,-1]=c[:,0]
 im=Image.fromarray(c);im.save(R/f'swatch-{name}.png');candidates.append(im)
board=Image.new('RGB',(1024,560),'#222222');d=ImageDraw.Draw(board)
for i,im in enumerate(candidates):board.paste(im,(0,i*280+24));d.text((12,i*280+5),['A: quiet zones','B: strengthened broad zones, same sparse cloud painting'][i],fill='white')
board.save(R/'swatches.png')
# B chosen after visual review; lossless color guarantees identical seam endpoints.
c=candidates[1];c.save(M/'saturn-color.png',optimize=True)
# Cloud coloration is not embossed rock. Only tiny smooth tonal relief.
g=np.asarray(c.convert('L').filter(ImageFilter.GaussianBlur(1.2)),dtype=float)/255
h=(g-np.asarray(c.convert('L').filter(ImageFilter.GaussianBlur(5)),dtype=float)/255)*.10
dy,dx=np.gradient(h)
# Cap tangent slopes at 0.05 (under 3 degrees): gentle relief, never gritty pits.
dx*=.05/max(float(np.abs(dx).max()),1e-12);dy*=.05/max(float(np.abs(dy).max()),1e-12)
n=np.stack([-dx,dy,np.ones_like(dx)],-1);n/=np.linalg.norm(n,axis=-1,keepdims=True)
normal=np.uint8(np.clip((n*.5+.5)*255,0,255));normal[:,-1]=normal[:,0]
Image.fromarray(normal).save(M/'saturn-normal.png',optimize=True)
rough=np.uint8((.70+(g-g.min())/(g.max()-g.min())*.065)*255)
orm=np.stack([np.full_like(rough,255),rough,np.zeros_like(rough)],-1);orm[:,-1]=orm[:,0]
Image.fromarray(orm).save(M/'saturn-orm.png',optimize=True)
result={'strategy':'AI generated flat cloud painting; broad-zone contrast B; one targeted four-cell localized shear correction; restrained smoothing and 96px periodic seam repair. No procedural band synthesis or granular pits.','selected':'B','dimensions':[1024,256],'color_seam_max':int(np.abs(np.asarray(c,dtype=int)[:,0]-np.asarray(c,dtype=int)[:,-1]).max()),'normal_strength':.8,'normal_note':'Near-flat portable tangent normal; no rocky relief','roughness_range':[int(rough.min()),int(rough.max())],'maps':{p.name:p.stat().st_size for p in M.iterdir()}}
(R/'material-provenance.json').write_text(json.dumps(result,indent=2));print(result)
