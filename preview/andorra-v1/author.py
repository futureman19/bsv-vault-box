"""Brief-led Andorra pilot. Procedural stone and pastoral valley, not a scan.
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
stone_mat=mat('Granite / local stone',(.28,.29,.28),.8);maptex(stone_mat,'stone-color.png','Base Color');maptex(stone_mat,'stone-roughness.png','Roughness',True)
wood=stone_mat
end=stone_mat
granite=stone_mat
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
slate=mat('Slate / charcoal lid',(.065,.085,.10),.36);maptex(slate,'slate-color.png','Base Color')
seam=mat('Charcoal / recessed joints',(.025,.033,.035),.95)
pasture=mat('Pasture / muted olive',(.17,.22,.085),.95)
pathmat=mat('Path / pale stone',(.43,.41,.34),.85)
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   normal=p.normal
   if abs(normal.z)>=max(abs(normal.x),abs(normal.y)):u,v=co.x,co.y
   elif abs(normal.x)>abs(normal.y):u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u*.7+.5,v*.7+.5)
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
# Staggered physical masonry skins, four courses, butt-jointed corners.
for row in range(4):
 z=.10+(row+.5)*1.46/4;h=1.46/4-.018
 for sy in [-1,1]:
  cuts=[-1.64]+sorted(-1.64+(i+.4*(row%2))*3.28/6 for i in range(1,6))+[1.64]
  for i,(a,b) in enumerate(zip(cuts,cuts[1:])):
   cube('Masonry / long block',((a+b)/2,sy*1.145,z),(b-a-.016,.19,h),stone_mat,bevel=.012)
 for sx in [-1,1]:
  cuts=[-1.24,-.68+.1*(row%2),-.10,.48+.1*(row%2),1.24]
  for a,b in zip(cuts,cuts[1:]):cube('Masonry / side block',(sx*1.745,(a+b)/2,z),(.23,b-a-.016,h),stone_mat,bevel=.012)
# Small collar fills the central clasp mounting behind its retained position.
cube('Cedar / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:
 cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Cedar / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),slate,lid,.045)
# Restrained brass corner protectors replace the Iceland wraps entirely.
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
 for sy in [-1,1]:stone('Granite foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)
# Closed low-poly flanks, central pastoral valley left clear.
for sign in [-1,1]:
 nx,ny=14,14;verts=[];faces=[]
 for j in range(ny+1):
  y=-.83+1.66*j/ny
  for i in range(nx+1):
   u=i/nx;x=sign*(.28+1.13*u)
   env=max(0,math.sin(math.pi*u))*max(0,math.sin(math.pi*j/ny))
   z=1.98+.68*env**.7*(.8+.15*math.sin(j*.7+i*.8))
   verts.append((x,y,z))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;q=(a,a+1,a+nx+2,a+nx+1);faces.append(q if sign>0 else tuple(reversed(q)))
 boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
 for k,a in enumerate(boundary):
  b=boundary[(k+1)%len(boundary)];c=len(verts);verts.extend([(verts[a][0],verts[a][1],1.975),(verts[b][0],verts[b][1],1.975)]);faces.append((a,b,c+1,c))
 me=bpy.data.meshes.new('Madriu flank');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / valley flank '+str(sign),me);bpy.context.collection.objects.link(o);me.materials.append(stone_mat);me.materials.append(pasture)
 for f in me.polygons:
  f.material_index=1 if f.center.z<2.19 else 0
 uv(o);parent(o)
cube('Terrain / valley pasture',(0,0,1.989),(.55,1.7,.018),pasture,lid,.004)
for j in range(15):
 y=-.76+j*.108;x=.08*math.sin(j*.45)
 cube('Path / stepping stone',(x,y,2.008),(.19,.092,.022),pathmat,lid,.006)
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
bpy.ops.object.camera_add(location=(-5.6,-7.8,6.4));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=2;scene.use_nodes=False;scene.render.resolution_x=900;scene.render.resolution_y=820;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'andorra.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'andorra.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('ANDORRA AUTHORED')
