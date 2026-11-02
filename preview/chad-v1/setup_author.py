"""One-time lineage adaptation; requires the repository Japan v1 generator."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
a=s[:s.index('# Exterior skins')]
a=a.replace('Reference-led Japan pilot','Chad Ennedi landscape pilot').replace("wood=mat('Cedar / fine longitudinal grain'","wood=mat('Sandstone / ochre strata'").replace('cedar-color.png','sandstone-color.png').replace('cedar-roughness.png','sandstone-roughness.png').replace('cedar-end.png','dark-grain.png').replace('granite.png','dark-grain.png')
a+='''# Four stone skins preserve continuous inherited inner walls.
for sy in [-1,1]:cube('Sandstone / wall',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.035)
for sx in [-1,1]:cube('Sandstone / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.035,axis='Y')
'''
a+=s[s.index('# Small collar'):s.index('def stone')]
a=a.replace("(.035,.07,.032)","(.055,.028,.012)").replace('Mineral seam / moss green','Mineral seam / dark desert varnish')
a=a.replace('Cedar / clasp seat','Sandstone / clasp seat').replace('Cedar / rim corner','Sandstone / rim corner')
# Omit wooden end-grain finger decoration while retaining brass corner caps.
a=a[:a.index('# A thin satin')]+a[a.index('# Restrained brass'):]
a+=s[s.index('def stone'):s.index("stone('Terrain / granite'")]
a+='''# True hollow arch ring: front/back strips plus inner/outer reveals.
verts=[];faces=[];n=25
for side in [-1,1]:
 for i in range(n):
  t=math.pi*i/(n-1)
  for outer in [False,True]:
   rx=1.08 if outer else .68
   rz=.84 if outer else .49
   jitter=.025*math.sin(i*2.7) if outer else .008*math.sin(i*2.1)
   verts.append((rx*math.cos(t)+jitter,.28+side*(.19+.025*math.sin(i*1.3)),2.00+rz*math.sin(t)))
for i in range(n-1):
 a=i*2;b=(i+1)*2;c=2*n+a;d=2*n+b
 faces.extend([(a,b,b+1,a+1),(c+1,d+1,d,c),(a,c,d,b),(a+1,b+1,d+1,c+1)])
faces.extend([(0,1,2*n+1,2*n),(2*n-2,4*n-2,4*n-1,2*n-1)])
me=bpy.data.meshes.new('Open arch geometry');me.from_pydata(verts,[],faces);me.update()
o=bpy.data.objects.new('Ennedi / open wind arch',me);bpy.context.collection.objects.link(o);me.materials.append(wood);uv(o);parent(o)
for sx in [-1,1]:
 stone('Ennedi / arch footing',(sx*.92,.28,2.025),(.25,.32,.085),lid,wood,2)
for x,y,h in [(-1.3,.64,.29),(1.35,.61,.40),(1.12,-.56,.20)]:
 stone('Ennedi / eroded piton',(x,y,1.99+h*.42),(.15,.18,h*.55),lid,wood,2)
'''
a+=s[s.index('# Medallion'):]
a=a.replace('japan.blend','chad.blend').replace('japan.glb','chad.glb').replace('JAPAN AUTHORED','CHAD AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24')
(R/'author.py').write_text(a)
