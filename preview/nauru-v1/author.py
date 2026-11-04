"""Brief-led Nauru pilot. Authored mesh and maps; no photogrammetry.
Run maps.py first. Reproduction uses only the included trimmed mechanism.blend.
"""
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
wood=mat('Coral limestone / porous ivory',(.62,.57,.43),.8)
maptex(wood,'limestone-color.png','Base Color');maptex(wood,'limestone-roughness.png','Roughness',True)
t=wood.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/limestone-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();nm=wood.node_tree.nodes.new('ShaderNodeNormalMap');wood.node_tree.links.new(t.outputs['Color'],nm.inputs['Color']);wood.node_tree.links.new(nm.outputs['Normal'],wood.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
granite=wood
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / muted deep teal',(.025,.065,.06),.85)
water=mat('Lagoon / muted turquoise',(.035,.28,.27),.22,.12)
scrub=mat('Coastal scrub / olive',(.12,.17,.055),.95)
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Isotropic limestone')
 for p in o.data.polygons:
  dominant=max(range(3),key=lambda k:abs(p.normal[k]));axes=[k for k in range(3) if k!=dominant]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]*.65+.5,co[axes[1]]*.65+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o

for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Limestone / front' if sy<0 else 'Limestone / rear',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.025)
for sx in [-1,1]:cube('Limestone / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.025)
cube('Limestone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Limestone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def stone(n,loc,scale,p=None,material=granite,sub=2):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  k=1+random.uniform(-.11,.11);v.co=Vector((v.co.x*scale[0]*k,v.co.y*scale[1]*k,v.co.z*scale[2]*k))
 o.data.materials.append(material);uv(o)
 for face in o.data.polygons:face.use_smooth=True
 if p:parent(o,p)
 return o

for sx in [-1,1]:
 for sy in [-1,1]:stone('Limestone foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
# Concentric but offset irregular rings make an actual basin with sloping shores.
N=48;center=(-.35,-.20);verts=[];faces=[]
for ring in range(4):
 for j in range(N):
  a=j*math.tau/N;w=1+.055*math.sin(3*a)+.035*math.cos(7*a)
  if ring==0:x,y,z=center[0]+.58*w*math.cos(a),center[1]+.36*w*math.sin(a),2.025
  elif ring==1:x,y,z=center[0]+.70*w*math.cos(a),center[1]+.46*w*math.sin(a),2.12
  else:x,y,z=1.46*w*math.cos(a),.79*w*math.sin(a),2.105 if ring==2 else 1.965
  verts.append((x,y,z))
for k in range(3):
 for j in range(N):a=k*N+j;b=k*N+(j+1)%N;faces.append((a+N,b+N,b,a))
me=bpy.data.meshes.new('Limestone terrace rings');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / basin terrace',me);bpy.context.collection.objects.link(o);me.materials.append(wood);uv(o);parent(o)
# Water fan enclosed by inner shore; a tiny overlap buries the edge in the bank.
v=[(*center,2.045)]+[(center[0]+.60*(1+.055*math.sin(3*j*math.tau/N)+.035*math.cos(7*j*math.tau/N))*math.cos(j*math.tau/N),center[1]+.375*(1+.055*math.sin(3*j*math.tau/N)+.035*math.cos(7*j*math.tau/N))*math.sin(j*math.tau/N),2.045) for j in range(N)]
me=bpy.data.meshes.new('Lagoon surface');me.from_pydata(v,[],[(0,j+1,(j+1)%N+1) for j in range(N)]);me.update();o=bpy.data.objects.new('Terrain / inland lagoon',me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o)
# Eroded uneven limestone spires, rooted through the low terrace.
for i,(x,y,h,r) in enumerate([(-.95,.40,.28,.17),(-.57,.59,.42,.17),(-.12,.60,.60,.19),(.32,.57,.46,.18),(.73,.46,.63,.20),(1.03,.20,.39,.18),(.98,-.22,.31,.18),(.63,-.49,.23,.14)]):
 vs=[];fs=[];S=9
 for k,(z,scale) in enumerate([(2.06,1),(2.20,.88),(2.10+h*.65,.61),(2.10+h,.20)]):
  for j in range(S):
   a=j*math.tau/S;rad=r*scale*random.uniform(.82,1.18);vs.append((x+rad*math.cos(a)+k*.013,y+rad*math.sin(a),z+random.uniform(-.018,.018)))
 for k in range(3):
  for j in range(S):a=k*S+j;b=k*S+(j+1)%S;fs.append((a,b,b+S,a+S))
 fs.extend([tuple(reversed(range(S))),tuple(3*S+j for j in range(S))]);me=bpy.data.meshes.new('Eroded pinnacle');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Pinnacle / '+str(i+1),me);bpy.context.collection.objects.link(o);me.materials.append(wood);uv(o);parent(o)
for x,y in [(-1.1,-.18),(-.85,-.54),(.13,-.58),(.43,.30)]:stone('Terrain / olive scrub',(x,y,2.115),(.13,.09,.045),lid,scrub,2)
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
bpy.ops.object.camera_add(location=(-5.6,-7.8,4.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=2;scene.use_nodes=False;scene.render.resolution_x=1000;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'nauru.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'nauru.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('NAURU AUTHORED')
