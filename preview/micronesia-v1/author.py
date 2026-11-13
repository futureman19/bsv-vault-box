"""Reference-led Japan pilot. Authored mesh and maps; no photogrammetry.
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
wood=mat('Basalt / mineral grain',(.08,.12,.13),.7);maptex(wood,'basalt-color.png','Base Color');maptex(wood,'basalt-roughness.png','Roughness',True)
end=wood
granite=mat('Pale stone / coral limestone inspired',(.48,.52,.45),.82);maptex(granite,'pale-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / muted teal',(.025,.09,.08),.8)
water=mat('Tidal channels / teal inlay',(.018,.25,.24),.24,.12)
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   n=p.normal
   if abs(n.z)>.7:u,v=co.x,co.y
   elif abs(n.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u/1.6+.5,v/1.6+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=1;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o,'Y' if 'end' in o.name else 'X')
# Real stone courses with staggered vertical joints, continuous liner behind.
for row in range(7):
 z=.10+(row+.5)*1.46/7;h=1.46/7-.009
 for sy in [-1,1]:
  cuts=[-1.86]+[x for x in [-1.2+(.30 if row%2 else 0),-.35+(.30 if row%2 else 0),.55+(.30 if row%2 else 0),1.32+(.18 if row%2 else 0)] if x<1.86]+[1.86]
  for j,(lo,hi) in enumerate(zip(cuts,cuts[1:])):cube('Basalt course / long %s %s %s'%(row,sy,j),((lo+hi)/2,sy*1.145,z),(hi-lo-.012,.19,h),wood,bevel=.015)
 for sx in [-1,1]:
  for j in range(3):cube('Basalt course / end %s %s %s'%(row,sx,j),(sx*1.745,-.69+j*.69,z),(.23,.678,h),wood,bevel=.015)
# Small collar fills the central clasp mounting behind its retained position.
cube('Basalt / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:
 cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Basalt / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
# Restrained brass corner protectors replace the Iceland wraps entirely.
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
 for sy in [-1,1]:stone('Stone foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)
# Abstract constructed islets separated by a continuous connected water inlay.
cube('Lagoon / connected tidal inlay',(0,0,1.993),(3.18,1.82,.032),water,lid,.025)
platforms=[(-1.04,-.48,.72,.48),(-.08,-.48,.70,.48),(.94,-.48,.76,.48),(-1.02,.37,.76,.64),(.03,.39,.78,.66),(1.04,.39,.67,.60)]
for i,(x,y,w,d) in enumerate(platforms):
 cube('Islet / platform %02d'%i,(x,y,2.035),(w,d,.09),granite,lid,.035)
 # Small cut-stone edging adds genuine depth, not a copied map.
 for j in range(3):cube('Islet / edge %02d %02d'%(i,j),(x-w*.30+j*w*.30,y-d*.40,2.095),(w*.26,.055,.07),wood,lid,.009)
# A low OPEN enclosure evokes header/stretcher stonework, no funerary content.
x,y=-1.02,.37
for k in range(3):
 z=2.13+k*.095
 for sy in [-1,1]:cube('Basalt enclosure / long %s %s'%(k,sy),(x,y+sy*.205,z),(.64,.095,.082),wood,lid,.012)
 for sx in [-1,1]:cube('Basalt enclosure / end %s %s'%(k,sx),(x+sx*.27,y,z),(.095,.31,.082),wood,lid,.012)
# Smaller paired stone prisms on the far-right platform.
for j in range(3):cube('Basalt relief / prism '+str(j),(1.04,.21+j*.16,2.13),(.49,.10,.09),wood,lid,.012)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'micronesia.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'micronesia.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('MICRONESIA AUTHORED')
