"""Jamaica brief-driven landscape; procedural Blender source, no scans."""
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
stone_mat=mat('Limestone / warm porous cream',(.5,.45,.31),.8);maptex(stone_mat,'limestone-color.png','Base Color');maptex(stone_mat,'limestone-roughness.png','Roughness',True)
shale=mat('Shale / blue grey',(.15,.19,.23),.85);maptex(shale,'shale-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
forest=mat('Lid / deep forest green',(.0168,.0612,.0467),.52)
seam=mat('Mineral seam / forest shadow',(.025,.047,.032),.9)
terrain_mats=[mat('Forest / '+str(i),c,.92) for i,c in enumerate([(.024,.085,.052),(.04,.125,.071),(.064,.17,.092),(.09,.21,.115)])]+[shale,stone_mat]
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone projection')
 for p in o.data.polygons:
  n=p.normal; omit=max(range(3),key=lambda i:abs(n[i])); axes=[i for i in range(3) if i!=omit]
  for li in p.loop_indices:
   co=o.matrix_world@o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]*.65,co[axes[1]]*.65)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone_mat if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Limestone / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),stone_mat,bevel=.025)
for sx in [-1,1]:cube('Limestone / end wall',(sx*1.745,0,.83),(.23,2.10,1.46),stone_mat,bevel=.025)
cube('Limestone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone_mat,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Limestone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone_mat,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),forest,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Limestone / carved foot',(sx*1.47,sy*.91,-.07),(.48,.43,.31),stone_mat,bevel=.075)
# A connected triangulated relief with multiple asymmetric wooded ridges.
# Perimeter conforms to an irregular ellipse, with no rectangular display plinth.
verts=[(0,.05,2.48)];faces=[];rings=24;segments=112
for j in range(1,rings+1):
 r=j/rings
 for k in range(segments):
  a=k*math.tau/segments;edge=1+.025*math.sin(a*7)+.018*math.cos(a*11)
  x=1.40*r*math.cos(a)*edge;y=.05+.72*r*math.sin(a)*edge
  peaks=sum(h*math.exp(-((x-cx)/wx)**2-((y-cy)/wy)**2) for cx,cy,h,wx,wy in [(-.84,.06,.52,.36,.29),(-.10,.23,.71,.39,.33),(.65,.02,.58,.42,.30)])
  z=1.975+peaks*(1-r**8)+.027*math.sin(x*28+y*17)*math.sin(y*26-x*13)*(1-r)
  verts.append((x,y,z))
for k in range(segments):faces.append((0,1+k,1+(k+1)%segments))
for j in range(rings-1):
 for k in range(segments):
  a=1+j*segments+k;b=1+j*segments+(k+1)%segments;c=a+segments;d=b+segments
  faces.extend([(a,c,d),(a,d,b)])
mesh=bpy.data.meshes.new('Connected wooded mountain surface');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Terrain / Blue and John Crow relief',mesh);bpy.context.collection.objects.link(o)
for m in terrain_mats:mesh.materials.append(m)
for f in mesh.polygons:
 c=f.center
 f.material_index=5 if c.x>.80+.06*math.sin(c.y*31) and -.13<c.y<.02 and 2.14<c.z<2.29 else (4 if f.normal.z<.54 else int(2+math.sin(c.x*5+c.y*7))%4)
 f.use_smooth=True
uv(o)
# Low clustered broadleaf canopy relief, seated into actual terrain by rays.
# Stylized forest texture, not individually identified botanical trees.
terrain=o;canopies=[]
for j in range(180):
 x=random.uniform(-1.25,1.25);y=random.uniform(-.49,.60)
 hit,loc,normal,index=terrain.ray_cast(Vector((x,y,4)),Vector((0,0,-1)))
 if not hit or loc.z<2.05 or (x>.8 and y<.05):continue
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=loc)
 canopy=bpy.context.object;canopy.name='Terrain / broadleaf canopy'
 for v in canopy.data.vertices:
  k=random.uniform(.85,1.15);v.co=Vector((v.co.x*.066*k,v.co.y*.061*k,v.co.z*.047*k))
 canopy.data.materials.append(terrain_mats[j%4])
 for f in canopy.data.polygons:f.use_smooth=True
 parent(canopy);canopies.append(canopy)
parent(terrain)
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
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.use_nodes=False;scene.render.resolution_x=1000;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'jamaica.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'jamaica.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('PASS JAMAICA AUTHORED')
