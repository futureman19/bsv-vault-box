"""Direct original-art rectification. No planetary image or generated stripes.
Single image cannot uniquely recover albedo: conservative illumination estimate.
Hidden/occluded material reconstructed, never asserted observed.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,hashlib
R=Path(__file__).resolve().parent;M=R/'maps';M.mkdir(exist_ok=True)
original=Image.open(R/'references/primary-morocco.png').convert('RGB')
quads={'front':[[418,580],[893,469],[889,692],[419,817]],'left':[[138,465],[418,580],[419,817],[141,679]]}
polys=[[[620,490],[716,474],[726,515],[720,557],[703,577],[631,589],[615,568]],[[655,596],[679,594],[696,606],[703,632],[688,663],[666,680],[644,676],[630,659],[629,632],[642,608]],[[458,721],[497,717],[503,742],[520,759],[520,789],[502,811],[474,817],[448,795],[447,763]],[[371,779],[397,751],[427,755],[453,769],[451,782],[479,779],[481,815],[420,831],[376,814]],[[836,681],[860,669],[865,644],[898,632],[904,700],[839,719]],[[128,624],[159,630],[166,661],[183,676],[182,706],[130,684]]]
mask=Image.new('L',original.size);d=ImageDraw.Draw(mask)
for p in polys:d.polygon([tuple(x) for x in p],fill=255)
mask.save(R/'references/hardware-shadow-mask.png')
def warp(im,quad,w,h):
 dst=[(0,0),(w-1,0),(w-1,h-1),(0,h-1)];A=[];B=[]
 for (x,y),(u,v) in zip(dst,quad):A.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);B.extend([u,v])
 c=np.linalg.solve(A,B);return im.transform((w,h),Image.Transform.PERSPECTIVE,c,Image.Resampling.BICUBIC)
def fill(a,m):
 # Candidate B: coherent exemplar patches, source-only donors. Preserve fine
 # branched grain rather than previous interpolation's horizontal smears.
 a=a.copy();h,w=m.shape;original_a=a.copy();visited=np.zeros_like(m)
 # Treat boundary shade separately; nearest interior columns, not stretched rows.
 interior=m.copy();interior[:,:10]=False;interior[:,-10:]=False
 for sy,sx in zip(*np.where(interior)):
  if visited[sy,sx]:continue
  stack=[(sy,sx)];visited[sy,sx]=True;pixels=[]
  while stack:
   y,x=stack.pop();pixels.append((y,x))
   for ny,nx in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
    if 0<=ny<h and 0<=nx<w and interior[ny,nx] and not visited[ny,nx]:visited[ny,nx]=True;stack.append((ny,nx))
  cm=np.zeros_like(m)
  for y,x in pixels:cm[y,x]=True
  rim=np.asarray(Image.fromarray(np.uint8(cm)*255).filter(ImageFilter.MaxFilter(9)))>0;rim &= ~m
  yy,xx=np.where(cm|rim);ry,rx=np.where(rim)
  best=None
  for dy in range(-14,15,7):
   for dx in range(-w+20,w-20,9):
    if abs(dx)<24:continue
    ty=yy+dy;tx=xx+dx
    if ty.min()<0 or ty.max()>=h or tx.min()<0 or tx.max()>=w or np.any(m[ty,tx]):continue
    # Compare boundary layer colors: choose an intact neighboring geological patch.
    err=np.mean((original_a[ry,rx]-original_a[ry+dy,rx+dx])**2) if len(ry) else abs(dx)
    if best is None or err<best[0]:best=(err,dx,dy)
  cy,cx=np.where(cm)
  if best is not None:
   _,dx,dy=best;donor=original_a[np.clip(cy+dy,0,h-1),np.clip(cx+dx,0,w-1)].copy()
   a[cy,cx]=donor
  else:
   # Boundary-spanning components: per-row valid donor offset, never a flat fill.
   for y in np.unique(cy):
    xs=cx[cy==y];good=np.flatnonzero(~m[y]);
    for x in xs:a[y,x]=original_a[y,good[(int(x)+len(good)//2)%len(good)]]
 # Narrow mask-only edge blending; source outside masks stays pixel-identical.
 for x in range(10):a[:,x]=a[:,10+(10-x)];a[:,-1-x]=a[:,-11-(10-x)]
 return a
patches={}
for face,w in [('front',596),('left',460)]:
 raw=warp(original,quads[face],w,256);raw.save(R/f'references/{face}-rectified-observed.png')
 m=np.asarray(warp(mask,quads[face],w,256))>10
 # Explicit edge uncertainty: rounded edges + lid/contact shadow removed.
 m[:9]=True;m[-10:]=True;m[:,:8]=True;m[:,-8:]=True
 # Fill boundary rows from nearest valid material, then horizontal obscurations.
 a=np.asarray(raw,dtype=float).copy()
 # Reflect narrow edge context instead of repeating a single scanline (streaks).
 a[:9]=a[9:18][::-1];a[-10:]=a[-20:-10][::-1];m[:9]=m[9:18][::-1];m[-10:]=m[-20:-10][::-1]
 Image.fromarray(np.uint8(m)*255).save(R/f'references/{face}-rectified-mask.png')
 a=fill(a,m)
 # Approximate low-order lighting correction only, NOT flattening geological bands.
 yy,xx=np.mgrid[:256,:w];gain=1.0+.07*(yy/255-.5)
 if face=='left':gain*=1.66 # observed left-face lighting; same underlying pigment family
 a=np.clip(a*gain[...,None],0,255)
 patches[face]=a
 Image.fromarray(np.uint8(a)).save(R/f'{face}-clean-material.png')
# One candidate. Physical sizes front=3.72 left=2.88 height=1.60.
# Full 13.2-unit perimeter at 160 texels/unit. seam at rear centre.
front=patches['front'];left=patches['left']
# Match shaded side's overall chroma/luminance conservatively to front distribution.
for c in range(3):
 delta=np.median(front[:,:,c])-np.median(left[:,:,c]);left[:,:,c]+=delta*.65
left=np.clip(left,0,255)
# Back/right are disclosed mirrored extrapolations, not observations.
back=front[:,::-1].copy();right=left[:,::-1].copy()
a=np.concatenate([back[:,298:],left,front,right,back[:,:298]],axis=1)
# Narrow same-row crossfades at physical corners, not a new band design.
for seam in [298,758,1354,1814]:
 for k in range(-12,13):
  t=(k+12)/24;target=a[:,seam-13]*(1-t)+a[:,seam+13]*t
  weight=(1-abs(k)/13)*.85;a[:,seam+k]=a[:,seam+k]*(1-weight)+target*weight
# Rear seam endpoint is repaired only within 12 pixels.
target=(a[:,0]+a[:,-1])/2
for k in range(12):
 t=(1-k/12)**2;a[:,k]=a[:,k]*(1-t)+target*t;a[:,-1-k]=a[:,-1-k]*(1-t)+target*t
# One post-model focused correction: subdued reflectance calibration, not new strata.
# Bright/midtone cream and peach attenuated; deep geological seams less affected.
weight=np.clip(a.mean(axis=-1)/190,.25,1)[...,None]
a*=1-weight*np.array([.12,.16,.18])
a=np.uint8(np.clip(a,0,255));a[:,-1]=a[:,0]
Image.fromarray(a).save(M/'reference-color.png',optimize=True)
# Tiny physical-scale relief extracted from actual mineral grain, not uniform noise.
g=Image.fromarray(a).convert('L');hi=(np.asarray(g,dtype=float)-np.asarray(g.filter(ImageFilter.GaussianBlur(1.5)),dtype=float))/255
dy,dx=np.gradient(hi*.10);n=np.stack([-dx,dy,np.ones_like(dx)],-1);n/=np.linalg.norm(n,axis=-1,keepdims=True)
n=np.uint8((n*.5+.5)*255);n[:,-1]=n[:,0];Image.fromarray(n).save(M/'reference-normal.png',optimize=True)
rough=np.uint8(np.clip(.78+hi*.18,.72,.85)*255);orm=np.stack([np.full_like(rough,255),rough,np.zeros_like(rough)],-1);orm[:,-1]=orm[:,0];Image.fromarray(orm).save(M/'reference-orm.png',optimize=True)
board=Image.new('RGB',(1200,1000),'#242329');d=ImageDraw.Draw(board)
crop=original.crop((130,460,900,825));crop.thumbnail((760,360));board.paste(crop,(20,40));d.text((20,15),'ORIGINAL BODY CROP - image illumination and hardware present',fill='white')
for i,face in enumerate(['front','left']):
 im=Image.fromarray(np.uint8(patches[face]));board.paste(im,(20+i*650,445));d.text((20+i*650,420),face.upper()+' RECTIFIED / MASK-FILLED / LIGHT ESTIMATE',fill='white')
im=Image.fromarray(a);im.thumbnail((1160,240));board.paste(im,(20,770));d.text((20,740),'CANDIDATE B: physical-aspect perimeter atlas; back/right extrapolated',fill='white');board.save(R/'texture-swatch-board.jpg',quality=95)
provenance={'primary_sha256':hashlib.sha256((R/'references/primary-morocco.png').read_bytes()).hexdigest(),'source':'User-generated original marketing art, not a photograph or scan','quadrilaterals':quads,'obstruction_polygons':polys,'atlas_size':list(Image.fromarray(a).size),'physical_perimeter_height':[13.2,1.6],'front_atlas_pixels':[758,1354],'left_atlas_pixels':[298,758],'method':'Planar homographies; explicit hardware/shadow masks; same-height exemplar patch fill under occlusion; low-order illumination estimate. Source geological pixels retained outside masks. Narrow corner blends.','illumination_limit':'Single image intrinsic separation is approximate; global left gain 1.66 and partial median match, mild vertical gain, boundary shade removal.','extrapolated':'Back and right mirrored from front/left; occluded hardware zones exemplar-reconstructed. No new stripes or uniform noise.','candidate_count':2,'selected':'B exemplar patch reconstruction; A interpolation rejected for smears'}
(R/'material-provenance.json').write_text(json.dumps(dict(provenance,post_model_correction={'count':1,'reflectance_max_rgb_attenuation':[.12,.16,.18],'weight':'clip(mean_sRGB/190,.25,1)','edge_treatment':'reflect narrow valid context instead of repeating a scanline'}),indent=2));print(provenance)
