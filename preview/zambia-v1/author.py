"""Brief-led Zambia basalt-gorge pilot. Authored mesh/maps; no photogrammetry.
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

wood=mat('Basalt / river-cut dark stone',(.035,.045,.039),.8);maptex(wood,'basalt-color.png','Base Color');maptex(wood,'basalt-roughness.png','Roughness',True)
t=wood.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/basalt-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=wood.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.22;wood.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);wood.node_tree.links.new(n.outputs['Normal'],wood.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
granite=wood
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / olive',(.035,.055,.025),.9)
water=mat('Zambezi / blue green water',(.025,.24,.28),.22,.12)
foam=mat('Falls / ivory aerated water',(.72,.86,.81),.45)
bank=mat('Riverbank / muted olive',(.08,.12,.033),.94)
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
for sy in [-1,1]:cube('Basalt / front' if sy<0 else 'Basalt / rear',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.04)
for sx in [-1,1]:cube('Basalt / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.035,axis='Y')
cube('Basalt / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.09),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.09),seam,bevel=.009)
 for sy in [-1,1]:cube('Basalt / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
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
 for sy in [-1,1]:stone('Granite foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)

# Shaped gorge banks. Upper river flows from rear toward a broad drop at y=-.12.
# Each bank is a faceted closed volume with irregular crest, not a display plinth.
for side in [-1,1]:
 verts=[];N=19
 for i in range(N):
  y=-.86+i*1.67/(N-1);inner=.44+.075*math.sin(y*7);outer=1.48+.06*math.cos(i*1.7);height=2.13 if y<-.16 else 2.46+.06*math.sin(i*1.5+side)
  verts.extend([(side*inner,y,1.96),(side*outer,y,1.96),(side*outer,y,height-.035),(side*inner,y,height)])
 faces=[]
 for i in range(N-1):
  for j in range(4):a=i*4+j;b=i*4+(j+1)%4;faces.append((a,b,b+4,a+4))
 faces += [(3,2,1,0),tuple((N-1)*4+j for j in range(4))]
 me=bpy.data.meshes.new('Gorge bank');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Gorge / basalt bank '+str(side),me);bpy.context.collection.objects.link(o);o.data.materials.append(wood);uv(o);parent(o)
# Solid stone beds beneath water remove the unsupported front-sheet appearance.
cube('Gorge / lower channel bed',(0,-.51,2.005),(.90,.70,.07),wood,lid,.014)
cube('Gorge / upper channel bed',(0,.33,2.19),(.90,.91,.48),wood,lid,.02)
# Water profile: connected upstream river -> vertical falls -> lower plunge channel.
verts=[];faces=[]
profile=[(.78,2.44),(.51,2.44),(.23,2.44),(-.10,2.44),(-.14,2.41),(-.18,2.07),(-.30,2.05),(-.55,2.04),(-.83,2.04)]
for i,(y,z) in enumerate(profile):
 for j in range(13):
  x=(j/12-.5)*.85;verts.append((x,y,z+.007*math.sin(j*2+i)))
for i in range(len(profile)-1):
 for j in range(12):a=i*13+j;faces.append((a,a+1,a+14,a+13))
me=bpy.data.meshes.new('Connected river and waterfall');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Zambezi / continuous river and falls',me);bpy.context.collection.objects.link(o);me.materials.append(water);me.materials.append(foam)
for p in me.polygons:
 if 36<=p.index<72:p.material_index=1
parent(o)
# Foam streaks / bank vegetation: compact irregular accents, never sky mist spheres.
for i in range(11):
 x=-.38+i*.076
 cube('Falls / foam streak',(x,-.166,2.255),(.014,.014,.29),foam,lid,.004)
for i in range(24):
 side=-1 if i%2 else 1;y=.06+(i//2)*.061;x=side*(.66+.15*math.sin(i*1.7));z=2.47+.06*math.sin(((y+.86)/1.67*18)*1.5+side)
 stone('Gorge / olive bank accent',(x,y,z),(.11,.075,.025),lid,bank,1)
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
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'zambia.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'zambia.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('ZAMBIA AUTHORED')
