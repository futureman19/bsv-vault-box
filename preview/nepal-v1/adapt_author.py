"""One-time lineage adapter; author.py is the standalone reproducible output."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
s=s[:s.index('wood=mat')]+'''wood=mat('Slate / blue gray mineral',(.25,.30,.35),.75);maptex(wood,'slate-color.png','Base Color');maptex(wood,'slate-roughness.png','Roughness',True)
granite=mat('Granite / dark feet',(.20,.22,.25),.85);maptex(granite,'granite.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / dark blue',(.025,.04,.055),.9)
snow=mat('Snow / opaque ivory',(.86,.9,.93),.88)
rock=mat('Ridge / dark metamorphic stone',(.18,.23,.29),.84)
'''+s[s.index('def uv('):s.index('# Exterior skins')]+'''# Continuous stone skins with non-overlapping butt joints.
for sy in [-1,1]:cube('Slate / front rear',(0,sy*1.145,.83),(3.26,.19,1.46),wood,bevel=.014)
for sx in [-1,1]:cube('Slate / sides',(sx*1.745,0,.83),(.23,2.48,1.46),wood,bevel=.014,axis='Y')
'''+s[s.index('# Small collar'):s.index('# A thin satin')]+s[s.index('# Restrained brass'):s.index("stone('Terrain / granite'")]+'''# Three asymmetric ridges with triangulated slope planes and snow caps.
for k,(cx,cy,rx,ry,h) in enumerate([(-.90,.22,.38,.60,.62),(0,.38,.46,.63,.95),(.96,.30,.40,.58,.72)]):
 verts=[]
 N=12
 for ring in range(3):
  for j in range(N):
   a=math.tau*j/N; wob=1+.08*math.sin(j*2.3+k)
   if ring==0:r=1;z=1.974
   elif ring==1:r=.43+.07*math.sin(j*1.7);z=1.978+h*(.53+.09*math.sin(j*2.2+k))
   else:r=.09;z=1.978+h*(.91+.045*math.sin(j*2.1))
   verts.append((cx+rx*r*math.cos(a)*wob+ring*.025,cy+ry*r*math.sin(a),z))
 verts.append((cx+.08,cy+.02,1.978+h));faces=[];mats=[]
 for ring in range(2):
  for j in range(N):
   a=ring*N+j;b=ring*N+(j+1)%N;c=b+N;d=a+N
   faces.extend([(a,b,c),(a,c,d)]);mats.extend([ring,ring])
 for j in range(N):faces.append((24+j,24+(j+1)%N,36));mats.append(1)
 faces.append(tuple(reversed(range(N))));mats.append(0)
 me=bpy.data.meshes.new('Himalayan ridge');me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new('Mountain / '+str(k+1),me);bpy.context.collection.objects.link(o);me.materials.append(rock);me.materials.append(snow)
 for f,mi in zip(me.polygons,mats):f.material_index=mi
 parent(o,lid)
'''+s[s.index('# Medallion'):]
s=s.replace('japan','nepal').replace('JAPAN AUTHORED','NEPAL AUTHORED').replace('Reference-led Japan pilot','Brief-led Nepal pilot').replace('Cedar / clasp seat','Slate / clasp seat').replace('Cedar / rim corner','Slate / rim corner')
s=s.replace("scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000", "scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=1000;scene.render.resolution_y=800")
s=s.replace("location=(-5.6,-7.8,4.5)","location=(-5.6,-7.8,6.2)")
(R/'author.py').write_text(s)
