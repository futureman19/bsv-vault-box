import bpy,math,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p=lid):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def tex(m,f,s,noncolor=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/f),check_existing=True)
 if noncolor:t.image.colorspace_settings.name='Non-Color'
 t.image.pack();m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[s])
stone=mat('Globigerina / honey cream',(.7,.55,.32),.78);tex(stone,'limestone-color.png','Base Color');tex(stone,'limestone-roughness.png','Roughness',True)
water=mat('Harbour / blue teal',(.025,.15,.19),.26,.1);tex(water,'harbour-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Deep teal joint',(.025,.055,.05),.9)
def uv(o):
 l=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone planar')
 for p in o.data.polygons:
  k=max(range(3),key=lambda k:abs(p.normal[k]));axes=[i for i in range(3) if i!=k]
  for li in p.loop_indices:
   c=o.data.vertices[o.data.loops[li].vertex_index].co;l.data[li].uv=(c[axes[0]]*.6+.5,c[axes[1]]*.6+.5)
def cube(n,loc,dim,m,p=None,bevel=.008):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if bevel:
  b=o.modifiers.new('Worn edge','BEVEL');b.width=min(bevel,min(dim)*.3);b.segments=1;bpy.ops.object.modifier_apply(modifier=b.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Segmented true ashlar skins with staggered seams; continuous liner behind.
for row in range(5):
 z=.10+(row+.5)*1.46/5;h=1.46/5-.012
 for sy in [-1,1]:
  cuts=sorted(set([-1.86,1.86]+[v for v in [-1.86+(.37 if row%2 else .74)+j*.74 for j in range(6)] if -1.85<v<1.85]))
  for a,b in zip(cuts,cuts[1:]):cube('Ashlar / long',((a+b)/2,sy*1.145,z),(b-a-.012,.19,h),stone)
 for sx in [-1,1]:
  cuts=sorted(set([-1.045,1.045]+[v for v in [-1.045+(.35 if row%2 else .7)+j*.7 for j in range(4)] if -1.03<v<1.03]))
  for a,b in zip(cuts,cuts[1:]):cube('Ashlar / side',(sx*1.745,(a+b)/2,z),(.23,b-a-.012,h),stone)
cube('Stone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam)
 for sy in [-1,1]:cube('Stone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone,lid,.045)
cube('Harbour / water inlay',(0,0,1.986),(3.19,1.88,.016),water,lid,.005)
# Peninsula is a single solid irregular angular bastion perimeter, not a map.
poly=[(-1.33,-.20),(-1.12,-.34),(-.96,-.16),(-.62,-.27),(-.48,-.45),(-.24,-.42),(-.12,-.19),(.25,-.20),(.41,-.40),(.66,-.32),(.68,-.10),(1.09,-.06),(1.31,.12),(1.12,.30),(.80,.25),(.61,.48),(.35,.44),(.22,.28),(-.16,.37),(-.32,.57),(-.57,.48),(-.64,.29),(-1.10,.31),(-1.30,.15)]
def prism(n,points,z,h,m):
 N=len(points);vs=[(x,y,zz) for zz in [z,z+h] for x,y in points];fs=[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(m);uv(o);parent(o);return o
prism('Peninsula / angular bastions',poly,1.995,.19,stone)
# Inset promenade and small urban blocks, all bonded to the same lid relief.
for i in range(7):
 x=-.96+i*.3
 cube('Peninsula / low ashlar block',(x,.055,2.225),(.23,.19,.08),stone,lid,.007)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Limestone / foot',(sx*1.47,sy*.91,-.10),(.52,.44,.35),stone,bevel=.07)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.29
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.2));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.1))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
s=bpy.context.scene;s.camera=cam;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.use_nodes=False;s.render.resolution_x=900;s.render.resolution_y=800;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'malta.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'malta.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
s.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('MALTA AUTHORED')
