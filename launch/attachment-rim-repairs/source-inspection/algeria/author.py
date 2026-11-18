"""Algeria / Tassili Rock Forest. Procedurally authored, not a site replica.
Mechanical lineage: Japan trimmed mechanism; all new art is original geometry.
"""
import bpy, math, random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(179)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p=lid):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def tex(m,file,slot,noncolor=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file),check_existing=True)
 if noncolor:t.image.colorspace_settings.name='Non-Color'
 t.image.pack();m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[slot])
stone=mat('Sandstone / desert ochre',(.47,.22,.06),.8);tex(stone,'sandstone-color.png','Base Color');tex(stone,'sandstone-roughness.png','Roughness',True)
dark=mat('Sandstone / dark satin lid',(.11,.055,.025),.38);tex(dark,'dark-stone.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / umber',(.045,.027,.015),.9)
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone projection')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   if abs(p.normal.z)>.7:u,v=co.x,co.y
   elif abs(p.normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u/3.72+.5,v/2.38+.5)
def cube(n,loc,dim,material,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o)
 if bevel:
  m=o.modifiers.new('Soft stone edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(dark if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Continuous exterior behind erosion relief; original continuous interior retained.
for sy in [-1,1]:cube('Sandstone / body long',(0,sy*1.145,.83),(3.72,.19,1.46),stone,bevel=.035)
for sx in [-1,1]:cube('Sandstone / body side',(sx*1.745,0,.83),(.23,2.10,1.46),stone,bevel=.035)
cube('Sandstone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone,bevel=.025)
# Uneven vertical erosion relief, attached to the solid skins. Each closed tapered
# mesh varies in radius and leaning axis with height; not painted stripes.
def column(n,x,y,z,h,rx,ry,p=None,material=stone,seed=0):
 rng=random.Random(seed);sides=12;levels=9;verts=[];faces=[]
 tower=n.startswith('Tassili');angular=[rng.uniform(.80,1.18) for _ in range(sides)]
 for k in range(levels):
  t=k/(levels-1)
  # Broad angular buttresses taper to unequal fractured tops, never turned vases.
  shape=(1-.39*t+.055*math.sin(t*8+seed)) if tower else (.93+.07*math.sin(t*6+seed))
  for j in range(sides):
   a=j*math.tau/sides;w=angular[j]*(1+rng.uniform(-.025,.025))
   top=t*(1+(.075*math.sin(a*2+seed)+.035*math.cos(a*3)) if tower else 1)
   verts.append((x+rx*shape*w*math.cos(a)+rx*.21*t,y+ry*shape*w*math.sin(a)+ry*.12*math.sin(t*3+seed),z+h*top))
 for k in range(levels-1):
  for j in range(sides):a=k*sides+j;b=k*sides+(j+1)%sides;faces.append((a,b,b+sides,a+sides))
 faces.extend([tuple(reversed(range(sides))),tuple((levels-1)*sides+j for j in range(sides))])
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o)
 # Broad eroded flutes have smooth sides; weathered caps remain distinct.
 for f in me.polygons:f.use_smooth=len(f.vertices)==4
 if p:parent(o,p)
 return o
for sy in [-1,1]:
 for j in range(17):
  x=-1.67+j*.209
  if sy<0 and abs(x)<.38:continue
  column('Erosion / long flute',x,sy*1.211,.13,1.38,.105,.065,seed=j+int(sy+1)*27)
for sx in [-1,1]:
 for j in range(10):column('Erosion / side flute',sx*1.827,-.96+j*.213,.13,1.38,.055,.107,seed=j+70)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.608),(3.28,.16 if sy<0 else .08,.088),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.608),(.16,2.05,.088),seam,bevel=.009)
 for sy in [-1,1]:cube('Sandstone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),dark,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Sandstone / foot',(sx*1.47,sy*.91,-.09),(.55,.46,.35),dark,bevel=.09)
# Irregular low apron and 7 spaced but compositionally grouped rock towers.
bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=12,radius=1,location=(0,.10,1.995));o=bpy.context.object;o.name='Terrain / sand apron'
for v in o.data.vertices:
 a=math.atan2(v.co.y,v.co.x);w=1+.07*math.sin(a*5)+.04*math.cos(a*9);v.co=Vector((v.co.x*1.43*w,v.co.y*.72*w,v.co.z*.065))
o.data.materials.append(stone);uv(o);parent(o)
for i,(x,y,h,rx,ry) in enumerate([(-1.05,.30,.48,.19,.17),(-.62,.50,.63,.21,.18),(-.15,.52,.46,.17,.16),(.37,.51,.70,.23,.18),(.93,.42,.61,.21,.18),(-.50,-.15,.31,.18,.16),(.28,-.16,.39,.22,.18)]):
 column('Tassili / tower %02d'%i,x,y,2.015,h,rx,ry,lid,seed=179+i)
def disk(n,loc,r,depth,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold);m=o.modifiers.new('Rounded brass','BEVEL');m.width=.005;m.segments=3;select(o);bpy.ops.object.modifier_apply(modifier=m.name);return o
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035)
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(0,-1.282,.87),major_radius=.107,minor_radius=.008,rotation=(math.pi/2,0,0));bpy.context.object.name='Medallion / raised rim';bpy.context.object.data.materials.append(gold)
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=48,minor_segments=10,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,4.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'algeria.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'algeria.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('ALGERIA AUTHORED')
