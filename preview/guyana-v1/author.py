"""Original procedural Guyana landscape on preserved collection mechanism."""
import bpy,math,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(741)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o,p):
 bpy.context.view_layer.update();m=o.matrix_world.copy();o.parent=p;o.matrix_world=m;return o
def mat(n,c,r=.5,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def tex(m,f,socket):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/f));t.image.pack()
 if socket!='Base Color':t.image.colorspace_settings.name='Non-Color'
 if socket=='Normal':
  n=m.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.35;m.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);m.node_tree.links.new(n.outputs['Normal'],m.node_tree.nodes.get('Principled BSDF').inputs[socket])
 else:m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[socket])
stone=mat('Sandstone / layered escarpment',(.3,.15,.08),.78)
for f,s in [('color','Base Color'),('roughness','Roughness'),('normal','Normal')]:tex(stone,'sandstone-'+f+'.png',s)
gold=mat('Brass / satin',(.48,.30,.10),.28,.8);green=mat('Lid / forest enamel',(.025,.075,.043),.29);liner=mat('Interior / deep umber',(.055,.032,.018),.65);seam=mat('Seam / forest mineral',(.024,.045,.025),.85)
leaves=[mat('Canopy / '+str(i),c,.85) for i,c in enumerate([(.025,.08,.035),(.045,.12,.05),(.07,.15,.055)])]
water=mat('Potaro / amber water',(.27,.12,.035),.2);foam=mat('Kaieteur / ivory cascade',(.79,.80,.67),.25);pool=mat('Pool / tea green',(.065,.16,.11),.18)
def uv(o):
 l=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone projection')
 for p in o.data.polygons:
  axis=max(range(3),key=lambda i:abs(p.normal[i]))
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   u,v=(co.x,co.y) if axis==2 else ((co.y,co.z) if axis==0 else (co.x,co.z))
   l.data[li].uv=(u/3.72+.5,v/1.8+.5)
def cube(n,loc,dim,m,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if bevel:
  b=o.modifiers.new('Soft edges','BEVEL');b.width=min(bevel,min(dim)*.35);b.segments=2;bpy.ops.object.modifier_apply(modifier=b.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(liner if o.name.startswith('Interior') else gold)
for sy in [-1,1]:cube('Body / sandstone long',(0,sy*1.145,.83),(3.72,.19,1.46),stone,bevel=.025)
for sx in [-1,1]:cube('Body / sandstone side',(sx*1.745,0,.83),(.23,2.10,1.46),stone,bevel=.025)
cube('Body / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam)
for sx in [-1,1]:cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),green,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Foot / sandstone',(sx*1.47,sy*.91,-.10),(.55,.46,.35),stone,bevel=.07)
# Irregular stratified plateau, upper river, exposed front cliff and low pool.
outline=[(-1.28,-.72),(-.83,-.88),(-.30,-.79),(.22,-.73),(.76,-.58),(1.25,-.24),(1.32,.35),(.91,.73),(.25,.78),(-.38,.68),(-1.04,.35)]
def prism(n,points,bottom,top,m):
 vs=[(x,y,bottom) for x,y in points]+[(x,y,top) for x,y in points];N=len(points);fs=[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)];me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(m);uv(o);parent(o,lid);return o
prism('Terrain / lower island',outline,1.96,2.09,stone)
upper=[(-1.15,-.20),(-.60,-.23),(-.23,-.14),(.44,-.23),(1.14,-.10),(1.19,.31),(.85,.64),(.27,.69),(-.38,.59),(-1.02,.30)]
prism('Terrain / sandstone plateau',upper,2.07,2.65,stone)
# Connected solid ribbon, width 0.26; gentle bend across the plateau.
river=[(-.63,-.235),(-.37,-.235),(-.31,.00),(-.16,.25),(.02,.43),(.09,.68),(-.18,.68),(-.25,.45),(-.42,.28),(-.56,.04)]
prism('Water / upper Potaro river',river,2.647,2.67,water)
# The front cliff is near y=-.23 at waterfall location. Curtain ends in pool.
cube('Water / connected waterfall',(-.50,-.245,2.38),(.26,.045,.58),foam,lid,.008)
prism('Water / lower pool',[(-.91,-.58),(-.69,-.72),(-.31,-.70),(-.13,-.50),(-.29,-.25),(-.63,-.245),(-.85,-.36)],2.087,2.111,pool)
for i in range(6):
 cube('Water / fall streak '+str(i),(-.60+i*.04,-.271,2.38),(.009,.009,.54),foam,lid,.002)
# Canopies: clustered low irregular crowns rather than cone trees; river stays exposed.
for i,(x,y,r) in enumerate([(-.91,.20,.20),(-.78,.41,.22),(-.57,.51,.18),(.21,.50,.20),(.47,.43,.25),(.79,.39,.24),(.97,.14,.18),(.68,.02,.21),(.28,.02,.18),(-1.04,-.02,.13),(.80,-.47,.19),(-1.04,-.50,.14)]):
 z=2.65 if i<10 else 2.09
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=(x,y,z+.055));o=bpy.context.object;o.name='Canopy / crown '+str(i)
 for v in o.data.vertices:
  k=random.uniform(.85,1.15);v.co=Vector((v.co.x*r*k,v.co.y*r*k,v.co.z*r*.62*k))
 o.data.materials.append(leaves[i%3]);parent(o,lid)
 for p in o.data.polygons:p.use_smooth=True
# Real source studio; not promotional imagery.
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.7));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.2))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
s=bpy.context.scene;s.camera=cam;s.render.engine='CYCLES';s.cycles.samples=24;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=900;s.render.resolution_y=850;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.use_compositing=False
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for im in list(bpy.data.images):
 if im.users==0:bpy.data.images.remove(im)
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'guyana.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'guyana.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
s.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('GUYANA_AUTHORED_PASS')
