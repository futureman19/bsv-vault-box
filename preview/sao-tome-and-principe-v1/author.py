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
granite=mat('Phonolite / graphite olive',(.15,.17,.13),.8);maptex(granite,'stone-color.png','Base Color');maptex(granite,'stone-roughness.png','Roughness',True)
wood=granite
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Forest / green reveal',(.035,.07,.032),.9)
forest=mat('Forest / terrain',(.055,.13,.035),.9);maptex(forest,'forest-color.png','Base Color')
canopy=[mat('Forest / canopy '+str(i),c,.9) for i,c in enumerate([(.055,.13,.027),(.075,.17,.035),(.10,.20,.045)])]
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z
   if axis=='Y' and abs(p.normal.z)>.7:v=co.x
   layer.data[li].uv=(u*.65+.5,v*.65+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
def stone(n,loc,scale,p=None,material=granite,sub=2):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  k=1+random.uniform(-.11,.11);v.co=Vector((v.co.x*scale[0]*k,v.co.y*scale[1]*k,v.co.z*scale[2]*k))
 o.data.materials.append(material);uv(o)
 for face in o.data.polygons:face.use_smooth=True
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(granite if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Phonolite / body long',(0,sy*1.145,.83),(3.72,.19,1.46),granite,bevel=.025)
for sx in [-1,1]:cube('Phonolite / body side',(sx*1.745,0,.83),(.23,2.48,1.46),granite,bevel=.025)
cube('Phonolite / clasp seat',(0,-1.255,1.36),(.56,.075,.47),granite,bevel=.025)
for sy in [-1,1]:cube('Forest / seam long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Forest / seam side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Phonolite / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),granite,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),granite,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  stone('Phonolite foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
def mesh(n,v,f,m):
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(m);uv(o);parent(o);return o
# Irregular forest island: closed skirt seated into the stone lid.
N=64;v=[(0,0,2.16)];f=[]
for k in range(1,9):
 r=k/8
 for j in range(N):
  a=j*math.tau/N;edge=1+.07*math.sin(3*a)+.045*math.cos(5*a)
  x=1.34*r*math.cos(a)*edge;y=.72*r*math.sin(a)*edge
  z=1.98+.18*(1-r*r)+.018*math.sin(x*7)*math.sin(y*6)*(1-r)
  v.append((x,y,z))
for j in range(N):f.append((0,1+j,1+(j+1)%N))
for k in range(7):
 for j in range(N):
  a=1+k*N+j;b=1+k*N+(j+1)%N;f.append((a,a+N,b+N,b))
base=len(v)
for j in range(N):x,y,z=v[1+7*N+j];v.append((x,y,1.973))
for j in range(N):a=1+7*N+j;b=1+7*N+(j+1)%N;f.append((a,base+j,base+(j+1)%N,b))
f.append(tuple(reversed(range(base,base+N))))
terrain=mesh('Terrain / rainforest bed',v,f,forest)
for p in terrain.data.polygons:p.use_smooth=True
# Phonolitic needle: near-vertical irregular walls then rounded asymmetrical cap.
N=40;levels=[(2.09,.36),(2.23,.33),(2.42,.29),(2.63,.25),(2.85,.21),(3.02,.15),(3.12,.075)]
v=[];f=[]
for k,(z,r) in enumerate(levels):
 for j in range(N):
  a=j*math.tau/N;flute=1+.055*math.sin(9*a)+.045*math.cos(5*a+.4);cx=.4+.04*k/6;cy=.28+.035*math.sin(k/6*2)
  v.append((cx+r*flute*math.cos(a),cy+r*.86*flute*math.sin(a),z+.008*math.sin(3*a)))
for k in range(len(levels)-1):
 for j in range(N):a=k*N+j;b=k*N+(j+1)%N;f.append((a,b,b+N,a+N))
f.append(tuple(reversed(range(N))));v.append((.44,.31,3.145));top=len(v)-1
for j in range(N):f.append(((len(levels)-1)*N+j,(len(levels)-1)*N+(j+1)%N,top))
needle=mesh('Terrain / Pico Cao Grande inspired needle',v,f,granite)
for p in needle.data.polygons:p.use_smooth=True
# Distinct leafy canopy patches around the rock, each seated in terrain.
for i in range(54):
 a=i*2.399;r=.28+.58*((i%11)/10)**.5;x=1.20*r*math.cos(a);y=.64*r*math.sin(a)
 if ((x-.4)/.40)**2+((y-.28)/.36)**2<1:continue
 rr=((x/1.34)**2+(y/.72)**2)**.5;z=1.98+.18*(1-rr*rr)+.018*math.sin(x*7)*math.sin(y*6)*(1-rr)
 size=.10+.035*random.random()
 stone('Terrain / forest canopy', (x,y,z+.025),(size,size*.84,.08),lid,canopy[0 if x<-.3 else (1 if y<.1 else 2)],2)
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
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.2));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.35))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.render.resolution_x=1000;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'sao-tome-and-principe.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'sao-tome-and-principe.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('SAO TOME AND PRINCIPE AUTHORED')
