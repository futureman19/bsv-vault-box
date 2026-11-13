exec(compile((__import__('pathlib').Path(__file__).parent/'helpers.py').read_text(),'helpers.py','exec'))
lacquer=mat('Lacquer / midnight',(.012,.025,.028),.24)
maptex(lacquer,'lacquer.png','Base Color');maptex(lacquer,'roughness.png','Roughness',True)
gold=mat('Brass / satin',(.48,.30,.10),.28,.8)
pearl=mat('Pearl / generated nacre',(.7,.8,.75),.24,.22);maptex(pearl,'pearl.png','Base Color')
seam=mat('Seam / charcoal',(.008,.012,.014),.7)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(lacquer if o.name.startswith('Interior') else gold)
for sy in [-1,1]:cube('Lacquer / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),lacquer,bevel=.02)
for sx in [-1,1]:cube('Lacquer / side wall',(sx*1.745,0,.83),(.23,2.10,1.46),lacquer,bevel=.02)
cube('Lacquer / clasp seat',(0,-1.255,1.36),(.56,.075,.47),lacquer,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:
  cube('Lacquer / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),lacquer,bevel=.004)
  cube('Lacquer / foot',(sx*1.47,sy*.91,-.08),(.46,.36,.30),lacquer,bevel=.045)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),lacquer,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# Pointed, shallow petal prisms: original radial motifs, not copied museum art.
def flower(n,c,r,u,v,p=None):
 c=Vector(c);u=Vector(u);v=Vector(v);normal=u.cross(v)
 verts=[];faces=[]
 for j in range(12):
  a=j*math.tau/12;d=u*math.cos(a)+v*math.sin(a);w=-u*math.sin(a)+v*math.cos(a)
  pts=[c+d*r*.18,c+d*r*.59+w*r*.14,c+d*r,c+d*r*.59-w*r*.14]
  k=len(verts);verts.extend(pts+[q+normal*.014 for q in pts]);faces.extend([(k,k+3,k+2,k+1),(k+4,k+5,k+6,k+7)]+[(k+i,k+(i+1)%4,k+(i+1)%4+4,k+i+4) for i in range(4)])
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(pearl);uv(o)
 if p:parent(o,p)
 return o
for i,(x,y,r) in enumerate([(-1.12,-.38,.32),(-.54,.34,.27),(0,-.16,.35),(.62,.36,.29),(1.18,-.28,.31)]):
 flower('Pearl / lid chrysanthemum '+str(i),(x,y,1.98),r,(1,0,0),(0,1,0),lid)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=1,location=(x,y,1.99));o=bpy.context.object;o.name='Brass / flower center';o.scale=(.053,.053,.025);o.data.materials.append(gold);parent(o)
points=[(-1.48+i*2.96/64,.23*math.sin(i*math.tau*2/64),1.985) for i in range(65)]
tube('Brass / scrolling stem',points,[.007]*65,gold,sides=6)
for sy in [-1,1]:
 cube('Pearl / long border',(0,sy*.91,1.985),(3.08,.018,.014),pearl,lid,.003)
 for x in [-1.13,-.67,.67,1.13]:flower('Pearl / body flower',(x,sy*1.243,.77),.20,(1,0,0),(0,0,-sy))
for sx in [-1,1]:
 cube('Pearl / end border',(sx*1.54,0,1.985),(.018,1.82,.014),pearl,lid,.003)
 for y in [-.48,.48]:flower('Pearl / side flower',(sx*1.862,y,.77),.23,(0,1,0),(0,0,sx))
bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=.13,depth=.035,location=(0,-1.258,.87),rotation=(math.pi/2,0,0));o=bpy.context.object;o.name='Medallion / solid emblem';o.data.materials.append(gold)
bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.085,depth=.035,location=(-1.875,0,1.05),rotation=(0,math.pi/2,0));o=bpy.context.object;o.name='Side ring / mount';o.data.materials.append(gold)
bpy.ops.mesh.primitive_torus_add(major_segments=32,minor_segments=8,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));o=bpy.context.object;o.name='Side ring / hanging brass';o.data.materials.append(gold)
for m in list(bpy.data.materials):
 if not m.users:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if not i.users:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.25
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.05))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=1000;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.use_nodes=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'south-korea.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'south-korea.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('SOUTH KOREA AUTHORED')
