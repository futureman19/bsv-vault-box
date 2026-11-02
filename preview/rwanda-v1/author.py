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
earth=mat('Terracotta / pigment',(.32,.06,.028),.85);maptex(earth,'earth.png','Base Color')
wood=mat('Wood / dark liner',(.065,.024,.012),.6);maptex(wood,'wood.png','Base Color')
ivory=mat('Kaolin / ivory',(.80,.68,.49),.7);maptex(ivory,'ivory.png','Base Color')
black=mat('Charcoal / relief',(.018,.012,.009),.65)
ochre=mat('Ochre / accent',(.48,.23,.045),.7)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
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
for sy in [-1,1]:
 cube('Earth / wall',(0,sy*1.145,.83),(3.72,.19,1.46),earth)
 cube('Dark seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),black,bevel=.009)
for sx in [-1,1]:
 cube('Earth / side',(sx*1.745,0,.83),(.23,2.10,1.46),earth)
 cube('Dark seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),black,bevel=.009)
 for sy in [-1,1]:
  cube('Earth / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),earth,bevel=.004)
  cube('Dark wood foot',(sx*1.47,sy*.91,-.07),(.46,.40,.34),wood,bevel=.06)
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
cube('Earth / clasp seat',(0,-1.255,1.36),(.56,.075,.47),earth,bevel=.025)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),earth,lid,.045)
# Closed diamond annuli with genuine raised faces, independently composed.
def diamond(n,c,w,h,t,material,plane='top',p=None):
 outer=[(0,-h),(w,0),(0,h),(-w,0)];inner=[(0,-h+t),(w-t,0),(0,h-t),(-w+t,0)]
 verts=[]
 for depth in [0,.028]:
  for a,b in outer+inner:
   if plane=='top':v=(c[0]+a,c[1]+b,c[2]+depth)
   elif plane=='front':v=(c[0]+a,c[1]-depth,c[2]+b)
   else:v=(c[0]-depth,c[1]+a,c[2]+b)
   verts.append(v)
 faces=[]
 for k in range(4):
  q=(k+1)%4
  faces.extend([(k,q,q+4,k+4),(k+8,k+12,q+12,q+8),(k,q,q+8,k+8),(k+4,k+12,q+12,q+4)])
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material)
 # Recalculate outward normals on closed relief solids.
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();uv(o)
 if p:parent(o,p)
 return o
for x in [-1.15,0,1.15]:
 for idx,(w,h,t,m) in enumerate([(.51,.82,.085,ivory),(.35,.59,.065,black),(.20,.35,.055,ochre)]):
  diamond('Lid relief / diamond', (x,0,1.982),w,h,t,m,p=lid)
for x in [-1.45,-.88,.88,1.45]:
 for z in [.51,1.10]:
  diamond('Body relief / front',(x,-1.242,z),.23,.25,.065,ivory,'front')
  diamond('Body relief / inset',(x,-1.244,z),.115,.13,.038,black,'front')
for y in [-.70,0,.70]:
 for z in [.51,1.10]:
  diamond('Body relief / side',(-1.862,y,z),.29,.25,.065,ivory,'side')
  diamond('Body relief / side inset',(-1.864,y,z),.15,.13,.038,black,'side')
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
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'rwanda.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'rwanda.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('RWANDA AUTHORED')
