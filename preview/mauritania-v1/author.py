"""Original Richat-inspired procedural landscape, inherited articulation only."""
import bpy,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(2301)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
exec((R/'author_helpers.py').read_text())
sand=mat('Ochre / mineral bedding',(.48,.26,.10),.78);maptex(sand,'ochre-color.png','Base Color');maptex(sand,'mineral-roughness.png','Roughness',True)
slate=mat('Slate / eroded cuesta',(.11,.14,.14),.84);maptex(slate,'slate-color.png','Base Color')
cream=mat('Cream / exposed sandstone',(.65,.48,.28),.83)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / dark reveal',(.045,.05,.048),.88)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(sand if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Stone body / front' if sy<0 else 'Stone body / rear',(0,sy*1.145,.83),(3.72,.19,1.46),sand,bevel=.035)
for sx in [-1,1]:cube('Stone body / side',(sx*1.745,0,.83),(.23,2.10,1.46),sand,bevel=.025,axis='Y')
cube('Stone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),sand,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Stone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),sand,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),sand,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Stone / foot',(sx*1.47,sy*.91,-.09),(.54,.46,.34),slate,bevel=.06)
# One contiguous sculpted relief with three irregular ring crests and erosion cuts.
# All terrain vertices lie above the lid and all terrain belongs to its hinge.
N=112;M=76;verts=[];faces=[];radii=[]
for j in range(M+1):
 y=-.94+1.88*j/M
 for i in range(N+1):
  x=-1.43+2.86*i/N;theta=math.atan2(y/.83,x/1.31)
  r=math.hypot(x/1.31,y/.83);rr=r+.021*math.sin(theta*7)+.012*math.sin(theta*13+.5)
  ridge=sum(amp*math.exp(-((rr-center)/width)**2) for center,width,amp in [(.29,.045,.17),(.53,.052,.25),(.79,.055,.30)])
  channel=1-.86*math.exp(-(math.sin(theta-.46)/.075)**2)
  edge=max(0,min(1,(1.13-r)*12))
  dune=.024*(1+math.sin(x*16+y*9))*max(0,min(1,(r-.8)*5))
  z=1.98+edge*(.016+ridge*channel+dune+.007*math.sin(x*55+y*29)*min(1,ridge*10))
  verts.append((x,y,z));radii.append(rr)
for j in range(M):
 for i in range(N):
  a=j*(N+1)+i;faces.append((a,a+1,a+N+2,a+N+1))
me=bpy.data.meshes.new('Richat relief / eroded concentric strata');me.from_pydata(verts,[],faces);me.update()
o=bpy.data.objects.new('Terrain / Richat three cuestas and dunes',me);bpy.context.collection.objects.link(o)
for m in [sand,slate,cream]:me.materials.append(m)
for f in me.polygons:
 r=sum(radii[k] for k in f.vertices)/len(f.vertices)
 f.material_index=1 if any(abs(r-c)<.025 for c in [.29,.53,.79]) else (2 if any(.025<abs(r-c)<.052 for c in [.29,.53,.79]) else 0)
 f.use_smooth=True
uv(o);parent(o)
o['ridge_centers']=[.29,.53,.79];o['theme']='Eroded domed anticline abstraction, not impact crater'
# Raised brass emblem, with no culturally attributed symbol.
bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.13,depth=.035,location=(0,-1.258,.87),rotation=(math.pi/2,0,0));bpy.context.object.name='Medallion / solid brass';bpy.context.object.data.materials.append(gold)
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(0,-1.282,.87),major_radius=.107,minor_radius=.008,rotation=(math.pi/2,0,0));bpy.context.object.name='Medallion / raised rim';bpy.context.object.data.materials.append(gold)
exec((R/'author_finish.py').read_text())
