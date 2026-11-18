import bpy,bmesh,math,random,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(521)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p=lid):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def maptex(m,file,input,noncolor=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file),check_existing=True)
 if noncolor:t.image.colorspace_settings.name='Non-Color'
 t.image.pack();m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[input])
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Mineral projection')
 for p in o.data.polygons:
  normal=p.normal
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co + o.location
   if abs(normal.z)>.7:u,v=co.x,co.y
   elif abs(normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u/3.72+.5,v/2.38+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
# Country-specific material and landscape authoring, appended to family helpers.
mineral=mat('Atacama / terracotta sediment',(.32,.12,.065),.8)
maptex(mineral,'desert-color.png','Base Color');maptex(mineral,'desert-roughness.png','Roughness',True)
t=mineral.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/desert-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();nm=mineral.node_tree.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.28;mineral.node_tree.links.new(t.outputs['Color'],nm.inputs['Color']);mineral.node_tree.links.new(nm.outputs['Normal'],mineral.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Copper brass / brushed warm',(.48,.235,.105),.32,.78)
liner=mat('Interior / dark mineral',(.085,.055,.040),.8)
seam=mat('Gasket / dark umber',(.025,.018,.013),.9)
sand=mat('Terrain / ochre',(.48,.265,.115),.87)
salt=mat('Salt / warm ivory',(.79,.75,.62),.94)
ridge=mat('Ridge / oxidized umber',(.26,.10,.05),.9)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(liner if o.name.startswith('Interior') else gold)
for sy in [-1,1]:cube('Desert shell / front' if sy<0 else 'Desert shell / rear',(0,sy*1.145,.83),(3.72,.19,1.46),mineral,bevel=.025)
for sx in [-1,1]:cube('Desert shell / side',(sx*1.745,0,.83),(.23,2.10,1.46),mineral,bevel=.025)
cube('Desert shell / clasp seat',(0,-1.255,1.36),(.56,.075,.47),mineral,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Mineral rim / corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),mineral,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),mineral,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# Irregular closed terrain meshes, no photographic terrain planes.
def polygon_prism(name,points,z,height,material):
 vs=[(x,y,z) for x,y in points]+[(x,y,z+height) for x,y in points];n=len(points)
 faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(material);parent(o);uv(o);return o
polygon_prism('Terrain / desert island',[(-1.55,-.72),(-.9,-.93),(.45,-.84),(1.5,-.38),(1.48,.7),(.4,.94),(-1.38,.72)],1.978,.075,sand)
# Separate cracked salt cells, laid over a continuous recessed pale basin.
polygon_prism('Salt basin / bed',[(-1.1,-.52),(-.6,-.73),(.5,-.64),(.88,-.25),(.65,.12),(-.5,.18),(-1.16,-.1)],2.053,.014,salt)
# Voronoi cells clipped to a convex salt-basin inner boundary.
bound=[(-.98,-.44),(-.56,-.64),(.45,-.55),(.73,-.23),(.55,.04),(-.45,.10),(-1.02,-.10)]
seeds=[(-.85+i*.24+random.uniform(-.055,.055),-.47+j*.21+random.uniform(-.045,.045)) for i in range(7) for j in range(3)]
def clip(poly,a,b):
 # Half-plane closer to a than b.
 nx=b[0]-a[0];ny=b[1]-a[1];d=(b[0]**2+b[1]**2-a[0]**2-a[1]**2)/2
 out=[]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  fp=p[0]*nx+p[1]*ny-d;fq=q[0]*nx+q[1]*ny-d
  if fp<=0:out.append(p)
  if (fp<=0)!=(fq<=0):t=fp/(fp-fq);out.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
 return out
for i,a in enumerate(seeds):
 poly=bound[:]
 for b in seeds:
  if a!=b and poly:poly=clip(poly,a,b)
 if len(poly)<3:continue
 cx=sum(v[0] for v in poly)/len(poly);cy=sum(v[1] for v in poly)/len(poly)
 poly=[(cx+(x-cx)*.94,cy+(y-cy)*.94) for x,y in poly]
 polygon_prism('Salt crust / cell %02d'%i,poly,2.067,.012+random.random()*.009,salt)
def mountain(name,cx,cy,rx,ry,height):
 N=17;verts=[]
 for ring in range(3):
  r=[1,.48,.12][ring]
  for j in range(N):
   a=j*math.tau/N;rr=r*(1+random.uniform(-.12,.12));z=2.047+height*[0,.52,.91][ring]+random.uniform(0,.035)
   verts.append((cx+math.cos(a)*rx*rr,cy+math.sin(a)*ry*rr,z))
 verts.append((cx+.06,cy,2.047+height));faces=[tuple(reversed(range(N)))]
 for ring in range(2):
  for j in range(N):
   a=ring*N+j;b=ring*N+(j+1)%N;faces.extend([(a,b,a+N),(b,b+N,a+N)])
 for j in range(N):faces.append((2*N+j,2*N+(j+1)%N,3*N))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(ridge);me.materials.append(sand)
 for face in me.polygons:face.material_index=1 if random.random()<.22 else 0
 parent(o);uv(o)
mountain('Ridge / western folded desert',-.72,.53,.67,.31,.43)
mountain('Ridge / eastern volcanic silhouette',.77,.48,.56,.39,.64)
def stone(n,loc,scale,p=None,material=mineral,sub=2):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  k=1+random.uniform(-.11,.11);v.co=Vector((v.co.x*scale[0]*k,v.co.y*scale[1]*k,v.co.z*scale[2]*k))
 o.data.materials.append(material);uv(o)
 for face in o.data.polygons:face.use_smooth=True
 if p:parent(o,p)
 return o
for sx in [-1,1]:
 for sy in [-1,1]:stone('Desert stone foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)
# Medallion is solid, never an unexplained front opening.
def disk(n,loc,r,depth,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold);m=o.modifiers.new('Rounded brass','BEVEL');m.width=.005;m.segments=3;select(o);bpy.ops.object.modifier_apply(modifier=m.name);return o
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035)
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(0,-1.282,.87),major_radius=.107,minor_radius=.008,rotation=(math.pi/2,0,0));bpy.context.object.name='Medallion / raised rim';bpy.context.object.data.materials.append(gold)
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
# Clean obsolete unreferenced theme resources from source.
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
# Studio rendering is a real render of the exact exported mesh.
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'chile.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'chile.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('CHILE AUTHORED')
