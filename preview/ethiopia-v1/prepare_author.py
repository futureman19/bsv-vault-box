"""Construct scoped author script using the checked-in family helpers."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
s=s[:s.index('wood=mat')]+'''stone_mat=mat('Highland stone / weathered strata',(.38,.31,.24),.8);maptex(stone_mat,'stone-color.png','Base Color');maptex(stone_mat,'stone-roughness.png','Roughness',True)
dark=mat('Stone / dark foot',(.12,.11,.09),.9);maptex(dark,'stone-dark.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / deep olive',(.035,.045,.018),.92)
grass=mat('Afroalpine / olive',(.16,.20,.055),.95)
dry=mat('Afroalpine / dry ochre',(.28,.25,.09),.94)
'''+s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
a=s.index('def uv(');b=s.index('def cube(')
s=s[:a]+'''def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone projection')
 for p in o.data.polygons:
  n=p.normal
  for li in p.loop_indices:
   c=o.data.vertices[o.data.loops[li].vertex_index].co
   u,v=(c.x,c.y) if abs(n.z)>.7 else ((c.y,c.z) if abs(n.x)>.7 else (c.x,c.z))
   layer.data[li].uv=(u/3.72+.5,v/1.7+.5)
'''+s[b:]
s+='''
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone_mat if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Stone body / front rear',(0,sy*1.145,.83),(3.72,.19,1.46),stone_mat,bevel=.022)
for sx in [-1,1]:cube('Stone body / side',(sx*1.745,0,.83),(.23,2.10,1.46),stone_mat,bevel=.022)
cube('Stone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone_mat,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Stone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone_mat,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone_mat,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Stone foot',(sx*1.47,sy*.91,-.085),(.48,.42,.36),dark,bevel=.07)
# Three closed cliff masses, irregular rings and undulating grassy caps.
for name,cx,cy,rx,ry,h in [('west plateau',-.74,-.05,.69,.64,.54),('east massif',.58,.40,.69,.43,.79),('front buttress',.75,-.51,.46,.30,.34)]:
 count=32;verts=[];faces=[]
 for level in range(4):
  for j in range(count):
   a=math.tau*j/count;r=1+.075*math.sin(a*5)+.035*math.cos(a*9)
   k=[1,.94,.91,.87][level];z=1.978+[0,h*.35,h*.76,h][level]
   if level==3:z+=.025*math.sin(a*3)+.02*math.cos(a*5)
   verts.append((cx+rx*r*k*math.cos(a),cy+ry*r*k*math.sin(a),z))
 for level in range(3):
  for j in range(count):a=level*count+j;b=level*count+(j+1)%count;faces.append((a,b,b+count,a+count))
 verts.append((cx,cy,1.978+h+.012));center=len(verts)-1
 for j in range(count):faces.append((3*count+j,3*count+(j+1)%count,center))
 faces.append(tuple(reversed(range(count))))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Escarpment / '+name,me);bpy.context.collection.objects.link(o)
 for m in [stone_mat,grass,dry]:me.materials.append(m)
 for f in me.polygons:
  if 3*count<=f.index<4*count:f.material_index=1 if name!='front buttress' else 2
 uv(o);parent(o)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.28
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.9));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.25))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.9
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=1000;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.use_nodes=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'ethiopia.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'ethiopia.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('PASS ETHIOPIA AUTHORED')
'''
s=s.replace('Reference-led Japan pilot.','Brief-led Ethiopia pilot.')
(R/'author.py').write_text(s)
