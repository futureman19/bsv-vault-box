"""World-metric unfolded flag artwork. Original top radius, no independent side glyphs."""
from pathlib import Path
from PIL import Image,ImageDraw
import math,json
R=Path(__file__).resolve().parent
RED=(181,0,24);WHITE=(239,235,218);NAVY=(2,31,65)
XMIN,XMAX=-2.56,2.56;YMIN,YMAX=-1.89,1.89
TX,TY=1.815,1.145;ZTOP=1.978;BEVEL=.045
ARC=3*2*BEVEL*math.sin(math.pi/12)
RADIUS=.125
LEFT=[-.81,-.27,.27,.81];FRONT=[-1.54,-1.27,-1.,-.73,-.46]
def side_distance(z):return ARC+(ZTOP-BEVEL-z)
def star_points(x,y):
 return [(x+math.sin(i*math.pi/5)*RADIUS*(1 if i%2==0 else .42),y+math.cos(i*math.pi/5)*RADIUS*(1 if i%2==0 else .42)) for i in range(10)]
# One coordinate-space stencil, shared by top, bevel and any continuation onto sides.
STARS=[]
for row in range(4):
 count=4 if row%2==0 else 3
 for col in range(count):STARS.append((-1.86+(col+1)*1.71/(count+1),1.19-(row+.5)*2.38/4))
STARS += [(-TX-.015,y) for y in LEFT]+[(x,-TY-.015) for x in FRONT]
def inside_star(x,y,cx,cy):
 pts=star_points(cx,cy);inside=False
 for i,(a,b) in enumerate(pts):
  c,d=pts[i-1]
  if (b>y)!=(d>y) and x<(c-a)*(y-b)/(d-b)+a:inside=not inside
 return inside
# 300 texels per physical unit in BOTH axes; supersample outlines.
w,h=1536,1134;ss=2
im=Image.new('RGB',(w*ss,h*ss));d=ImageDraw.Draw(im)
def pix(x,y):return ((x-XMIN)/(XMAX-XMIN)*w*ss,(YMAX-y)/(YMAX-YMIN)*h*ss)
for py in range(h*ss):
 y=YMAX-(py+.5)/(h*ss)*(YMAX-YMIN);row=min(4,max(0,int((1.19-y)/2.38*5)))
 d.line((0,py,w*ss,py),fill=RED if row%2==0 else WHITE)
d.rectangle((0,0,pix(-.15,0)[0],h*ss),fill=NAVY)
for x,y in STARS:d.polygon([pix(a,b) for a,b in star_points(x,y)],fill=WHITE)
im.resize((w,h),Image.Resampling.LANCZOS).save(R/'maps/flag-lid.png',optimize=True)
# Retain exact v6 field and stripes, erase independent v6 side stars by repainting
# their entire navy interval. Shared star coordinates never extend this far down.
w,h=2048,256
im=Image.new('RGB',(w,h));d=ImageDraw.Draw(im)
for i in range(5):d.rectangle((0,int(i*h/5),w,int((i+1)*h/5)),fill=RED if i%2==0 else WHITE)
d.rectangle((int(2.01/12.4*w),0,int(7.91/12.4*w),int(h*.125)),fill=NAVY)
# Evaluate SAME world stencil on shallow band, with metric unfolding from lid top.
for py in range(int(h*.125)+1):
 z=.10+(1-(py+.5)/h)*1.46;distance=side_distance(z)
 for px in range(int(2.01/12.4*w),int(7.91/12.4*w)+1):
  s=(px+.5)/w*12.4
  if 3.72<=s<=6.20:x,y=-TX-distance,4.96-s
  elif 6.20<s<=9.92:x,y=s-8.06,-TY-distance
  else:continue
  if any(inside_star(x,y,cx,cy) for cx,cy in STARS):im.putpixel((px,py),WHITE)
im.save(R/'maps/flag-wall.png',optimize=True)
(R/'wrap-layout.json').write_text(json.dumps(dict(radius=RADIUS,diameter=.25,top_stars=STARS[:-9],left_centers=STARS[-9:-5],front_centers=STARS[-5:],atlas_bounds=[XMIN,XMAX,YMIN,YMAX],texels_per_world_unit=300,bevel_chord_length=ARC,top_z=ZTOP,top_tangencies=[TX,TY],body_top_z=1.56,limitation='A 0.25 diameter star cannot span the 0.30 thick lid and reach the body. Continuous glyphs terminate on vertical lid; navy band alone continues below seam.'),indent=2))
print('Shared metric masks: 4 left + 5 front folded edge stars; radius .125')
