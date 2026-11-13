"""Estonia limestone and abstract bog; authored mesh, no copied imagery."""
import bpy,math,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(372)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def parent(o,p=lid):
 bpy.context.view_layer.update();m=o.matrix_world.copy();o.parent=p;o.matrix_world=m;return o
def mat(n,c,r=.7,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
stone=mat('Limestone / pale mineral',(.42,.44,.38));p=stone.node_tree.nodes.get('Principled BSDF')
for file,inp in [('limestone-color.png','Base Color'),('limestone-roughness.png','Roughness'),('limestone-normal.png','Normal')]:
 t=stone.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file));t.image.pack()
 if inp!='Base Color':t.image.colorspace_settings.name='Non-Color'
 if inp=='Normal':
  n=stone.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.32;stone.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);stone.node_tree.links.new(n.outputs['Normal'],p.inputs[inp])
 else:stone.node_tree.links.new(t.outputs['Color'],p.inputs[inp])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / peat green',(.035,.055,.028),.92)
peat=mat('Bog / peat rim',(.17,.105,.035),.95)
moss=mat('Bog / olive moss',(.18,.23,.055),.94)
water=mat('Bog / dark reflecting pools',(.018,.075,.085),.16,.12)
wood=mat('Boardwalk / weathered ochre',(.31,.23,.12),.8)
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone projection')
 for p in o.data.polygons:
  axis=max(range(3),key=lambda a:abs(p.normal[a]));a,b=[i for i in range(3) if i!=axis]
  for li in p.loop_indices:
   v=o.data.vertices[o.data.loops[li].vertex_index].co;layer.data[li].uv=(v[a]/1.5+.5,v[b]/1.5+.5)
def cube(n,loc,dim,m,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if bevel:
  mod=o.modifiers.new('Soft edges','BEVEL');mod.width=min(bevel,min(dim)*.30);mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Limestone / front rear skin',(0,sy*1.145,.83),(3.26,.19,1.46),stone)
for sx in [-1,1]:cube('Limestone / side skin',(sx*1.745,0,.83),(.23,2.48,1.46),stone)
cube('Limestone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam)
 for sy in [-1,1]:cube('Limestone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Limestone / foot',(sx*1.47,sy*.91,-.10),(.58,.49,.32),stone,bevel=.06)
# Rings are closed annular solids with irregular silhouettes and real recesses.
for k,(cx,cy,rx,ry) in enumerate([(-.85,.25,.47,.47),(.05,.36,.34,.43),(.88,.18,.43,.51)]):
 N=64;v=[];f=[]
 for ring in range(4):
  for j in range(N):
   a=j*math.tau/N;w=1+.065*math.sin(3*a+k)+.035*math.cos(5*a-k);scale=.73 if ring in [1,2] else 1
   z=(2.105+.025*math.sin(a*3+k)) if ring<2 else 1.973
   v.append((cx+rx*scale*w*math.cos(a),cy+ry*scale*w*math.sin(a),z))
 for ring,other in [(0,1),(1,2),(2,3),(3,0)]:
  for j in range(N):f.append((ring*N+j,ring*N+(j+1)%N,other*N+(j+1)%N,other*N+j))
 me=bpy.data.meshes.new('Organic closed peat ring');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new('Bog / rim '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(moss);me.materials.append(peat)
 for face in me.polygons:face.material_index=0 if face.index<N else 1;face.use_smooth=True
 parent(o)
 # Filled inner water disc beneath the raised rim, no stacked image plane.
 verts=[(cx,cy,2.015)]+[(cx+rx*.78*(1+.065*math.sin(3*j*math.tau/N+k)+.035*math.cos(5*j*math.tau/N-k))*math.cos(j*math.tau/N),cy+ry*.78*(1+.065*math.sin(3*j*math.tau/N+k)+.035*math.cos(5*j*math.tau/N-k))*math.sin(j*math.tau/N),2.015) for j in range(N)]
 me=bpy.data.meshes.new('Pool surface');me.from_pydata(verts,[],[(0,j+1,(j+1)%N+1) for j in range(N)]);me.update();o=bpy.data.objects.new('Bog / water '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o)
for i in range(18):
 x=-1.36+i*2.72/17;cube('Boardwalk / plank '+str(i),(x,-.51,2.012),(.145,.30,.066),wood,lid,.008)
# Small clumps seated in the top annulus, not ungrounded grass sprites.
for k,(cx,cy,rx,ry) in enumerate([(-.85,.25,.47,.47),(.05,.36,.34,.43),(.88,.18,.43,.51)]):
 for j in range(13):
  a=j*math.tau/13;w=1+.065*math.sin(3*a+k)+.035*math.cos(5*a-k);z=2.105+.025*math.sin(a*3+k)
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(cx+rx*.87*w*math.cos(a),cy+ry*.87*w*math.sin(a),z));o=bpy.context.object;o.name='Bog / moss cushion';o.scale=(.055,.045,.028);o.data.materials.append(moss);parent(o)
def disk(n,loc,r,d,rot):
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=d,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold)
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035,(math.pi/2,0,0))
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=32,minor_segments=8,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
for m in list(bpy.data.materials):
 if not m.users:bpy.data.materials.remove(m)
for im in list(bpy.data.images):
 if not im.users:bpy.data.images.remove(im)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.28
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.05))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
s=bpy.context.scene;s.camera=cam;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=1000;s.render.resolution_y=900;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.use_nodes=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'estonia.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'estonia.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
s.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('ESTONIA AUTHORED PASS')
