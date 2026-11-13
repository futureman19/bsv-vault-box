"""One-time assembly from the repository's mechanically proven Japan author."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
a=s[s.index('import bpy'):s.index("wood=mat")]
a+='''stone_mat=mat('Limestone / pale fractured strata',(.55,.56,.52),.72);maptex(stone_mat,'limestone-color.png','Base Color');maptex(stone_mat,'limestone-roughness.png','Roughness',True)
granite=stone_mat
wood=stone_mat
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Jade / narrow reveal',(.025,.075,.055),.8)
green=mat('Bank / alpine green',(.08,.18,.10),.9);maptex(green,'bank-green.png','Base Color')
water=mat('Soca / polished emerald inlay',(.015,.36,.26),.16,.18)
'''
a+='''def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone projection')
 for p in o.data.polygons:
  n=p.normal; k=max(range(3),key=lambda k:abs(n[k])); axes=[i for i in range(3) if i!=k]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]/2+.5,co[axes[1]]/2+.5)
'''
a+=s[s.index('def cube'):s.index('# Exterior skins')]
a+='''for sy in [-1,1]:cube('Limestone / front' if sy<0 else 'Limestone / rear',(0,sy*1.145,.83),(3.72,.19,1.46),stone_mat,bevel=.025)
for sx in [-1,1]:cube('Limestone / side',(sx*1.745,0,.83),(.23,2.10,1.46),stone_mat,bevel=.025)
'''
a+=s[s.index('# Small collar'):s.index('# A thin satin')]
a+=s[s.index('# Restrained brass'):s.index("stone('Terrain / granite'")]
a+='''# Watertight sinuous miniature ribbon and independent irregular banks.
def center(x):return -.15+.18*math.sin(x*2.8)
def width(x):return .105+.018*math.cos(x*4)
def mesh(n,verts,faces,material):
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o);return o
N=49
xs=[-1.4+i*2.8/(N-1) for i in range(N)]
v=[]
for x in xs:
 for z in [2.005,2.035]:
  for side in [-1,1]:v.append((x,center(x)+side*width(x),z))
f=[]
for i in range(N-1):
 q=i*4;r=q+4;f.extend([(q+2,r+2,r+3,q+3),(q+1,r+1,r,q),(q,r,r+2,q+2),(q+3,r+3,r+1,q+1)])
f.extend([(0,2,3,1),(4*(N-1),4*(N-1)+1,4*(N-1)+3,4*(N-1)+2)])
mesh('Landscape / Soca continuous inlay',v,f,water)
for side in [-1,1]:
 verts=[];faces=[]
 for i,x in enumerate(xs):
  c=center(x);inner=c+side*(width(x)+.008);outer=side*(.70+.10*math.sin(x*3+side))
  ridge=(inner+outer)*.5
  peak=(.13 if side<0 else .48)*(0.5+0.5*math.sin(i*.67+side)**2)*math.sin(math.pi*i/(N-1))
  verts.extend([(x,inner,2.025),(x,ridge,2.08+peak),(x,outer,2.015),(x,inner,1.99),(x,outer,1.99)])
 for i in range(N-1):
  q=i*5;r=q+5
  faces.extend([(q,r,r+1),(q,r+1,q+1),(q+1,r+1,r+2),(q+1,r+2,q+2),(q+3,r+3,r,q),(q+2,r+2,r+4,q+4),(q+4,r+4,r+3,q+3)])
 faces.extend([(0,1,2,4,3),(5*(N-1)+3,5*(N-1)+4,5*(N-1)+2,5*(N-1)+1,5*(N-1))])
 mesh('Landscape / limestone gorge bank '+str(side),verts,faces,stone_mat)
 # Low green patches sit on outer toes, outside channel.
 for i in range(9):
  x=-1.15+i*.28;y=side*(.66+.10*math.sin(x*3+side))
  stone('Landscape / green bank accent',(x,y,2.02),(.12,.065,.035),lid,green,2)
'''
a+=s[s.index('# Medallion'):]
a=a.replace('japan.blend','slovenia.blend').replace('japan.glb','slovenia.glb').replace('JAPAN AUTHORED','SLOVENIA AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
(R/'author.py').write_text(a,encoding='utf8')
print('AUTHOR_ASSEMBLED')
