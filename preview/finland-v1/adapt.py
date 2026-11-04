"""Reproduce the scoped author adaptation from the repository Japan mechanism pilot."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
s=s.replace('Reference-led Japan pilot','Brief-led Finland pilot').replace("wood=mat('Cedar / fine longitudinal grain',(.4,.18,.08),.4);maptex(wood,'cedar-color.png','Base Color');maptex(wood,'cedar-roughness.png','Roughness',True)","wood=mat('Birch / pale honey wood',(.67,.53,.30),.5);maptex(wood,'wood-color.png','Base Color');maptex(wood,'birch-roughness.png','Roughness',True)\nbirch=mat('Birch / ivory bark',(.70,.68,.59),.72);maptex(birch,'birch-color.png','Base Color');maptex(birch,'birch-roughness.png','Roughness',True)")
s=s.replace("'cedar-end.png'","'birch-end.png'")
s=s.replace(',wood,bevel=.003)',',birch,bevel=.003)').replace(",wood,bevel=.003,axis='Y')",",birch,bevel=.003,axis='Y')")
a=s.index("stone('Terrain / granite'");b=s.index('# Medallion is solid',a)
s=s[:a]+'''# Three invented low island outlines surrounded by a contiguous enamel lake.
water=mat('Lake / deep Finnish blue',(.018,.18,.29),.22,.15)
green=mat('Island / forest green',(.075,.16,.07),.88)
def relief(n,cx,cy,rx,ry,bottom,top,material,phase):
 verts=[];N=64
 for z in [bottom,top]:
  for i in range(N):
   a=i*math.tau/N;k=1+.075*math.sin(3*a+phase)+.035*math.cos(5*a-phase)
   verts.append((cx+rx*k*math.cos(a),cy+ry*k*math.sin(a),z))
 faces=[tuple(reversed(range(N))),tuple(range(N,2*N))]
 for i in range(N):j=(i+1)%N;faces.append((i,j,j+N,i+N))
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);parent(o);return o
relief('Lake / enamel basin',0,0,1.34,.73,1.976,2.035,water,.3)
for i,(x,y,rx,ry) in enumerate([(-.68,.04,.29,.29),(.02,.19,.22,.32),(.66,-.03,.28,.27)]):
 relief('Island / forest relief '+str(i),x,y,rx,ry,2.025,2.12+i*.018,green,i*.8)
''' +s[b:]
s=s.replace('Cedar','Birch').replace('japan.blend','finland.blend').replace('japan.glb','finland.glb').replace('JAPAN AUTHORED','FINLAND AUTHORED')
s=s.replace("scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000", "scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=900;scene.render.resolution_y=820")
s=s.replace("location=(-5.6,-7.8,4.5)","location=(-5.6,-7.8,6.7)")
(R/'author.py').write_text(s)
