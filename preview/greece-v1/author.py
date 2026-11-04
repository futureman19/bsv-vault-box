"""Greece: procedurally authored marble vessel and fanlight-inspired lid relief."""
import bpy, math, random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
marble=mat('Tinian-inspired / ivory veined marble',(.70,.73,.70),.45)
for filename,socket in [('marble-color.png','Base Color'),('marble-roughness.png','Roughness'),('marble-normal.png','Normal')]:
 t=marble.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/filename));t.image.pack()
 if socket!='Base Color':t.image.colorspace_settings.name='Non-Color'
 if socket=='Normal':
  n=marble.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.35;marble.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);marble.node_tree.links.new(n.outputs['Normal'],marble.node_tree.nodes.get('Principled BSDF').inputs[socket])
 else:marble.node_tree.links.new(t.outputs['Color'],marble.node_tree.nodes.get('Principled BSDF').inputs[socket])
gold=mat('Brass / satin',(.48,.30,.10),.28,.8);blue=mat('Aegean / blue enamel',(.018,.11,.22),.30);seam=mat('Seam / deep blue',(.012,.035,.055),.8)
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone physical projection')
 for p in o.data.polygons:
  axis=max(range(3),key=lambda a:abs(p.normal[a]));a,b=[i for i in range(3) if i!=axis]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;layer.data[li].uv=(co[a]/2+.5,co[b]/2+.5)
def cube(n,loc,dim,m,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if bevel:
  mod=o.modifiers.new('Soft stone edge','BEVEL');mod.width=min(bevel,min(dim)*.35);mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(marble if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Butt-jointed continuous skins, no coplanar overlapping corner faces.
for sy in [-1,1]:cube('Marble skin / front' if sy<0 else 'Marble skin / rear',(0,sy*1.145,.83),(3.26,.19,1.46),marble,bevel=.008)
for sx in [-1,1]:cube('Marble skin / side',(sx*1.745,0,.83),(.23,2.48,1.46),marble,bevel=.008)
cube('Marble / clasp seat',(0,-1.255,1.36),(.56,.075,.47),marble,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Marble / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),marble,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),marble,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Marble foot',(sx*1.47,sy*.91,-.10),(.56,.46,.36),marble,bevel=.08)
# Blue fine inset frame, deliberately below the broad relief.
for sy in [-1,1]:cube('Inlay / long',(0,sy*.91,1.981),(2.95,.025,.009),blue,lid,.002)
for sx in [-1,1]:cube('Inlay / short',(sx*1.475,0,1.981),(.025,1.82,.009),blue,lid,.002)
def arc(n,ri,ro,z0,z1,material,steps=48):
 v=[];f=[]
 for i in range(steps+1):
  a=math.pi*i/steps
  for r,z in [(ri,z0),(ro,z0),(ri,z1),(ro,z1)]:v.append((r*math.cos(a),-.20+r*math.sin(a),z))
 for i in range(steps):
  j=i*4;k=j+4;f.extend([(j,k,k+1,j+1),(j+2,j+3,k+3,k+2),(j,j+2,k+2,k),(j+1,k+1,k+3,j+3)])
 f.extend([(0,1,3,2),(steps*4,steps*4+2,steps*4+3,steps*4+1)])
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o,lid);return o
arc('Fanlight / outer arch',.70,.80,1.978,2.085,marble)
arc('Fanlight / blue center',.01,.20,1.978,2.045,blue)
cube('Fanlight / sill',(0,-.20,2.025),(1.68,.10,.094),marble,lid,.015)
for i in range(7):
 a=(i+1)*math.pi/8;r=.46;o=cube('Fanlight / radial rib '+str(i),(r*math.cos(a),-.20+r*math.sin(a),2.029),(.56,.052,.102),marble,None,.009);o.rotation_euler.z=a;parent(o,lid)
# Compact brass plaque and side ring, inherited family extrapolations.
def disk(n,loc,r,depth,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=r,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold);return o
disk('Medallion / plain',(0,-1.258,.87),.13,.035)
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=10,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / brass';bpy.context.object.data.materials.append(gold)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.30
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.8));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.12))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=1000;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'greece.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'greece.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('GREECE AUTHORED PASS')
