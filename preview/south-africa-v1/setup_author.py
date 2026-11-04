"""Derive only reusable mechanism authoring helpers; writes local author.py."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
s=s[:s.index('trunk=')]+s[s.index('# Medallion'):]
a=s.index('# Exterior skins');b=s.index('# Small collar')
s=s[:a]+'''# Continuous sandstone exterior behind the independent liner.
for sy in [-1,1]:cube('Sandstone / front rear',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.025)
for sx in [-1,1]:cube('Sandstone / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.025)
'''+s[b:]
a=s.index('# A thin satin');b=s.index('# Restrained brass')
s=s[:a]+s[b:]
a=s.index("stone('Terrain / granite'");b=s.index('def tube(',a)
s=s[:a]+'''# Closed irregular mesa: stratified perimeter rings with level summit.
N=40;verts=[];faces=[]
for k,(z,scale) in enumerate([(1.97,1.08),(2.12,1.02),(2.29,.94),(2.48,.91),(2.69,.88)]):
 for j in range(N):
  a=math.tau*j/N
  x=math.copysign(abs(math.cos(a))**.45,math.cos(a))*1.15
  y=math.copysign(abs(math.sin(a))**.55,math.sin(a))*.46
  q=1+.035*math.sin(j*2.7)+.018*math.cos(j*1.3)
  verts.append((x*scale*q,y*scale*q+.22,z+(.012*math.sin(j*1.4) if k==4 else .018*math.sin(j*1.7+k))))
for k in range(4):
 for j in range(N):faces.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
faces.extend([tuple(reversed(range(N))),tuple(4*N+j for j in range(N))])
me=bpy.data.meshes.new('Mesa stratified closed surface');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / Table Mountain mesa',me);bpy.context.collection.objects.link(o);me.materials.append(wood);uv(o);parent(o)
# Low clustered vegetation, not a botanical reconstruction.
for i in range(38):
 a=i*2.399;r=.81+.07*math.sin(i*3.1);x=math.cos(a)*1.46;y=math.sin(a)*.76+.12
 if abs(x)<1.3 and abs(y-.22)<.52:continue
 stone('Fynbos / cushion',(x,y,2.005),(.11,.075,.046),lid,moss,2)
'''+s[b:]
s=s.replace('japan.blend','south-africa.blend').replace('japan.glb','south-africa.glb').replace('JAPAN AUTHORED','SOUTH AFRICA AUTHORED')
s=s.replace('Cedar / fine longitudinal grain','Sandstone / irregular strata').replace('cedar-color.png','sandstone-color.png').replace('cedar-roughness.png','sandstone-roughness.png').replace('cedar-end.png','sandstone-detail.png').replace('Cedar /','Sandstone /')
s=s.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z","u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z")
s=s.replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=4').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820').replace('(-5.6,-7.8,4.5)','(-5.6,-7.8,6.3)')
(R/'author.py').write_text(s)
print('local author generator prepared')
