"""Brief-led UK pilot. Authored mesh and maps; no photogrammetry.
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
wood=mat('Slate / blue charcoal cleavage',(.18,.20,.25),.68);maptex(wood,'slate-color.png','Base Color');maptex(wood,'slate-roughness.png','Roughness',True)
granite=mat('Wall stone / weathered grey',(.31,.33,.29),.88);maptex(granite,'wall-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / dark green',(.035,.07,.032),.9)
fields=[mat('Meadow / '+str(i),c,.93) for i,c in enumerate([(.12,.21,.055),(.17,.25,.075),(.095,.17,.04),(.20,.28,.085)])]
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
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=1;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Staggered slate joints; continuous inherited liner remains behind them.
for row in range(6):
 z=.10+(row+.5)*1.46/6;h=1.46/6-.012
 for sy in [-1,1]:
  edges=[-1.86]+[x for x in [-1.86+.45*(row%2)+j*.62 for j in range(1,7)] if -1.85<x<1.85]+[1.86]
  for a,b in zip(edges,edges[1:]):cube('Slate / front' if sy<0 else 'Slate / rear',((a+b)/2,sy*1.145,z),(b-a-.012,.19,h),wood,bevel=.009)
 for sx in [-1,1]:
  edges=[-1.04]+[x for x in [-1.04+.20*(row%2)+j*.53 for j in range(1,5)] if -1.03<x<1.03]+[1.04]
  for a,b in zip(edges,edges[1:]):cube('Slate / side',(sx*1.745,(a+b)/2,z),(.23,b-a-.012,h),wood,bevel=.009)
cube('Slate / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Slate / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
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
def height(x,y):
 return 2.005+.28*math.exp(-((x-.65)**2/.55+(y-.32)**2/.45))+.13*math.exp(-((x+.8)**2/.3+(y+.2)**2/.6))
verts=[];faces=[];nx=40;ny=24
for j in range(ny+1):
 for i in range(nx+1):
  x=-1.45+2.9*i/nx;y=-.85+1.7*j/ny;verts.append((x,y,height(x,y)))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
me=bpy.data.meshes.new('Rolling meadow grid');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / walled meadows',me);bpy.context.collection.objects.link(o);parent(o)
for m in fields:me.materials.append(m)
for f in me.polygons:
 c=f.center;f.material_index=(int(c.x>-.2)+2*int(c.y>.08));f.use_smooth=True
# Exposed terrain edge connects relief down into slab.
boundary=[verts[i] for i in range(nx+1)]+[verts[j*(nx+1)+nx] for j in range(1,ny+1)]+[verts[ny*(nx+1)+i] for i in range(nx-1,-1,-1)]+[verts[j*(nx+1)] for j in range(ny-1,0,-1)]
v=[];f=[]
for p in boundary:v.extend([p,(p[0],p[1],1.975)])
for i in range(len(boundary)):a=2*i;b=2*((i+1)%len(boundary));f.append((a,b,b+1,a+1))
me=bpy.data.meshes.new('Terrain edge');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new('Terrain / slate edge',me);bpy.context.collection.objects.link(o);me.materials.append(wood);uv(o);parent(o)
for axis,count in [('X',22),('Y',12)]:
 for i in range(count):
  x=-1.37+i*2.74/(count-1) if axis=='X' else -.2
  y=.08 if axis=='X' else -.77+i*1.54/(count-1)
  if axis=='Y' and abs(y-.08)<.13:continue
  z=height(x,y)
  for row in range(2):cube('Field wall / course',(x,y,z+.035+row*.055),(.12,.075,.065) if axis=='X' else (.075,.12,.065),granite,lid,.008)
  cube('Field wall / upright coping',(x,y,z+.155),(.075,.085,.11) if axis=='X' else (.085,.075,.11),granite,lid,.009)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'united-kingdom.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'united-kingdom.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('UNITED KINGDOM AUTHORED')
