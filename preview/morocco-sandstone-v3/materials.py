"""Seeded original mineral painting, not scans; no external assets or runtime network."""
from pathlib import Path
from PIL import Image,ImageFilter
import numpy as np,json
R=Path(__file__).resolve().parent;M=R/'maps';M.mkdir(exist_ok=True)
rng=np.random.default_rng(71834);W,H=1024,128

def noise(w,h,outw=W,outh=H):
 a=rng.uniform(0,1,(h,w));a[:,-1]=a[:,0]
 im=Image.fromarray(np.float32(a),'F').resize((outw,outh),Image.Resampling.BICUBIC)
 return np.asarray(im)
def smooth(w,h):return noise(w,h)-.5
Y,X=np.mgrid[:H,:W];v=Y/H
# A stack of eroded depositional sheets. Each boundary has an independent
# periodic random-walk profile, never a repeated sinusoid or marble warp.
warp=smooth(18,8)*.012+smooth(64,16)*.004
edges=np.concatenate(([0],np.cumsum(rng.uniform(.022,.14,24))));edges=edges[edges<1.05]
palette=np.array([[174,117,88],[184,132,100],[174,126,91],[191,148,109],[161,107,82],[187,142,108],[197,159,119],[178,124,96]])
c=np.empty((H,W,3));c[:]=palette[0];relief=np.zeros((H,W));bandfield=np.zeros((H,W))
for i,e in enumerate(edges[1:]):
 profile=(noise(int(rng.integers(12,45)),1, W,1)[0]-.5)*rng.uniform(.009,.025)
 d=v-e-profile[None,:]-warp
 blend=np.clip(d/.003+.5,0,1)
 color=palette[i%len(palette)]*.42+np.array([165,119,83])*.58
 c=c*(1-blend[...,None])+color*blend[...,None]
 # Thin broken gritty seams. The middle and lower stack have more bedding.
 broken=np.clip((noise(80,10)-.35)*2,0,1)
 seam=np.exp(-(d/.0018)**2)*broken
 if i%3==0:
  c-=seam[...,None]*np.array([21,19,15]);relief-=seam*.42
 elif i%4==0:c+=seam[...,None]*11
 relief+=blend*rng.uniform(-.12,.12);bandfield+=blend
# Sand matrix, weathering mottles, embedded mineral grains and shallow pore clusters.
grain=rng.normal(0,1,(H,W));micro=smooth(512,64);mottle=smooth(256,32);weather=smooth(64,8)
flecks=(rng.random((H,W))>.978).astype(float);pits=(rng.random((H,W))>.974).astype(float)
c+=grain[...,None]*8+micro[...,None]*13+mottle[...,None]*22+weather[...,None]*15
c+=flecks[...,None]*rng.uniform(15,38,(H,W,1));c-=pits[...,None]*rng.uniform(12,26,(H,W,1))
relief+=grain*.25+micro*.8+mottle*.65-flecks*.12-pits*.8
# Periodic wrap endpoints exactly agree before encoding.
c[:,-1]=c[:,0];relief[:,-1]=relief[:,0]
Image.fromarray(np.uint8(np.clip(c,0,255))).save(M/'sandstone-color.jpg',quality=88,subsampling=0,optimize=True)
# Compact normals/ORM share continuous body coordinates; OpenGL tangent convention.
h=np.asarray(Image.fromarray(np.float32(relief),'F').resize((1024,128),Image.Resampling.BICUBIC))
dy,dx=np.gradient(h);nx=-dx*2.2;ny=dy*2.2;nz=np.ones(h.shape);length=np.sqrt(nx*nx+ny*ny+nz*nz)
n=np.stack([nx/length,ny/length,nz/length],-1);normal=np.uint8(np.clip((n*.5+.5)*255,0,255));normal[:,-1]=normal[:,0]
Image.fromarray(normal).save(M/'sandstone-normal.png',optimize=True)
r=np.asarray(Image.fromarray(np.float32(.86+grain*.035+micro*.13+mottle*.12+pits*.10),'F').resize((1024,128),Image.Resampling.BICUBIC));rough=np.uint8(np.clip(r,.66,.99)*255)
orm=np.stack([np.full_like(rough,255),rough,np.zeros_like(rough)],-1);orm[:,-1]=orm[:,0]
Image.fromarray(orm).save(M/'sandstone-orm.jpg',quality=91,subsampling=0,optimize=True)
result={'provenance':'Original seeded synthetic mineral painting, not scanned sandstone or sourced CC0','seed':71834,'mapping':'continuous object-space XY angle and physical Z, periodic at rear','maps':{p.name:p.stat().st_size for p in M.iterdir()},'palette_mean':np.mean(c,axis=(0,1)).tolist(),'normal_channel_std':normal.std(axis=(0,1)).tolist(),'roughness_minmax':[int(rough.min()),int(rough.max())]}
(R/'material-provenance.json').write_text(json.dumps(result,indent=2));print(result)
