"""Laos Bamboo & Karst pilot. Authored mesh and maps; no photogrammetry.
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
wood=mat('Bamboo / woven honey panels',(.4,.25,.10),.5);maptex(wood,'bamboo-color.png','Base Color');maptex(wood,'bamboo-roughness.png','Roughness',True)
t=wood.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/bamboo-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();normal=wood.node_tree.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.45;wood.node_tree.links.new(t.outputs['Color'],normal.inputs['Color']);wood.node_tree.links.new(normal.outputs['Normal'],wood.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
end=mat('Bamboo / dark binding',(.21,.075,.028),.47);maptex(end,'bamboo-frame.png','Base Color')
# Actual end-grain differs in UV frequency and tint via a separate compact map.
granite=mat('Limestone / weathered ivory',(.24,.25,.25),.85);maptex(granite,'limestone.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
bark=mat('Bamboo / furrowed bark',(.19,.075,.031),.85)
moss=mat('Moss / muted cushions',(.095,.16,.035),.95)
seam=mat('Mineral seam / moss green',(.035,.07,.032),.9)
leafm=[mat('Cedar foliage / '+str(i),c,.92) for i,c in enumerate([(.045,.10,.024),(.07,.14,.035),(.10,.18,.047),(.13,.21,.06)])]
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
  if o.name.startswith('Interior'):uv(o,'Y' if 'end' in o.name else 'X')
# Woven panel faces surrounded by real dark frame rails.
for sy in [-1,1]:
 cube('Bamboo / woven front' if sy<0 else 'Bamboo / woven rear',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.025)
 for z in [.16,1.49]:cube('Bamboo frame / horizontal',(0,sy*1.246,z),(3.70,.035,.115),end,bevel=.009)
for sx in [-1,1]:
 cube('Bamboo / woven side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.025,axis='Y')
 for z in [.16,1.49]:cube('Bamboo frame / side',(sx*1.872,0,z),(.035,2.36,.115),end,bevel=.009,axis='Y')
 for sy in [-1,1]:cube('Bamboo frame / upright',(sx*1.745,sy*1.247,.83),(.17,.038,1.46),end,bevel=.009)
# Small collar fills the central clasp mounting behind its retained position.
cube('Bamboo / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:
 cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.090),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.090),seam,bevel=.009)
 for sy in [-1,1]:cube('Bamboo / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
# A thin satin upper facing with an independently oriented grain field.
for sx in [-1,1]:
 for j in range(6):cube('Lid finger / end',(sx*1.858,-.98+j*.39,1.83),(.012,.16,.23),end,lid,.003,axis='Y')
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
 for sy in [-1,1]:stone('Limestone foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)
# Asymmetric layered karst towers: coarse silhouette with uneven flutes.
for k,(cx,cy,rx,ry,height) in enumerate([(-.78,.48,.36,.28,.58),(-.02,.67,.33,.26,.80),(.64,.48,.30,.25,.43)]):
 verts=[];faces=[];sides=13;rings=7
 for j in range(rings):
  z=1.97+height*j/(rings-1);factor=[1,.93,.84,.79,.66,.48,.17][j]
  for i in range(sides):
   ang=math.tau*i/sides;rough=1+.15*math.sin(i*2.4+k)+random.uniform(-.07,.07)
   verts.append((cx+rx*factor*rough*math.cos(ang)+.055*j/(rings-1),cy+ry*factor*rough*math.sin(ang),z+(.025*math.sin(i*1.7+k) if j else 0)))
 for j in range(rings-1):
  for i in range(sides):
   q=j*sides+i;n=j*sides+(i+1)%sides;faces.append((q,n,n+sides,q+sides))
 faces.extend([tuple(reversed(range(sides))),tuple((rings-1)*sides+i for i in range(sides))])
 me=bpy.data.meshes.new('Karst stratified mesh');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Karst / peak '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(granite);uv(o);parent(o)
 for j in range(9):
  ang=j*2.4;stone('Vegetation / karst foothill',(cx+rx*.83*math.cos(ang),cy+ry*.83*math.sin(ang),2.015),(.10,.075,.045),lid,moss,1)
jade=mat('River / muted jade',(.055,.24,.19),.25,.1)
# A continuous low curved river strip, not independent blue fragments.
verts=[];faces=[]
for i in range(45):
 x=-1.45+2.9*i/44;y=-.39+.17*math.sin(x*2.4)
 for side in [-1,1]:verts.append((x,y+side*.065,1.987))
 if i:faces.append((2*i-2,2*i-1,2*i+1,2*i))
me=bpy.data.meshes.new('River strip');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('River / Nam Song inspired inlay',me);bpy.context.collection.objects.link(o);me.materials.append(jade);parent(o)
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
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'laos.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'laos.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('LAOS AUTHORED')
