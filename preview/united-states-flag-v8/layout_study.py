"""Analytic developed-surface swatch before structural authoring."""
from pathlib import Path
from PIL import Image,ImageDraw
import math,json
R=Path(__file__).resolve().parent
r=.045;scale=.20
arc=sum(math.hypot(r*(math.sin((i+1)*math.pi/6)-math.sin(i*math.pi/6)),r*scale*(math.cos((i+1)*math.pi/6)-math.cos(i*math.pi/6))) for i in range(3))
top=1.56+(1.978-1.56)*scale
qbody=arc+(1.56+(1.933-1.56)*scale-1.56)
report=dict(strategy='Reprofile all geometry above body rim z=1.56 by 0.20; retain lower body and foot silhouette, transform affected pivots and hardware consistently.',old_lid_thickness=.30,new_lid_thickness=.06,top=top,top_bevel_developed=arc,body_q=qbody,star_radius=.125,edge_center_q=.045,front_lowest_q=.045+.125*math.cos(math.pi/5),left_lowest_q=.045+.125*math.sin(2*math.pi/5),body_continuation_expected=True)
assert qbody<report['front_lowest_q'] and qbody<report['left_lowest_q']
im=Image.new('RGB',(900,400),'#101e45');d=ImageDraw.Draw(im)
for i,c in enumerate([.045,.045]):
 cx=250+i*400;cy=120
 pts=[(cx+math.sin(k*math.pi/5)*.125*(1 if k%2==0 else .42)*1500,cy-math.cos(k*math.pi/5)*.125*(1 if k%2==0 else .42)*1500) for k in range(10)]
 d.polygon(pts,fill='#efebda')
for q,label in [(0,'top tangency'),(arc,'vertical lid'),(qbody,'BODY START')]:
 y=120+(q-.045)*1500;d.line((0,y,900,y),fill='#ff7040',width=2);d.text((5,y+3),label,fill='white')
im.save(R/'stage1-analytic-swatch.png');(R/'stage1-layout.json').write_text(json.dumps(report,indent=2));print(report)
