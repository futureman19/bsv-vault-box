import bpy, math, random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(734)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def parent(o,p):
 bpy.context.view_layer.update();m=o.matrix_world.copy();o.parent=p;o.matrix_world=m
 return o
def mat(n,c,r=.7,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
stone=mat('Titano limestone / invented procedural finish',(.48,.44,.36));gold=mat('Antique satin brass',(.48,.30,.10),.28,.8);seam=mat('Blue gray mineral seam',(.06,.13,.19));dark=mat('Tower window shadow',(.045,.055,.06));olive=mat('Olive scrub',(.12,.17,.055))
for file,inp in [('stone-color.png','Base Color'),('stone-roughness.png','Roughness'),('stone-normal.png','Normal')]:
 t=stone.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file));t.image.pack()
 if inp!='Base Color':t.image.colorspace_settings.name='Non-Color'
 if inp=='Normal':
  n=stone.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.45;stone.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);stone.node_tree.links.new(n.outputs['Normal'],stone.node_tree.nodes.get('Principled BSDF').inputs[inp])
 else:stone.node_tree.links.new(t.outputs['Color'],stone.node_tree.nodes.get('Principled BSDF').inputs[inp])
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone planar')
 for f in o.data.polygons:
  axis=max(range(3),key=lambda a:abs(f.normal[a]));axes=[a for a in range(3) if a!=axis]
  for li in f.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;layer.data[li].uv=(co[axes[0]]*.7,co[axes[1]]*.7)
def cube(n,loc,dim,m=stone,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if bevel:
  mod=o.modifiers.new('Stone edge','BEVEL');mod.width=min(bevel,min(dim)*.3);mod.segments=1;bpy.ops.object.modifier_apply(modifier=mod.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Thin continuous exterior stone walls with shallow staggered masonry joints.
for sy in [-1,1]:cube('Stone body / long',(0,sy*1.145,.83),(3.72,.19,1.46))
for sx in [-1,1]:cube('Stone body / side',(sx*1.745,0,.83),(.23,2.10,1.46))
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam)
 for sy in [-1,1]:cube('Stone rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112))
cube('Stone clasp seat',(0,-1.255,1.36),(.56,.075,.47),bevel=.025)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Stone foot',(sx*1.47,sy*.91,-.10),(.55,.46,.36),stone,bevel=.07)
def rock(n,loc,scale,p=lid,m=stone):
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  k=1+random.uniform(-.13,.13);v.co=Vector((v.co.x*scale[0]*k,v.co.y*scale[1]*k,v.co.z*scale[2]*k))
 o.data.materials.append(m);uv(o);parent(o,p);return o
# Ridge made of overlapping crag islands, with towers rooted in their peaks.
for i,(x,y,z,s) in enumerate([(-.98,-.30,2.10,(.55,.48,.25)),(0,.08,2.17,(.62,.55,.32)),(.98,.42,2.08,(.53,.42,.23))]):
 rock('Titano ridge / crag '+str(i),(x,y,z),s)
 h=[.54,.68,.43][i];base=[2.25,2.39,2.20][i];w=[.38,.40,.30][i]
 cube('Tower '+str(i+1)+' / keep',(x,y,base+h/2),(w,w,h),stone,lid,.015)
 cube('Tower '+str(i+1)+' / crown',(x,y,base+h-.02),(w+.07,w+.07,.08),stone,lid,.008)
 for a in [-1,1]:
  for b in [-1,1]:cube('Battlement '+str(i+1),(x+a*w*.40,y+b*w*.40,base+h+.055),(.10,.10,.12),stone,lid,.004)
 for zz in [base+.17,base+.34]:
  if zz<base+h-.08:cube('Window '+str(i+1),(x,y-w/2-.002,zz),(.065,.012,.095),dark,lid,.008)
 # Low wall sections intentionally join the ridge, not historic plan replicas.
 if i<2:cube('Fortification wall '+str(i),(x+.43,y+.07,2.27),(.48,.09,.19),stone,lid,.01)
for j,(x,y) in enumerate([(-.49,-.10),(.49,.28)]):
 rock('Titano ridge / saddle '+str(j),(x,y,2.105),(.51,.38,.20))
for i in range(18):
 x=random.uniform(-1.35,1.35);y=random.uniform(-.55,.65)
 rock('Scrub '+str(i),(x,y,2.00),(.09,.07,.035),lid,olive)
# Shared restrained side ring.
bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=8,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / brass';bpy.context.object.data.materials.append(gold)
cube('Side ring seat',(-1.87,0,1.04),(.07,.14,.14),gold)
for m in list(bpy.data.materials):
 if not m.users:bpy.data.materials.remove(m)
for im in list(bpy.data.images):
 if not im.users:bpy.data.images.remove(im)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.2));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.35))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.8
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=960;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.use_nodes=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'san-marino.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'san-marino.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('PASS SAN MARINO AUTHORED')
