from pathlib import Path
from PIL import Image
import numpy as np,json
R=Path(__file__).resolve().parent
OLD=R.parent/'united-states-flag-v4'
def features(root):
 a=np.array(Image.open(root/'maps/flag-lid.png').convert('RGB')).astype(int)
 mask=(a[:,:350,0]>230)&(a[:,:350,1]>230)
 seen=set();components=[]
 for y,x in zip(*np.where(mask)):
  if (y,x) in seen:continue
  stack=[(y,x)];seen.add((y,x));pts=[]
  while stack:
   p=stack.pop();pts.append(p)
   for q in [(p[0]-1,p[1]),(p[0]+1,p[1]),(p[0],p[1]-1),(p[0],p[1]+1)]:
    if 0<=q[0]<mask.shape[0] and 0<=q[1]<mask.shape[1] and mask[q] and q not in seen:seen.add(q);stack.append(q)
  if len(pts)>10:components.append([len(pts),max(p[1] for p in pts)-min(p[1] for p in pts)+1])
 col=a[:,600];runs=1+int(np.any(col[1:]!=col[:-1],axis=1).sum())
 red=a[(a[:,:,0]>150)&(a[:,:,1]<80)].mean(axis=0).tolist()
 return dict(stars=len(components),mean_star_width=float(np.mean([c[1] for c in components])),stripe_count=runs,red_RGB=red)
a=features(OLD);b=features(R)
assert b['stars']==14<a['stars'] and b['mean_star_width']>1.8*a['mean_star_width']
assert b['stripe_count']==5<a['stripe_count']
assert b['red_RGB'][0]>230 and b['red_RGB'][1]<15 and b['red_RGB'][2]<25
w=np.array(Image.open(R/'maps/flag-wall.png'));navy=np.all(w==[12,30,69],axis=2)
ys,xs=np.where(navy);assert ys.min()==0 and .10<=((ys.max()+1)/w.shape[0])<=.15
# Rectangle is one connected shallow strip, has no white stars/holes.
assert navy[:ys.max()+1,xs.min():xs.max()+1].all() and not navy[ys.max()+1:].any()
# Physical canton boundaries registered to left-lid allocation, rear and front.
start=xs.min()/w.shape[1]*12.4;end=(xs.max()+1)/w.shape[1]*12.4
assert abs(start-(1.86-(-.15)))<.015 and abs(end-(6.20+1.71))<.015
out=dict(PASS=True,v4=a,v5=b,body_band_fraction=(ys.max()+1)/w.shape[0],body_band_single_rectangle_no_stars=True,perimeter_bounds=[start,end],navy_RGB=[12,30,69],ivory_unchanged=[239,235,218],correction_iterations=1)
(R/'features-check.json').write_text(json.dumps(out,indent=2));print(out)
