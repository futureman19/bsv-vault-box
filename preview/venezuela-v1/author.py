"""Brief-led Venezuela pilot. Authored mesh and maps; no photogrammetry.
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
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
stone_mat=mat('Sandstone / weathered strata',(.4,.18,.10),.82)
maptex(stone_mat,'stone-color.png','Base Color');maptex(stone_mat,'stone-roughness.png','Roughness',True)
cap=mat('Summit / olive vegetation',(.10,.16,.055),.92);maptex(cap,'summit.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Weathered dark seam',(.045,.035,.025),.92)
water=mat('Cascade / pale mineral water',(.58,.78,.79),.22)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone_mat if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Sandstone / wall',(0,sy*1.145,.83),(3.72,.19,1.46),stone_mat,bevel=.016)
for sx in [-1,1]:cube('Sandstone / side',(sx*1.745,0,.83),(.23,2.10,1.46),stone_mat,bevel=.016)
cube('Sandstone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone_mat,bevel=.025)
for sy in [-1,1]:cube('Weathered seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Weathered seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Sandstone / rim',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone_mat,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone_mat,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Stone foot',(sx*1.47,sy*.91,-.10),(.55,.46,.35),stone_mat,bevel=.09)
# Irregular flat-topped cliff: disconnected strata are not used; one closed solid.
outline=[(-.95,-.40),(-.55,-.52),(-.12,-.50),(.25,-.42),(.77,-.38),(.91,-.05),(.79,.52),(.34,.64),(-.25,.59),(-.82,.42),(-1.01,.08)]
verts=[];faces=[];N=len(outline)
for z,scale in [(1.97,1.05),(2.15,1.0),(2.48,.98),(2.82,.93)]:
 for x,y in outline:verts.append((x*scale+.15,y*scale+.15,z))
faces.append(tuple(reversed(range(N))))
for k in range(3):
 for j in range(N):faces.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
faces.append(tuple(3*N+j for j in range(N)))
me=bpy.data.meshes.new('Tepui cliff');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Tepui / sandstone massif',me);bpy.context.collection.objects.link(o);me.materials.append(stone_mat);uv(o);parent(o)
# Thin summit polygon cap, inset to preserve bare cliff edge.
v=[(x*.88+.15,y*.88+.15,2.824) for x,y in outline];me=bpy.data.meshes.new('Summit');me.from_pydata(v,[],[tuple(range(N))]);me.update();o=bpy.data.objects.new('Tepui / summit vegetation',me);bpy.context.collection.objects.link(o);me.materials.append(cap);uv(o);parent(o)
# Continuous narrow water ribbon from summit over front cliff into a lid basin.
points=[(-.12,-.12,2.838),(-.12,-.30,2.838),(-.12,-.355,2.81),(-.12,-.38,2.50),(-.12,-.40,2.17),(-.12,-.48,2.015),(-.12,-.72,2.015)]
v=[]
for x,y,z in points:v.extend([(x-.027,y,z),(x+.027,y,z)])
f=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(points)-1)];me=bpy.data.meshes.new('Cascade');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new('Tepui / continuous cascade',me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o)
bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=12,radius=1,location=(-.12,-.73,2.003));o=bpy.context.object;o.name='Tepui / basin';o.scale=(.25,.18,.025);select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(water);parent(o)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'venezuela.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'venezuela.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('VENEZUELA AUTHORED')
