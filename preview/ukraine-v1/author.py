"""Brief-led Ukraine Petrykivka Bloom pilot. Authored mesh and maps; no photogrammetry.
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
wood=mat('Lacquer / floral painted wood',(.025,.035,.025),.34);maptex(wood,'floral-color.png','Base Color');maptex(wood,'lacquer-roughness.png','Roughness',True)
plain=mat('Lacquer / deep green wood',(.015,.025,.018),.32);maptex(plain,'wood-color.png','Base Color');maptex(plain,'lacquer-roughness.png','Roughness',True)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / dark green',(.012,.02,.012),.85)
red=mat('Bloom / vermilion',(.65,.035,.018),.36)
coral=mat('Bloom / coral',(.85,.12,.045),.4)
ochre=mat('Bloom / ochre heart',(.85,.43,.035),.35)
green=mat('Leaf / forest',(.055,.24,.08),.4)
lightgreen=mat('Leaf / young green',(.16,.36,.08),.4)
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
  o.data.materials.clear();o.data.materials.append(plain if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
def panel_uv(o):
 o.data.materials.append(plain)
 layer=o.data.uv_layers.active
 for f in o.data.polygons:
  mainface=abs(f.normal.x)>.95 if 'side' in o.name else abs(f.normal.y)>.95
  if not mainface:f.material_index=1
  for li in f.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   u=co.x/o.dimensions.x+.5 if abs(f.normal.y)>.5 else co.y/o.dimensions.y+.5
   layer.data[li].uv=(u,co.z/o.dimensions.z+.5)
for sy in [-1,1]:
 o=cube('Painted body / front' if sy<0 else 'Painted body / rear',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.012);panel_uv(o)
for sx in [-1,1]:
 o=cube('Painted body / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.012);panel_uv(o)
cube('Lacquer / clasp seat',(0,-1.255,1.36),(.56,.075,.47),plain,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Lacquer / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),plain,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),plain,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Lacquer foot',(sx*1.47,sy*.91,-.10),(.52,.43,.32),plain,bevel=.055)
def tube(n,points,radii,material,p=lid,sides=9):
 verts=[];faces=[]
 for i,c in enumerate(points):
  c=Vector(c);t=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)]);t.normalize();a=t.cross(Vector((0,1,0)))
  if a.length<.01:a=t.cross(Vector((1,0,0)))
  a.normalize();b=t.cross(a).normalized()
  for j in range(sides):verts.append(c+radii[i]*(a*math.cos(j*math.tau/sides)+b*math.sin(j*math.tau/sides)))
 for i in range(len(points)-1):
  for j in range(sides):a=i*sides+j;bb=i*sides+(j+1)%sides;faces.append((a,bb,bb+sides,a+sides))
 faces.extend([tuple(reversed(range(sides))),tuple((len(points)-1)*sides+j for j in range(sides))]);me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material)
 for f in me.polygons:f.use_smooth=True
 if p:parent(o,p)
 return o
# Five original fantastic flowers: low, physically raised lacquer relief.
flowers=[(-1.05,-.33,.27,red),(-.60,.48,.23,coral),(.0,-.05,.33,red),(.68,.48,.26,red),(1.05,-.38,.24,coral)]
def ellipsoid(n,loc,sc,material,angle=0):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:v.co=Vector((v.co.x*sc[0],v.co.y*sc[1],v.co.z*sc[2]))
 o.rotation_euler.z=angle;o.data.materials.append(material)
 for f in o.data.polygons:f.use_smooth=True
 parent(o);return o
for i,(x,y,r,material) in enumerate(flowers):
 for j in range(11):
  a=j*math.tau/11
  ellipsoid('Bloom %d / petal %02d'%(i,j),(x+math.cos(a)*r*.57,y+math.sin(a)*r*.57,2.035),(r*.53,r*.20,.045),material,a)
 ellipsoid('Bloom %d / ochre heart'%i,(x,y,2.065),(r*.26,r*.26,.05),ochre)
 for j in range(9):
  a=j*math.tau/9;ellipsoid('Bloom %d / seed'%i,(x+math.cos(a)*r*.16,y+math.sin(a)*r*.16,2.11),(.012,.012,.012),gold)
# Curved central branch connects every flower at its base.
for i,(x,y,r,material) in enumerate(flowers):
 pts=[(-1.35,-.72,1.998),(-.65,-.50,2.004),(x*.6,-.30,2.006),(x,y,2.006)]
 tube('Floral stem / %d'%i,pts,[.014,.019,.018,.013],green,sides=7)
for i,(x,y,a) in enumerate([(-1.25,.15,2.3),(-.90,.12,1.0),(-.3,.56,.8),(-.35,-.52,-.8),(.35,-.49,-.6),(.38,.48,2.0),(.95,.12,.5),(1.30,.18,1.0)]):
 # Closed tapered leaf mesh, not a floating flat image.
 verts=[(0,0,0),(.15,.075,.025),(.35,0,0),(.15,-.075,.025),(.16,0,.05),(.16,0,-.008)]
 faces=[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(1,0,5),(2,1,5),(3,2,5),(0,3,5)]
 me=bpy.data.meshes.new('Tapered leaf');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Floral leaf / %d'%i,me);bpy.context.collection.objects.link(o);o.location=(x,y,2.005);o.rotation_euler.z=a;me.materials.append(green if i%2 else lightgreen);parent(o)
 # Connect each leaf root to the closest point on an existing flower stem.
 candidates=[]
 for fx,fy,fr,fm in flowers:
  path=[Vector(v) for v in [(-1.35,-.72,1.998),(-.65,-.50,2.004),(fx*.6,-.30,2.006),(fx,fy,2.006)]]
  for aa,bb in zip(path,path[1:]):
   t=max(0,min(1,(Vector((x,y,2.006))-aa).dot(bb-aa)/(bb-aa).length_squared));candidates.append(aa.lerp(bb,t))
 root=min(candidates,key=lambda v:(v-Vector((x,y,2.006))).length)
 tube('Leaf branch / %d'%i,[root,root.lerp(Vector((x,y,2.006)),.5),Vector((x,y,2.006))],[.009,.009,.008],green,sides=6)
 tube('Leaf vein / %d'%i,[(x,y,2.02),(x+.15*math.cos(a),y+.15*math.sin(a),2.06),(x+.32*math.cos(a),y+.32*math.sin(a),2.02)],[.006,.006,.003],ochre,sides=6)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.use_compositing=False;scene.render.resolution_x=900;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'ukraine.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'ukraine.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('UKRAINE AUTHORED')
