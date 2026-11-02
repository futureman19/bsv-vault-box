for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone_mat if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Limestone / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),stone_mat,bevel=.025)
for sx in [-1,1]:cube('Limestone / end wall',(sx*1.745,0,.83),(.23,2.10,1.46),stone_mat,bevel=.025,axis='Y')
cube('Limestone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone_mat,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Limestone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone_mat,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone_mat,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# Closed relief mesh: nested scalloped elliptical rings and triangulated floor.
# Outer contour seats into the lid; basin floor is higher than lid top.
N=96
rings=[(.20,2.025),(.42,2.035),(.59,2.065),(.70,2.12),(.78,2.31),(.86,2.40),(.94,2.30),(1.0,1.97)]
verts=[(-.10,0,2.02)];faces=[];mats=[]
for ri,(r,z) in enumerate(rings):
 for j in range(N):
  a=math.tau*j/N;w=1+.045*math.sin(5*a+.4)+.025*math.sin(11*a)+.018*math.cos(17*a)
  x=1.48*r*math.cos(a)*w-.10*(1-r);y=.82*r*math.sin(a)*w
  height=z+(r**2)*(.055*math.sin(3*a)+.025*math.sin(13*a))
  verts.append((x,y,height))
for j in range(N):faces.append((0,1+j,1+(j+1)%N));mats.append(0)
for ri in range(len(rings)-1):
 for j in range(N):
  a=1+ri*N+j;b=1+ri*N+(j+1)%N;c=b+N;d=a+N
  faces.extend([(a,d,c),(a,c,b)]);mats.extend([1 if ri>=4 else (2 if ri==2 else 0)]*2)
# Orient all top triangles upward, independent of ring-winding convention.
for i,f in enumerate(faces):
 if (Vector(verts[f[1]])-Vector(verts[f[0]])).cross(Vector(verts[f[2]])-Vector(verts[f[0]])).z<0:faces[i]=tuple(reversed(f))
faces.append(tuple(reversed([1+(len(rings)-1)*N+j for j in range(N)])));mats.append(1)
me=bpy.data.meshes.new('Eroded basin relief');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / Negev erosion basin',me);bpy.context.collection.objects.link(o)
for m in [sand,chalk,shade]:me.materials.append(m)
for p,mi in zip(me.polygons,mats):p.material_index=mi
parent(o,lid)
