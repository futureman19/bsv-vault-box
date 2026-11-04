"""Reference-led Papua New Guinea pilot. Authored mesh and maps; no photogrammetry.
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
wood=mat('Timber / warm dark frame',(.08,.035,.017),.48)
fibre=mat('Bilum inspired / looped plant fibre',(.45,.25,.09),.85)
maptex(fibre,'fibre-color.png','Base Color');maptex(fibre,'fibre-roughness.png','Roughness',True)
t=fibre.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/fibre-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack()
n=fibre.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.38;fibre.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);fibre.node_tree.links.new(n.outputs['Normal'],fibre.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / deep forest green',(.025,.052,.023),.92)
greens=[mat('Highlands / '+str(i),c,.93) for i,c in enumerate([(.045,.11,.037),(.08,.16,.055),(.12,.20,.073)])]
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z
   if axis=='Y' and abs(p.normal.z)>.7:v=co.x
   layer.data[li].uv=(u/3.72+.5,v/1.7+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=2;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
for sy in [-1,1]:
 cube('Timber / long backing',(0,sy*1.145,.83),(3.72,.19,1.46),wood)
 cube('Fibre panel / long',(0,sy*1.247,.83),(3.17,.025,1.12),fibre,bevel=.006)
for sx in [-1,1]:
 cube('Timber / side backing',(sx*1.745,0,.83),(.23,2.10,1.46),wood,axis='Y')
 cube('Fibre panel / side',(sx*1.868,0,.83),(.025,1.88,1.12),fibre,bevel=.006,axis='Y')
cube('Timber / clasp seat',(0,-1.28,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:
 cube('Forest seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.08),seam,bevel=.009)
for sx in [-1,1]:
 cube('Forest seam / side',(sx*1.74,0,1.618),(.16,2.05,.08),seam,bevel=.009)
 for sy in [-1,1]:
  cube('Timber / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
  cube('Timber / foot',(sx*1.47,sy*.91,-.07),(.48,.40,.34),wood,bevel=.045)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# Three continuous irregular ridge surfaces, closed below the lid top.
for k,(cx,cy,rx,ry,h) in enumerate([(-.77,-.03,.48,.57,.39),(.0,.13,.43,.63,.59),(.72,.04,.46,.60,.46)]):
 verts=[(cx,cy,1.965+h)];faces=[];rings=9;N=40
 for j in range(1,rings+1):
  r=j/rings
  for i in range(N):
   a=i*math.tau/N;rr=r*(1+.055*math.sin(5*a+k)+.035*math.cos(7*a))
   z=1.965+h*(1-r*r)**1.35 + .025*math.sin(a*3+k)*math.sin(math.pi*r)
   verts.append((cx+rx*rr*math.cos(a),cy+ry*rr*math.sin(a),z))
 for i in range(N):faces.append((0,1+i,1+(i+1)%N))
 for j in range(rings-1):
  for i in range(N):
   a=1+j*N+i;b=1+j*N+(i+1)%N;faces.append((a,a+N,b+N,b))
 faces.append(tuple(reversed([1+(rings-1)*N+i for i in range(N)])))
 me=bpy.data.meshes.new('Highland ridge');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Highland ridge / '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(greens[k]);parent(o)
 for f in me.polygons:f.use_smooth=True
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=1000;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'papua-new-guinea.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'papua-new-guinea.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('PAPUA NEW GUINEA AUTHORED')
