"""DR Congo Raffia & River. Original procedural art, not photogrammetry.
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
wood=mat('Raffia / ochre woven panels',(.4,.23,.10),.78);maptex(wood,'raffia-color.png','Base Color');maptex(wood,'raffia-roughness.png','Roughness',True)
tex=wood.node_tree.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(R/'maps'/'raffia-normal.png'));tex.image.colorspace_settings.name='Non-Color';tex.image.pack()
n=wood.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.3;wood.node_tree.links.new(tex.outputs['Color'],n.inputs['Color']);wood.node_tree.links.new(n.outputs['Normal'],wood.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
end=mat('Frame / satin umber',(.065,.032,.015),.43)
granite=mat('Earth / river banks',(.09,.07,.028),.92)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / dark inset',(.02,.027,.016),.9)
water=mat('River / blue green enamel',(.018,.21,.22),.21,.18)
leafm=[mat('Canopy / '+str(i),c,.85) for i,c in enumerate([(.025,.09,.04),(.045,.14,.055),(.075,.18,.065),(.12,.22,.085)])]
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
  o.data.materials.clear();o.data.materials.append(end if o.name.startswith('Interior') else gold)
for sy in [-1,1]:
 cube('Raffia / front' if sy<0 else 'Raffia / rear',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.018)
for sx in [-1,1]:
 cube('Raffia / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.018,axis='Y')
for sy in [-1,1]:
 for z in [.17,1.49]:cube('Frame / horizontal',(0,sy*1.25,z),(3.72,.045,.12),end,bevel=.01)
for sx in [-1,1]:
 for sy in [-1,1]:cube('Frame / upright',(sx*1.74,sy*1.25,.83),(.16,.045,1.4),end,bevel=.012)
cube('Frame / clasp seat',(0,-1.255,1.36),(.56,.075,.47),end,bevel=.025)
for sy in [-1,1]:
 cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Frame / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),end,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),end,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Foot / umber',(sx*1.47,sy*.91,-.08),(.4,.34,.25),end,bevel=.06)
def stone(n,loc,scale,p=None,material=granite,sub=2):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  k=1+random.uniform(-.11,.11);v.co=Vector((v.co.x*scale[0]*k,v.co.y*scale[1]*k,v.co.z*scale[2]*k))
 o.data.materials.append(material);uv(o)
 for face in o.data.polygons:face.use_smooth=True
 if p:parent(o,p)
 return o
# Continuous original winding river ribbon, inlaid on the lid; no source image.
verts=[];faces=[]
for i in range(65):
 x=-1.5+3*i/64;y=.23*math.sin(x*2.8)+.08*math.sin(x*5);w=.10+.018*math.cos(x*3)
 verts.extend([(x,y-w,1.997),(x,y+w,1.997)])
 if i:faces.append((2*i-2,2*i,2*i+1,2*i-1))
me=bpy.data.meshes.new('Continuous river ribbon');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('River / continuous channel',me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o)
# Broadleaf forest relief: low irregular crowns, with an open water corridor.
for side in [-1,1]:
 for i in range(9):
  x=-1.35+i*.33;y=.23*math.sin(x*2.8)+.08*math.sin(x*5)+side*(.59+random.uniform(-.03,.03))
  stone('Terrain / bank', (x,y,1.998),(.27,.25,.028),lid,leafm[0],2)
  stone('Canopy / crown', (x+random.uniform(-.04,.04),y,2.075+random.uniform(0,.03)),(.25,.21,.085+random.uniform(0,.025)),lid,leafm[i%4],2)
  for j in range(3):
   stone('Canopy / leaf cluster',(x+random.uniform(-.17,.17),y+random.uniform(-.12,.12),2.14+random.uniform(0,.035)),(.115,.095,.045),lid,leafm[(i+j)%4],1)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'dr-congo.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'dr-congo.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('DR CONGO AUTHORED')
