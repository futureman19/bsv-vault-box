"""Cabo Verde / Fogo — Atlantic Caldera. Script-authored, no scans."""
import bpy, math, random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
random.seed(6100)
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
 t.image.pack();m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[input]);return t
stone=mat('Fogo / porous volcanic stone',(.055,.043,.034),.8)
tex(stone,'scoria-color.png','Base Color');tex(stone,'scoria-roughness.png','Roughness',True)
t=tex(stone,'scoria-normal.png','Normal',True);n=stone.node_tree.nodes.new('ShaderNodeNormalMap');stone.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);stone.node_tree.links.new(n.outputs['Normal'],stone.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
blue=mat('Atlantic / deep blue inlay',(.006,.025,.035),.4,.05)
ash=mat('Fogo / dry ash',(.09,.065,.045),.9)
rust=mat('Fogo / oxidized scoria',(.12,.040,.018),.9)
soil=mat('Fogo / cultivated green',(.065,.10,.025),.95)
inner=mat('Interior / charcoal stone',(.045,.038,.032),.85)
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone spatial UV')
 for p in o.data.polygons:
  for li in p.loop_indices:
   c=o.data.vertices[o.data.loops[li].vertex_index].co
   a,b=(c.x,c.y) if abs(p.normal.z)>.7 else ((c.x,c.z) if abs(p.normal.y)>.7 else (c.y,c.z))
   layer.data[li].uv=(a*.7,b*.7)
def cube(n,loc,dim,material,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o)
 if bevel:
  mod=o.modifiers.new('Soft stone edge','BEVEL');mod.width=min(bevel,min(dim)*.35);mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(inner if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Scoria / '+('front' if sy<0 else 'rear'),(0,sy*1.145,.83),(3.72,.19,1.46),stone,bevel=.04)
for sx in [-1,1]:cube('Scoria / side',(sx*1.745,0,.83),(.23,2.10,1.46),stone,bevel=.04)
cube('Scoria / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone,bevel=.025)
# Short, recessed blue sea-line: keep the inherited hinge's clearance.
for sy in [-1,1]:cube('Atlantic seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.088),blue,bevel=.009)
for sx in [-1,1]:
 cube('Atlantic seam / side',(sx*1.74,0,1.618),(.16,2.05,.088),blue,bevel=.009)
 for sy in [-1,1]:cube('Scoria / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Scoria / foot',(sx*1.47,sy*.91,-.10),(.53,.44,.34),stone,bevel=.075)
def mesh(n,vs,fs,mats,indices=None):
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o)
 for m in mats:me.materials.append(m)
 if indices:
  for p,i in zip(me.polygons,indices):p.material_index=i
 uv(o);parent(o);return o
# Broad horseshoe rim. Explicit east-facing gap rather than a closed ring.
vs=[];fs=[];mi=[];steps=100;rows=9
for i in range(steps+1):
 a=.50+(math.tau-1.00)*i/steps
 wave=1+.07*math.sin(a*7)+.035*math.cos(a*17)
 for j in range(rows):
  t=j/(rows-1);rad=.69+.33*t
  peak=math.sin(math.pi*t)**1.3
  z=1.986+peak*(.25+.12*(.5+.5*math.sin(a*3))) * (min(1,i/5,(steps-i)/5)*.8+.2)
  vs.append((1.37*rad*math.cos(a)*wave,.73*rad*math.sin(a)*wave,z))
for i in range(steps):
 for j in range(rows-1):
  q=i*rows+j;fs.append((q,q+1,q+rows+1,q+rows));mi.append(1 if j in [3,4] and i%9<6 else (2 if j==6 and i%13<8 else 0))
mesh('Caldera / open east horseshoe',vs,fs,[stone,ash,rust],mi)
# Off-center Fogo-inspired cone with an annular rim and depressed inner crater.
# Radial profile center->outside: crater floor, inner bowl, summit rim, fluted slopes.
profile=[(.0,2.39),(.09,2.39),(.14,2.43),(.205,2.70),(.25,2.73),(.32,2.64),(.43,2.43),(.57,2.18),(.68,1.992)]
N=96;vs=[(-.18,.02,profile[0][1])];fs=[];mi=[]
for k,(r,z) in enumerate(profile[1:]):
 for j in range(N):
  a=j*math.tau/N;ruffle=1+.03*math.sin(a*13)+.018*math.cos(a*23);dz=(.015*math.sin(a*9)+.008*math.sin(a*21))*(0 if k==0 else 1)
  vs.append((-.18+r*math.cos(a)*ruffle,.02+r*.88*math.sin(a)*ruffle,z+dz))
for j in range(N):fs.append((0,1+j,1+(j+1)%N));mi.append(0)
for k in range(len(profile)-2):
 for j in range(N):
  a=1+k*N+j;b=1+k*N+(j+1)%N;fs.append((a,a+N,b+N,b));mi.append(2 if k in [1,2] else (1 if k==4 and j%17<9 else 0))
mesh('Fogo / cratered cone',vs,fs,[stone,ash,rust],mi)
# Small cultivated plots suggest volcanic-soil agriculture, not literal vineyards.
for i in range(5):
 for j in range(3):
  o=cube('Cultivation / low green patch',(.67+i*.09,-.36+j*.09,1.996),(.065,.057,.022),soil,lid,.008)
# Restrained inherited-style side ring and front medallion.
def disk(n,loc,r,depth,rot=(math.pi/2,0,0)):
 bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=r,depth=depth,location=loc,rotation=rot);o=bpy.context.object;o.name=n;o.data.materials.append(gold);m=o.modifiers.new('Rounded brass','BEVEL');m.width=min(.005,depth*.35);m.segments=3;select(o);bpy.ops.object.modifier_apply(modifier=m.name)
disk('Medallion / solid emblem',(0,-1.258,.87),.13,.035)
disk('Side ring / mount',(-1.875,0,1.05),.085,.035,(0,math.pi/2,0))
bpy.ops.mesh.primitive_torus_add(major_segments=40,minor_segments=10,location=(-1.91,0,.91),major_radius=.125,minor_radius=.018,rotation=(0,math.pi/2,0));bpy.context.object.name='Side ring / hanging brass';bpy.context.object.data.materials.append(gold)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.28
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.2));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'cabo-verde.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'cabo-verde.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('CABO VERDE AUTHORED')
