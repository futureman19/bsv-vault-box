"""V10: one vertical star stencil across the closed lid, rim and body.
Top stars retain their size; seam stars intentionally move off the top bevel.
"""
from pathlib import Path
from PIL import Image,ImageDraw
import math,json
R=Path(__file__).resolve().parent
RED=(181,0,24);WHITE=(239,235,218);NAVY=(2,31,65)
XMIN,XMAX=-2.56,2.56;YMIN,YMAX=-1.89,1.89
TX,TY=1.815,1.145;ZTOP=1.978;BEVEL=.045
ARC=3*2*BEVEL*math.sin(math.pi/12)
RADIUS=.125;SEAM_CENTER=1.72
LEFT=[-.81,-.27,.27,.81];FRONT=[-1.54,-1.27,-1.,-.73,-.46]
def side_distance(z):return ARC+(ZTOP-BEVEL-z)
def star_points(x,y):
 return [(x+math.sin(i*math.pi/5)*RADIUS*(1 if i%2==0 else .42),y+math.cos(i*math.pi/5)*RADIUS*(1 if i%2==0 else .42)) for i in range(10)]
STARS=[]
for row in range(4):
 count=4 if row%2==0 else 3
 for col in range(count):STARS.append((-1.86+(col+1)*1.71/(count+1),1.19-(row+.5)*2.38/4))
# Edge glyphs use shared vertical coordinates, not a second independent row.
STARS += [(-TX-side_distance(SEAM_CENTER),y) for y in LEFT]+[(x,-TY-side_distance(SEAM_CENTER)) for x in FRONT]
w,h=1536,1134;ss=2
im=Image.new('RGB',(w*ss,h*ss));d=ImageDraw.Draw(im)
def pix(x,y):return ((x-XMIN)/(XMAX-XMIN)*w*ss,(YMAX-y)/(YMAX-YMIN)*h*ss)
for py in range(h*ss):
 y=YMAX-(py+.5)/(h*ss)*(YMAX-YMIN);row=min(4,max(0,int((1.19-y)/2.38*5)))
 d.line((0,py,w*ss,py),fill=RED if row%2==0 else WHITE)
d.rectangle((0,0,pix(-.15,0)[0],h*ss),fill=NAVY)
for x,y in STARS:d.polygon([pix(a,b) for a,b in star_points(x,y)],fill=WHITE)
im.resize((w,h),Image.Resampling.LANCZOS).save(R/'maps/flag-lid.png',optimize=True)
# Full-height body map; retain historical stripe elevations below the navy band.
w,h=2480,752;ss=2;ZMIN=.10;ZMAX=1.978
im=Image.new('RGB',(w*ss,h*ss));d=ImageDraw.Draw(im)
def wallpix(s,z):return (s/12.4*w*ss,(ZMAX-z)/(ZMAX-ZMIN)*h*ss)
for py in range(h*ss):
 z=ZMAX-(py+.5)/(h*ss)*(ZMAX-ZMIN);row=min(4,max(0,int((1.56-z)/1.46*5)))
 d.line((0,py,w*ss,py),fill=RED if row%2==0 else WHITE)
d.rectangle((*wallpix(2.01,ZMAX),*wallpix(7.91,1.3775)),fill=NAVY)
# Front glyph orientation follows the same atlas x,z; left atlas swaps axes.
for y in LEFT:
 pts=star_points(-TX-side_distance(SEAM_CENTER),y)
 d.polygon([wallpix(4.96-b,ZTOP-BEVEL+ARC+a+TX) for a,b in pts],fill=WHITE)
for x in FRONT:
 pts=star_points(x,-TY-side_distance(SEAM_CENTER))
 d.polygon([wallpix(a+8.06,ZTOP-BEVEL+ARC+b+TY) for a,b in pts],fill=WHITE)
im.resize((w,h),Image.Resampling.LANCZOS).save(R/'maps/flag-wall.png',optimize=True)
(R/'wrap-layout.json').write_text(json.dumps(dict(radius=RADIUS,diameter=.25,top_stars=STARS[:-9],left_centers=STARS[-9:-5],front_centers=STARS[-5:],seam_center_z=SEAM_CENTER,body_z_range=[ZMIN,ZMAX],limitation='Same-size seam stars span vertical lid, fixed rim and upper body, not the distant lid top. Existing physical closure seam interrupts pigment; no geometry bridges the opening.'),indent=2))
print('14 top stars; shared seam glyphs: four left, five front; radius .125')
