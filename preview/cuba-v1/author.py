import bpy,math,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(840)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def mat(n,c,r=.6,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def tex(m,f,input,non=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/f),check_existing=True)
 if non:t.image.colorspace_settings.name='Non-Color'
 t.image.pack();m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[input])
stone=mat('Limestone / warm porous',(.45,.42,.33));tex(stone,'limestone.png','Base Color');tex(stone,'roughness.png','Roughness',True)
earth=mat('Valley / red earth',(.3,.08,.03));tex(earth,'earth.png','Base Color')
green=mat('Mogote / olive canopy',(.065,.14,.028),.92);gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8);seam=mat('Seam / muted green',(.035,.07,.032),.9)
def parent(o,p):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw
 return o
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new()
 for f in o.data.polygons:
  axis=max(range(3),key=lambda i:abs(f.normal[i]));axes=[i for i in range(3) if i!=axis]
  for li in f.loop_indices:
   v=o.data.vertices[o.data.loops[li].vertex_index].co;layer.data[li].uv=(v[axes[0]]*.7+.5,v[axes[1]]*.7+.5)
def cube(n,loc,dim,m,p=None,b=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if b:
  mod=o.modifiers.new('Soft edges','BEVEL');mod.width=min(b,min(dim)*.3);mod.segments=2;bpy.ops.object.modifier_apply(modifier=mod.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Limestone / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),stone)
for sx in [-1,1]:cube('Limestone / end wall',(sx*1.745,0,.83),(.23,2.10,1.46),stone)
cube('Limestone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone,b=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,b=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,b=.009)
 for sy in [-1,1]:
  cube('Limestone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone,b=.004)
  cube('Limestone / foot',(sx*1.47,sy*.91,-.08),(.51,.45,.32),stone,b=.06)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
cube('Valley / earth plain',(0,0,1.999),(3.12,1.75,.06),earth,lid,.025)
# Closed ring stacks give abrupt limestone flanks and rounded vegetated crowns.
for k,(cx,cy,rx,ry,h) in enumerate([(-.94,.29,.43,.39,.61),(.02,.39,.45,.37,.82),(.91,.08,.39,.38,.46)]):
 verts=[];faces=[];N=32;levels=[(0,.94),(.12,1),(.50,.91),(.77,.72),(.94,.36),(1,.07)]
 for j,(z,r) in enumerate(levels):
  for i in range(N):
   a=i*math.tau/N;w=1+.065*math.sin(a*5+k)+.025*math.sin(a*11+j);verts.append((cx+rx*r*w*math.cos(a),cy+ry*r*w*math.sin(a),2.023+h*z))
 for j in range(len(levels)-1):
  for i in range(N):faces.append((j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i))
 faces.extend([tuple(reversed(range(N))),tuple((len(levels)-1)*N+i for i in range(N))]);me=bpy.data.meshes.new('Mogote rings');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Mogote / '+str(k+1),me);bpy.context.collection.objects.link(o);me.materials.append(stone);me.materials.append(green)
 for f in me.polygons:
  f.material_index=1 if f.center.z>2.023+h*.66 else 0
 uv(o);parent(o,lid)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.27
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.2));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.8
s=bpy.context.scene;s.camera=cam;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=1000;s.render.resolution_y=900;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.use_nodes=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'cuba.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'cuba.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
s.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True);print('CUBA AUTHORED PASS')
