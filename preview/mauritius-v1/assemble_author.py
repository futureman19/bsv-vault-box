"""One-time author bootstrap from reviewed family geometry helpers."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
a=s[:s.index('wood=mat')]
a+='''earth=mat('Chamarel / weathered earth',(.38,.16,.085),.8);maptex(earth,'earth-color.png','Base Color');maptex(earth,'earth-roughness.png','Roughness',True)
granite=mat('Basalt / dark volcanic feet',(.06,.065,.075),.88);maptex(granite,'basalt.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / dark earth',(.04,.025,.02),.9)
'''
a+=s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
a+='''for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(earth if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Earth / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),earth,bevel=.028)
for sx in [-1,1]:cube('Earth / end wall',(sx*1.745,0,.83),(.23,2.10,1.46),earth,bevel=.028)
cube('Earth / clasp seat',(0,-1.255,1.36),(.56,.075,.47),earth,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Earth / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),earth,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),earth,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
'''
a+=s[s.index('def stone('):s.index("stone('Terrain / granite'")]
a+='''# A shared continuous heightfield split along seven curved mineral ribbons.
# No intersecting overlapping dunes; all material boundaries share coordinates.
palette=['a65e45','bf914c','68483c','79617c','946b83','61748a','7c8055']
def lin(v):
 v=v/255;return v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4
for k,h in enumerate(palette):
 material=mat('Earth ribbon / '+str(k),tuple(lin(int(h[j:j+2],16)) for j in (0,2,4)),.85)
 verts=[];faces=[];nx=64;ny=8
 for j in range(ny+1):
  v=(k+j/ny)/7
  for i in range(nx+1):
   u=i/nx;x=-1.54+3.08*u
   y=-.89+1.78*v+.12*math.sin(u*math.tau+v*2)*math.sin(math.pi*v)
   edge=math.sin(math.pi*u)**.6*math.sin(math.pi*v)**.6
   z=1.993+edge*(.13+.09*math.sin(x*4+y*5)+.08*math.sin(x*1.3-y*3)**2)
   verts.append((x,y,z))
 for j in range(ny):
  for i in range(nx):
   q=j*(nx+1)+i;faces.append((q,q+1,q+nx+2,q+nx+1))
 me=bpy.data.meshes.new('Dune ribbon');me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new('Dune / ribbon '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(material)
 for p in me.polygons:p.use_smooth=True
 parent(o)
'''
a+=s[s.index('# Medallion'):]
a=a.replace('japan.blend','mauritius.blend').replace('japan.glb','mauritius.glb').replace('JAPAN AUTHORED','MAURITIUS AUTHORED').replace('Reference-led Japan pilot','Chamarel landscape-inspired Mauritius pilot')
(R/'author.py').write_text(a)
