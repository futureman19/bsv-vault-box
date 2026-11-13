"""One-time lineage adaptation; reads Japan helpers, writes only this folder."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
head=s[s.index('import bpy'):s.index("wood=mat")]
helpers=s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
helpers=helpers[:helpers.index('def cube')]+helpers[helpers.index('def cube'):]
# Stone surfaces use physical-scale dominant-face UV projection, not wood axes.
a=helpers.index('def uv(');b=helpers.index('def cube(')
helpers=helpers[:a]+'''def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone projection')
 for p in o.data.polygons:
  n=p.normal; omit=max(range(3),key=lambda i:abs(n[i])); axes=[i for i in range(3) if i!=omit]
  for li in p.loop_indices:
   co=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]*.65,co[axes[1]]*.65)
'''+helpers[b:]
materials='''stone_mat=mat('Limestone / warm porous cream',(.5,.45,.31),.8);maptex(stone_mat,'limestone-color.png','Base Color');maptex(stone_mat,'limestone-roughness.png','Roughness',True)
shale=mat('Shale / blue grey',(.15,.19,.23),.85);maptex(shale,'shale-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
forest=mat('Lid / deep forest green',(.0168,.0612,.0467),.52)
seam=mat('Mineral seam / forest shadow',(.025,.047,.032),.9)
terrain_mats=[mat('Forest / '+str(i),c,.92) for i,c in enumerate([(.024,.085,.052),(.04,.125,.071),(.064,.17,.092),(.09,.21,.115)])]+[shale,stone_mat]
'''
body='''for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone_mat if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Limestone / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),stone_mat,bevel=.025)
for sx in [-1,1]:cube('Limestone / end wall',(sx*1.745,0,.83),(.23,2.10,1.46),stone_mat,bevel=.025)
cube('Limestone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone_mat,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Limestone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone_mat,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),forest,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Limestone / carved foot',(sx*1.47,sy*.91,-.07),(.48,.43,.31),stone_mat,bevel=.075)
# A connected triangulated relief with multiple asymmetric wooded ridges.
# Perimeter conforms to an irregular ellipse, with no rectangular display plinth.
verts=[(0,.05,2.48)];faces=[];rings=24;segments=112
for j in range(1,rings+1):
 r=j/rings
 for k in range(segments):
  a=k*math.tau/segments;edge=1+.025*math.sin(a*7)+.018*math.cos(a*11)
  x=1.40*r*math.cos(a)*edge;y=.05+.72*r*math.sin(a)*edge
  peaks=sum(h*math.exp(-((x-cx)/wx)**2-((y-cy)/wy)**2) for cx,cy,h,wx,wy in [(-.84,.06,.52,.36,.29),(-.10,.23,.71,.39,.33),(.65,.02,.58,.42,.30)])
  z=1.975+peaks*(1-r**8)+.027*math.sin(x*28+y*17)*math.sin(y*26-x*13)*(1-r)
  verts.append((x,y,z))
for k in range(segments):faces.append((0,1+k,1+(k+1)%segments))
for j in range(rings-1):
 for k in range(segments):
  a=1+j*segments+k;b=1+j*segments+(k+1)%segments;c=a+segments;d=b+segments
  faces.extend([(a,c,d),(a,d,b)])
mesh=bpy.data.meshes.new('Connected wooded mountain surface');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Terrain / Blue and John Crow relief',mesh);bpy.context.collection.objects.link(o)
for m in terrain_mats:mesh.materials.append(m)
for f in mesh.polygons:
 c=f.center
 f.material_index=5 if c.x>.75 and c.y<.05 and c.z>2.10 else (4 if f.normal.z<.58 else random.randrange(4))
 f.use_smooth=False
uv(o);parent(o)
'''
med=s[s.index('def disk('):s.index('# Clean obsolete')]
footer=s[s.index('# Clean obsolete'):].replace('japan.blend','jamaica.blend').replace('japan.glb','jamaica.glb').replace('JAPAN AUTHORED','PASS JAMAICA AUTHORED')
footer=footer.replace("scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000", "scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=1000;scene.render.resolution_y=900")
(R/'author.py').write_text('"""Jamaica brief-driven landscape; procedural Blender source, no scans."""\n'+head+materials+helpers+body+med+footer)
print('Author generated from declared mechanical/helper lineage')
