"""Brief-led Zimbabwe pilot. Authored mesh and maps; no photogrammetry.
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
stone_mat=mat('Granite / warm mineral grain',(.34,.29,.22),.8);maptex(stone_mat,'granite-color.png','Base Color');maptex(stone_mat,'granite-roughness.png','Roughness',True)
liner=mat('Interior / dark granite',(.12,.105,.08),.8);maptex(liner,'liner-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / charcoal olive',(.045,.05,.03),.9)
earth=mat('Ground / dry ochre',(.24,.15,.06),.95)
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone projection')
 for p in o.data.polygons:
  normal=p.normal
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   a,b=(co.x,co.y) if abs(normal.z)>.7 else ((co.y,co.z) if abs(normal.x)>.7 else (co.x,co.z))
   layer.data[li].uv=(a*.8+.5,b*.8+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=1;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(liner if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Staggered individual stone blocks, with epsilon-clipped edge partitions.
for row in range(8):
 z=.10+(row+.5)*1.46/8;h=1.46/8-.012
 for sy in [-1,1]:
  cuts=sorted(set([-1.86,1.86]+[round(-1.86+j*.465+(row%2)*.2325,5) for j in range(9) if -1.86+1e-5 < -1.86+j*.465+(row%2)*.2325 < 1.86-1e-5]))
  for a,b in zip(cuts,cuts[1:]):cube('Masonry / front rear block',((a+b)/2,sy*1.145,z),(b-a-.012,.19,h),stone_mat,bevel=.008)
 for sx in [-1,1]:
  cuts=sorted(set([-1.044,1.044]+[round(-1.044+j*.4176+(row%2)*.2088,5) for j in range(6) if -1.044+1e-5 < -1.044+j*.4176+(row%2)*.2088 < 1.044-1e-5]))
  for a,b in zip(cuts,cuts[1:]):cube('Masonry / side block',(sx*1.745,(a+b)/2,z),(.23,b-a-.012,h),stone_mat,bevel=.008)
cube('Granite / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone_mat,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Granite / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone_mat,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone_mat,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def rock(n,loc,scale,p=None,material=stone_mat):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  x,y,z=v.co;k=1+.035*math.sin(3*x+2*y)+.025*math.cos(4*z-y)
  v.co=Vector((x*scale[0]*k,y*scale[1]*k,z*scale[2]))
 o.data.materials.append(material);uv(o)
 for f in o.data.polygons:f.use_smooth=True
 if p:parent(o,p)
 return o
for sx in [-1,1]:
 for sy in [-1,1]:rock('Granite foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19))
rock('Terrain / ochre plinth',(0,.10,1.98),(1.20,.79,.075),lid,earth)
rock('Kopje / basal boulder',(.22,.20,2.19),(.70,.49,.25),lid)
rock('Kopje / middle boulder',(.15,.18,2.54),(.51,.38,.24),lid)
rock('Kopje / crown boulder',(.24,.20,2.86),(.61,.36,.20),lid)
rock('Kopje / companion',(-.72,-.18,2.17),(.35,.28,.20),lid)
 # Solid family emblem, not a traditional symbol.
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'zimbabwe.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'zimbabwe.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('ZIMBABWE AUTHORED')
