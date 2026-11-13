"""Norway fjord pilot. Authored mesh and maps; no photogrammetry.
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
rock=mat('Gneiss / cool folded mineral bands',(.13,.17,.19),.67);maptex(rock,'gneiss-color.png','Base Color');maptex(rock,'gneiss-roughness.png','Roughness',True)
granite=mat('Crystalline rock / fine grain',(.24,.28,.30),.8);maptex(granite,'cliff.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / charcoal',(.018,.03,.035),.9)
water=mat('Fjord / deep blue green',(.018,.16,.20),.21,.15)
forest=mat('Cliff / muted green crown',(.10,.18,.07),.94)
foam=mat('Cascade / pale mineral water',(.54,.75,.77),.3)
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
  o.data.materials.clear();o.data.materials.append(rock if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:
 cube('Gneiss / front' if sy<0 else 'Gneiss / rear',(0,sy*1.145,.83),(3.72,.19,1.46),rock,bevel=.025)
for sx in [-1,1]:
 cube('Gneiss / side',(sx*1.745,0,.83),(.23,2.10,1.46),rock,bevel=.025,axis='Y')
cube('Gneiss / clasp seat',(0,-1.255,1.36),(.56,.075,.47),rock,bevel=.025)
for sy in [-1,1]:
 cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Gneiss / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),rock,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),rock,lid,.045)
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
 for sy in [-1,1]:stone('Crystalline foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
def center(y):return .16*math.sin(y*3.8)+.035*math.cos(y*8)
def bankpoint(side,i,j):
 y=-.88+1.76*j/24;t=i/12
 inner=center(y)+side*(.36+.025*math.sin(y*6))
 outer=side*(1.48-.13*math.cos(y*3))
 x=inner*(1-t)+outer*t
 envelope=max(0,math.sin(math.pi*j/24))**.45
 z=1.978+envelope*(.23+.78*math.sin(math.pi*(.19+.81*t))**1.3)*(1+.08*math.sin(j*.7+i*.8+side))
 return (x,y,z)
for side in [-1,1]:
 verts=[bankpoint(side,i,j) for j in range(25) for i in range(13)];faces=[]
 for j in range(24):
  for i in range(12):
   a=j*13+i;f=(a,a+1,a+14,a+13);faces.append(f if side==1 else tuple(reversed(f)))
 # Watertight skirt and base, seated into stone lid.
 edge=list(range(13))+[j*13+12 for j in range(1,25)]+list(range(323,311,-1))+[j*13 for j in range(23,0,-1)]
 n=len(verts)
 verts.extend([(verts[k][0],verts[k][1],1.97) for k in edge])
 for k,a in enumerate(edge):b=edge[(k+1)%len(edge)];faces.append((a,b,n+(k+1)%len(edge),n+k))
 faces.append(tuple(reversed(range(n,len(verts)))))
 me=bpy.data.meshes.new('Solid crystalline cliff');me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new('Fjord bank / west' if side<0 else 'Fjord bank / east',me);bpy.context.collection.objects.link(o);me.materials.append(granite);me.materials.append(forest);parent(o);uv(o)
 for p in me.polygons:
  if p.index<288 and p.center.z>2.48 and p.normal.z>.45:p.material_index=1
 # normals unified on the closed solid
 select(o);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT')
# Continuous water ribbon, broad enough to reach beneath both bank walls.
verts=[]
for j in range(33):
 y=-.90+1.80*j/32;c=center(y)
 verts.extend([(c-.39,y,2.012),(c+.39,y,2.012)])
faces=[(j*2,j*2+1,j*2+3,j*2+2) for j in range(32)]
me=bpy.data.meshes.new('Continuous fjord');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Fjord / continuous water',me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o)
# Stylized cascade directly on the exposed inner west cliff face.
y=.29333333333333333;x=center(y)-(.36+.025*math.sin(y*6));top=bankpoint(-1,0,16)[2]
verts=[(x+.004,y-.025,top),(x+.004,y+.025,top),(x+.018,y+.035,2.012),(x+.018,y-.035,2.012)]
me=bpy.data.meshes.new('Cascade ribbon');me.from_pydata(verts,[],[(0,1,2,3)]);me.update();o=bpy.data.objects.new('Fjord / pale waterfall',me);bpy.context.collection.objects.link(o);me.materials.append(foam);parent(o)
# Clean obsolete unreferenced theme resources from source.
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
# Studio rendering is a real render of the exact exported mesh.
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.7));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'norway.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'norway.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('NORWAY AUTHORED')
