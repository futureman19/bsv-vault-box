"""Lesotho / Maloti Basalt & Woven Indigo. Procedural Blender source."""
import bpy,math,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(8701)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
bpy.context.preferences.filepaths.save_version=0
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p=lid):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def tex(m,file,input,noncolor=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/file),check_existing=True)
 if noncolor:t.image.colorspace_settings.name='Non-Color'
 t.image.pack();m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[input])
stone=mat('Basalt / blue charcoal mineral',(.06,.08,.10),.78);tex(stone,'basalt-color.png','Base Color');tex(stone,'basalt-roughness.png','Roughness',True)
weave=mat('Textile / invented indigo weave',(.03,.05,.09),.92);tex(weave,'woven-indigo.png','Base Color')
gold=mat('Brass / aged satin',(.42,.26,.09),.31,.8)
inner=mat('Interior / dark slate',(.045,.06,.068),.65)
seam=mat('Seam / shadow charcoal',(.012,.02,.023),.95)
grass=mat('Highland / muted olive',(.14,.18,.075),.98)
peakm=[mat('Maloti / basalt facet '+str(i),c,.85) for i,c in enumerate([(.095,.13,.16),(.14,.18,.21),(.19,.23,.25),(.22,.25,.24)])]
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Authored surface')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   if abs(p.normal.z)>.7:u,v=co.x/3.72+.5,co.y/2.38+.5
   elif abs(p.normal.x)>.7:u,v=co.y/2.38+.5,co.z/1.5
   else:u,v=co.x/3.72+.5,co.z/1.5
   layer.data[li].uv=(u,v)
def cube(n,loc,dim,m,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if bevel:
  b=o.modifiers.new('Soft edges','BEVEL');b.width=min(bevel,min(dim)*.35);b.segments=3;bpy.ops.object.modifier_apply(modifier=b.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(inner if o.name.startswith('Interior') else gold)
# Continuous outer mineral walls. Subtle relief courses sit flush with the shell.
for sy in [-1,1]:cube('Basalt / front' if sy<0 else 'Basalt / rear',(0,sy*1.145,.83),(3.72,.19,1.46),stone,bevel=.028)
for sx in [-1,1]:cube('Basalt / side',(sx*1.745,0,.83),(.23,2.10,1.46),stone,bevel=.025)
# Irregular shallow mineral ledges, not repeated wood joinery.
for sy in [-1,1]:
 for row in range(3):
  z=.32+row*.44
  for j in range(5):
   x=-1.48+j*.73+random.uniform(-.06,.06)
   if sy<0 and abs(x)<.4:continue
   cube('Basalt / weathered ledge',(x,sy*1.241,z+random.uniform(-.14,.14)),(.18+random.random()*.25,.023,.04+random.random()*.04),stone,bevel=.009)
cube('Basalt / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.624),(3.28,.12 if sy<0 else .065,.070),seam,bevel=.008)
for sx in [-1,1]:cube('Seam / side',(sx*1.74,0,1.624),(.14,2.05,.070),seam,bevel=.008)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone,lid,.045)
panel=cube('Lid / woven indigo inset',(0,-.04,1.986),(3.28,1.94,.014),weave,lid,.004)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Basalt / low foot',(sx*1.47,sy*.91,-.09),(.48,.43,.29),stone,bevel=.08)
# One connected three-peak ridge: closed heightfield with irregular footprint.
# Coordinates chosen clear of latch sweep. Three unequal crests are geometric.
nx,ny=49,17;verts=[];faces=[]
for j in range(ny):
 v=j/(ny-1);y=-.12+v*.97
 for i in range(nx):
  u=i/(nx-1);x=-1.36+u*2.72
  edge=math.sin(math.pi*u)*math.sin(math.pi*v)
  peaks=sum(a*math.exp(-((x-c)/w)**2-((y-d)/.27)**2) for c,d,w,a in [(-.90,.42,.29,.55),(-.03,.51,.33,.48),(.87,.40,.29,.55)])
  z=2.001+.015+edge*(.045+peaks)+random.uniform(-.016,.016)*edge
  verts.append((x,y,z))
for j in range(ny-1):
 for i in range(nx-1):
  a=j*nx+i;faces.extend([(a,a+1,a+nx+1),(a,a+nx+1,a+nx)])
loop=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+list(range((ny-1)*nx+nx-2,(ny-1)*nx-1,-1))+[j*nx for j in range(ny-2,0,-1)]
bottom=len(verts);verts.extend([(verts[k][0],verts[k][1],1.997) for k in loop])
for k,a in enumerate(loop):
 b=loop[(k+1)%len(loop)];faces.append((b,a,bottom+k,bottom+(k+1)%len(loop)))
faces.append(tuple(reversed(range(bottom,len(verts)))))
me=bpy.data.meshes.new('Connected Maloti heightfield');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Maloti / three peak ridge',me);bpy.context.collection.objects.link(o)
for m in peakm:me.materials.append(m)
for f in me.polygons:f.material_index=random.choices(range(4),[4,5,2,1])[0]
parent(o)
# Grass-like low rough clustered patches, not an imported moss/tree asset.
for k in range(19):
 x=-1.24+k*.135;y=-.08+.055*math.sin(k*1.7)
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=(x,y,2.025));o=bpy.context.object;o.name='Highland / grass cushion';o.scale=(.09+random.random()*.05,.06,.025);o.data.materials.append(grass);parent(o)
# Original family medallion and side ring, decorative only.
def disk(n,loc,r,depth,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold);return o
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035)
bpy.ops.mesh.primitive_torus_add(major_segments=32,minor_segments=8,location=(0,-1.282,.87),major_radius=.107,minor_radius=.008,rotation=(math.pi/2,0,0));bpy.context.object.name='Medallion / raised rim';bpy.context.object.data.materials.append(gold)
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=32,minor_segments=8,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.25
bpy.ops.object.camera_add(location=(-5.6,-7.8,4.8));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'lesotho.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'lesotho.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('LESOTHO AUTHORED PASS')
