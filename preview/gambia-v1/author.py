"""Brief-led Gambia pilot. Authored mesh and maps; no photogrammetry.
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
wood=mat('Sediment bronze / tidal traces',(.32,.19,.075),.57,.22);maptex(wood,'sediment-color.png','Base Color');maptex(wood,'sediment-roughness.png','Roughness',True)
granite=mat('Silt / ochre banks',(.26,.19,.09),.88);maptex(granite,'silt-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
bark=mat('Mangrove / umber bark',(.12,.075,.035),.87)
seam=mat('Tidal seam / deep green',(.025,.045,.03),.8)
water=mat('Estuary / blue green enamel',(.022,.24,.27),.2,.25)
leafm=[mat('Mangrove foliage / '+str(i),c,.85) for i,c in enumerate([(.035,.095,.03),(.065,.16,.045),(.10,.20,.065)])]
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
for sy in [-1,1]:cube('Sediment / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.025)
for sx in [-1,1]:cube('Sediment / end wall',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.025,axis='Y')
cube('Sediment / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Tidal seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.096),seam,bevel=.009)
for sx in [-1,1]:
 cube('Tidal seam / side',(sx*1.74,0,1.618),(.16,2.05,.096),seam,bevel=.009)
 for sy in [-1,1]:cube('Sediment / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
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
for sx in [-1,1]:
 for sy in [-1,1]:stone('Sediment foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
# A continuous enamel estuary inset; banks follow both sides of its actual mesh.
def ribbon(n,points,width,z):
 verts=[]
 for i,(x,y) in enumerate(points):
  d=Vector((*points[min(i+1,len(points)-1)],0))-Vector((*points[max(i-1,0)],0));d.normalize();w=Vector((-d.y,d.x,0))*width/2
  verts.extend([(x+w.x,y+w.y,z),(x-w.x,y-w.y,z)])
 faces=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(points)-1)]
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o);return o
points=[(-1.62+i*3.24/48,.22*math.sin(i/48*math.tau*1.15)-.12) for i in range(49)]
ribbon('Estuary / main channel',points,.31,1.997)
ribbon('Estuary / tributary',[(.38,-.27),(.48,-.43),(.64,-.56),(.72,-.79),(.87,-.94)],.11,1.999)
for side in [-1,1]:
 for i in range(16):
  x=-1.5+i*.20;y=.22*math.sin((x+1.62)/3.24*math.tau*1.15)-.12+side*.29
  if side<0 and .3<x<1:continue
  stone('Bank / sediment',(x,y,2.015),(.19,.12,.035),lid,granite,2)
# Three distinct mangroves with curved aerial prop roots and spreading broad leaves.
vs=[[] for _ in leafm];fs=[[] for _ in leafm]
for ti,(x,y,h) in enumerate([(.68,.64,.64),(1.17,.53,.51),(.15,.61,.48)]):
 base=2.015
 stone('Bank / mangrove island',(x,y,base),(.29,.23,.04),lid,granite,2)
 trunk=[(x,y,base),(x-.025,y,base+.19),(x+.025,y+.02,base+h*.75),(x+.04,y+.02,base+h)]
 tube('Mangrove / trunk',trunk,[.043,.035,.023,.011],bark)
 for j in range(5):
  ang=j*math.tau/5+.3*ti
  tube('Mangrove / prop root',[(x+math.cos(ang)*.24,y+math.sin(ang)*.18,base+.01),(x+math.cos(ang)*.17,y+math.sin(ang)*.13,base+.14),(x,y,base+.28)],[.012,.016,.025],bark,sides=7)
 for j in range(7):
  ang=j*2.399;start=Vector((x+.02,y+.02,base+h*.65));tip=Vector((x+math.cos(ang)*.23,y+math.sin(ang)*.18,base+h+random.uniform(-.08,.02)))
  tube('Mangrove / branch',[start,start.lerp(tip,.6),tip],[.016,.011,.004],bark,sides=7)
  for k in range(28):
   a=random.random()*math.tau;r=random.random()**.5*.13;c=tip+Vector((math.cos(a)*r,math.sin(a)*r*.8,random.uniform(-.035,.035)))
   d=Vector((math.cos(a),math.sin(a),.16))*.065;w=Vector((-math.sin(a),math.cos(a),0))*.025
   mi=ti;n=len(vs[mi]);vs[mi].extend([c-d,c+w,c+d,c-w,c+Vector((0,0,.009))]);fs[mi].extend([(n,n+1,n+4),(n+1,n+2,n+4),(n+2,n+3,n+4),(n+3,n,n+4)])
for i in range(3):
 me=bpy.data.meshes.new('Broadleaf canopy');me.from_pydata(vs[i],[],fs[i]);me.update();o=bpy.data.objects.new('Mangrove / canopy '+str(i),me);bpy.context.collection.objects.link(o);me.materials.append(leafm[i]);parent(o)
 for f in me.polygons:f.use_smooth=True
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'gambia.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'gambia.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('GAMBIA AUTHORED')
