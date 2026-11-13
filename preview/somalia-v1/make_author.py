"""Construct this pilot's standalone author from the read-only mechanism lineage."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
s=s[:s.index('wood=mat')]+'''stonebody=mat('Coral limestone / warm porous',(.65,.52,.35),.78);maptex(stonebody,'limestone-color.png','Base Color');maptex(stonebody,'limestone-roughness.png','Roughness',True)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / deep teal',(.018,.09,.10),.85)
granite=stonebody
sand=mat('Merka / rust dune sand',(.50,.22,.095),.88);maptex(sand,'dune-color.png','Base Color')
water=mat('Indian Ocean / teal blue',(.018,.24,.32),.24,.12)
shore=mat('Shore / pale sand',(.72,.61,.40),.8)
wood=stonebody
'''+s[s.index('def uv('):s.index('# Exterior skins')]+'''# Continuous stone skins; no inherited cedar finger joints.
for sy in [-1,1]:cube('Limestone / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),stonebody,bevel=.025)
for sx in [-1,1]:cube('Limestone / end wall',(sx*1.745,0,.83),(.23,2.10,1.46),stonebody,bevel=.025)
'''+s[s.index('# Small collar'):s.index('# A thin satin')]+s[s.index('# Restrained brass'):s.index("stone('Terrain / granite'")]+'''# Inlaid stylized sea and pale shoreline, all carried by lid.
cube('Ocean / inlay',(0,0,1.989),(3.12,1.70,.025),water,lid,.009)
cube('Shore / coastal edge',(0,.12,2.011),(3.02,.10,.035),shore,lid,.012)
# Closed, asymmetric cross sections with nonrepeating gently curved crests.
for k,(cy,width,height,length) in enumerate([(.48,.40,.34,2.85),(-.13,.32,.27,2.72),(-.60,.28,.19,2.60)]):
 verts=[];faces=[];nx=48;ny=10
 for i in range(nx+1):
  u=i/nx;x=(u-.5)*length;env=max(0,math.sin(math.pi*u))**.65
  center=cy+.065*math.sin(u*math.tau+k)
  for j in range(ny+1):
   v=j/ny;cross=max(0,1-abs((v-.42)/(.42 if v<.42 else .58)))
   verts.append((x,center+(v-.5)*width,2.004+height*env*cross**.8))
 for i in range(nx):
  for j in range(ny):
   a=i*(ny+1)+j;faces.append((a,a+ny+1,a+ny+2,a+1))
 boundary=list(range(ny+1))+[i*(ny+1)+ny for i in range(1,nx+1)]+[nx*(ny+1)+j for j in range(ny-1,-1,-1)]+[i*(ny+1) for i in range(nx-1,0,-1)]
 for a,b in zip(boundary,boundary[1:]+boundary[:1]):
  n=len(verts);verts.extend([(verts[a][0],verts[a][1],1.997),(verts[b][0],verts[b][1],1.997)]);faces.append((a,n,n+1,b))
 me=bpy.data.meshes.new('Sculpted dune surface');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Merka dune / ridge '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(sand);uv(o);parent(o)
 for f in me.polygons:f.use_smooth=True
'''+s[s.index('# Medallion'):]
a=s.index("def uv(");b=s.index('def cube(',a)
s=s[:a]+'''def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone spatial projection')
 for p in o.data.polygons:
  ax=max(range(3),key=lambda i:abs(p.normal[i]));indices=[i for i in range(3) if i!=ax]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[indices[0]]*.5+.5,co[indices[1]]*.5+.5)
'''+s[b:]
s=s.replace('Cedar / clasp seat','Limestone / clasp seat').replace('Cedar / rim corner','Limestone / rim corner').replace('Granite foot','Limestone foot').replace("japan.blend","somalia.blend").replace("japan.glb","somalia.glb").replace('JAPAN AUTHORED','SOMALIA AUTHORED')
s=s.replace('4.5));cam','6.1));cam').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=1000').replace('resolution_y=1000','resolution_y=900')
s=s.replace('Reference-led Japan pilot.','Somalia Merka dunes pilot.')
(R/'author.py').write_text(s,encoding='utf8')
