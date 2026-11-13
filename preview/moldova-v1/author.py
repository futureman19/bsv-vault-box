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
wood=mat('Walnut / warm rim',(.18,.08,.035),.48);maptex(wood,'walnut-color.png','Base Color')
weave=mat('Woven / charcoal burgundy',(.12,.05,.04),.85);maptex(weave,'weave-color.png','Base Color');maptex(weave,'weave-roughness.png','Roughness',True)
t=weave.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/weave-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=weave.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.25;weave.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);weave.node_tree.links.new(n.outputs['Normal'],weave.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / antique',(.48,.30,.10),.28,.8)
seam=mat('Seam / charcoal',(.022,.018,.014),.92)
red=mat('Petals / burgundy',(.24,.035,.06),.8)
ivory=mat('Petals / ivory',(.65,.50,.29),.8)
green=mat('Leaves / muted green',(.12,.18,.065),.85)
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z
   if axis=='Y' and abs(p.normal.z)>.7:v=co.x
   layer.data[li].uv=(u/3.72+.5,v/1.7+.5)
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
# Four recessed woven panels with explicit panel-local UVs.
def panel(n,loc,dim,axis,p=None):
 o=cube(n,loc,dim,weave,p,bevel=.006)
 for poly in o.data.polygons:
  for li in poly.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   u=co.x/dim[0]+.5 if axis!='Y' else co.y/dim[1]+.5
   v=co.y/dim[1]+.5 if axis=='TOP' else co.z/dim[2]+.5
   o.data.uv_layers.active.data[li].uv=(u,v)
 return o
for sy in [-1,1]:
 cube('Walnut / wall',(0,sy*1.145,.83),(3.72,.19,1.46),wood)
 panel('Woven / wall',(0,sy*1.246,.83),(3.20,.012,1.10),'X')
for sx in [-1,1]:
 cube('Walnut / end',(sx*1.745,0,.83),(.23,2.10,1.46),wood,axis='Y')
 panel('Woven / end',(sx*1.866,0,.83),(.012,1.86,1.10),'Y')
 for sy in [-1,1]:cube('Walnut / corner',(sx*1.745,sy*1.145,.83),(.23,.19,1.46),wood)
cube('Walnut / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.08),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.08),seam,bevel=.009)
 for sy in [-1,1]:cube('Walnut / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
panel('Woven / lid',(0,0,1.986),(3.28,1.94,.016),'TOP',lid)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Walnut / foot',(sx*1.47,sy*.91,-.10),(.50,.42,.32),wood,bevel=.045)
# Raised eight-petal angular flowers, contemporary invention, not a copied textile.
def diamond(n,cx,cy,rx,ry,z,material,angle=0):
 pts=[(-rx,0),(0,-ry),(rx,0),(0,ry)];v=[]
 for zz in [z,z+.026]:
  for x,y in pts:v.append((cx+x*math.cos(angle)-y*math.sin(angle),cy+x*math.sin(angle)+y*math.cos(angle),zz))
 faces=[(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
 me=bpy.data.meshes.new(n);me.from_pydata(v,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);parent(o);return o
for i,cx in enumerate([-.96,0,.96]):
 for j in range(8):
  a=j*math.tau/8;diamond('Flower %d / petal %d'%(i,j),cx+.225*math.cos(a),.225*math.sin(a),.155,.075,2.012,red if j%2==0 else ivory,a)
 diamond('Flower %d / heart'%i,cx,0,.08,.08,2.020,gold)
 for sy in [-1,1]:
  diamond('Flower %d / leaf'%i,cx,sy*.55,.16,.075,2.008,green,.4*sy)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=1000;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'moldova.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'moldova.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('MOLDOVA AUTHORED')
