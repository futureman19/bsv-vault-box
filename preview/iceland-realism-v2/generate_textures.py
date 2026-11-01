"""Deterministic multiscale PROCEDURAL PBR maps. No photographic scans or downloads.
RGB normals are tangent-space OpenGL (+Y), roughness linear grayscale.
2K stone/lid/brass enable millimetric detail in close inspection; 1K liner.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json
R=Path(__file__).resolve().parent/'textures';R.mkdir(exist_ok=True)
rng=np.random.default_rng(7319)
def noise(n,grid):
 a=rng.random((grid,grid)).astype('float32');return np.asarray(Image.fromarray(a).resize((n,n),Image.Resampling.BICUBIC)).copy()
def save(f,k,a):Image.fromarray(np.uint8(np.clip(a,0,1)*255)).save(R/f'{f}-{k}.png',compress_level=7)
def maps(f,n):
 broad=noise(n,9)-.5;mid=noise(n,63)-.5;grain=noise(n,440)-.5;fine=rng.random((n,n)).astype('float32')-.5
 h=.3*mid+.13*grain+.025*fine
 if f=='basalt':
  # Small vesicles and discontinuous fine fractures rather than giant craters.
  pit=Image.new('L',(n,n));d=ImageDraw.Draw(pit)
  for _ in range(2400):
   x,y=rng.integers(0,n,2);radius=int(rng.choice([1,2,3,4],p=[.4,.35,.2,.05]));d.ellipse((x,y,x+radius*2,y+radius),fill=int(rng.integers(80,210)))
  pores=np.asarray(pit.filter(ImageFilter.GaussianBlur(.6)),dtype='float32')/255
  cracks=Image.new('L',(n,n));d=ImageDraw.Draw(cracks)
  for _ in range(28):
   x,y=rng.integers(0,n,2);pts=[(int(x),int(y))]
   for i in range(int(rng.integers(3,9))):x+=int(rng.integers(-12,13));y+=int(rng.integers(8,30));pts.append((int(x),int(y)))
   d.line(pts,fill=150,width=1)
  fracture=np.asarray(cracks.filter(ImageFilter.GaussianBlur(.5)),dtype='float32')/255
  h-=pores*.42+fracture*.25
  v=.235+.07*broad+.04*mid+.035*grain-.10*pores-.06*fracture
  c=np.stack([v*.94,v*.99,v*1.02],2)
  # Sparse olive mineral/lichen film in mottled pockets, deliberately restrained.
  mineral=np.clip((noise(n,25)-.75)*2.3,0,.25)*(noise(n,190))
  c+=mineral[:,:,None]*np.array([.16,.17,.065]);rough=.77+.18*mid+.08*grain+.12*pores
  strength=2.4
 elif f in ['lid','brass']:
  scratches=Image.new('L',(n,n));d=ImageDraw.Draw(scratches)
  for _ in range(1400 if f=='brass' else 650):
   x,y=rng.integers(0,n,2);length=int(rng.integers(4,110));d.line((int(x),int(y),int(x+length),int(y+rng.integers(-4,5))),fill=int(rng.integers(18,85)),width=1)
  scratch=np.asarray(scratches.filter(ImageFilter.GaussianBlur(.35)),dtype='float32')/255
  h=.025*grain+.018*fine-.13*scratch
  if f=='lid':
   v=.19+.055*broad+.025*mid+.012*grain;c=np.stack([v*.84,v*.95,v*1.07],2);rough=.26+.10*mid+.05*grain+.22*scratch;strength=2.4
  else:
   tarnish=np.clip((noise(n,22)-.42)*1.2,0,.65)
   v=.035*broad+.025*grain-.16*tarnish
   c=np.stack([.64+v,.53+v,.33+v],2);rough=.32+.16*mid+.15*tarnish+.24*scratch;strength=2.4
 else:
  yy,xx=np.mgrid[:n,:n];weave=(np.sin(xx*np.pi)*0 + np.sin(xx*1.55)*np.sin(yy*1.55))*.012
  h=.06*grain+.025*fine+weave;v=.19+.025*broad+.022*mid+.025*grain;c=np.stack([v*.88,v*.96,v],2);rough=.83+.12*mid+.04*grain;strength=1.6
 dy,dx=np.gradient(h);nx=-dx*strength;ny=-dy*strength;nz=np.ones_like(h);norm=np.sqrt(nx*nx+ny*ny+nz*nz);normal=np.stack([nx/norm,ny/norm,nz/norm],2)*.5+.5
 save(f,'color',c);save(f,'rough',rough);save(f,'normal',normal)
for f,n in [('basalt',2048),('lid',2048),('brass',2048),('interior',1024)]:maps(f,n);print('Generated',f,n)
