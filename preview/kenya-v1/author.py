"""Original procedural Kenya landscape collectible; inherited mechanism only."""
import bpy,math,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(1060)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
def parent(o,p):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=p;o.matrix_world=mw;return o
def mat(n,c,r=.6,metal=0):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=r;p.inputs['Metallic'].default_value=metal;return m
def tex(m,f,slot,noncolor=False):
 t=m.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps'/f),check_existing=True)
 if noncolor:t.image.colorspace_settings.name='Non-Color'
 t.image.pack();m.node_tree.links.new(t.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs[slot])
stone=mat('Volcanic stone',(.08,.055,.035),.85);tex(stone,'volcanic-color.png','Base Color');tex(stone,'stone-roughness.png','Roughness',True)
earth=mat('Ochre escarpment',(.31,.19,.06),.9);tex(earth,'ochre-color.png','Base Color')
gold=mat('Satin brass',(.48,.30,.10),.28,.8)
water=mat('Soda lake / blue green',(.087,.262,.223),.19,.12)
shore=mat('Mineral shoreline',(.63,.52,.28),.8)
seam=mat('Dark seam',(.025,.023,.019),.9)
def uv(o):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone projection')
 for p in o.data.polygons:
  for li in p.loop_indices:
   c=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=((c.y if abs(p.normal.x)>.7 else c.x)/3.72+.5,(c.y if abs(p.normal.z)>.7 else c.z)/2.38+.5)
def cube(n,loc,dim,m,p=None,bevel=.012):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(m);uv(o)
 if bevel:
  mod=o.modifiers.new('Rounded edges','BEVEL');mod.width=min(bevel,min(dim)*.35);mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 if p:parent(o,p)
 return o
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Volcanic / wall',(0,sy*1.145,.83),(3.72,.19,1.46),stone,bevel=.035)
for sx in [-1,1]:cube('Volcanic / side',(sx*1.745,0,.83),(.23,2.10,1.46),stone,bevel=.03)
cube('Volcanic / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.08),seam)
for sx in [-1,1]:cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.08),seam)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Volcanic foot',(sx*1.47,sy*.91,-.08),(.55,.47,.32),stone,bevel=.10)
# Low jagged ridge islands flank the basin, with real closed mesh relief.
def ridge(n,cx,cy,length,width,height):
 verts=[];N=17
 for row in range(3):
  for i in range(N):
   x=cx+(i/(N-1)-.5)*length;y=cy+(row-1)*width*.5
   z=1.99 if row!=1 else 2.04+height*(.35+.65*math.sin(math.pi*i/(N-1)))*random.uniform(.65,1)
   verts.append((x,y,z))
 faces=[]
 for row in range(2):
  for i in range(N-1):
   a=row*N+i;faces.extend([(a,a+1,a+1+N),(a,a+1+N,a+N)])
 boundary=list(range(N))+[2*N-1,3*N-1]+list(range(3*N-2,2*N-1,-1))+[N]
 center=len(verts);verts.append((cx,cy,1.985))
 for a,b in zip(boundary,boundary[1:]+boundary[:1]):faces.append((center,b,a))
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(earth);uv(o);parent(o,lid)
ridge('Terrain / north escarpment',0,.62,3.10,.55,.48)
ridge('Terrain / south escarpment',.12,-.77,2.78,.30,.10)
# Irregular flat lake outlines with separate narrow raised shoreline rings.
for j,(cx,cy,rx,ry) in enumerate([(-.97,-.02,.35,.29),(-.02,.06,.40,.32),(.98,-.06,.30,.25)]):
 N=40;ring=[]
 for i in range(N):
  a=i*math.tau/N;k=1+.09*math.sin(3*a+j)+.06*math.sin(7*a);ring.append((cx+rx*k*math.cos(a),cy+ry*k*math.sin(a),2.008))
 me=bpy.data.meshes.new('Lake');me.from_pydata([(cx,cy,2.008)]+ring,[],[(0,i+1,(i+1)%N+1) for i in range(N)]);me.update();o=bpy.data.objects.new('Lake / '+str(j+1),me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o,lid)
 vs=ring+[(cx+(x-cx)*1.08,cy+(y-cy)*1.08,z+.006) for x,y,z in ring];fs=[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
 me=bpy.data.meshes.new('Shore');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Shore / '+str(j+1),me);bpy.context.collection.objects.link(o);me.materials.append(shore);parent(o,lid)
# Small irregular stone facets on exterior stay static and clear of articulation.
for sy in [-1,1]:
 for i in range(14):
  x=-1.55+i*.24;z=.36+random.random()*.64
  o=cube('Volcanic / broken facet',(x,sy*1.245,z),(.16+random.random()*.10,.025,.12+random.random()*.20),stone,bevel=.008);o.rotation_euler.y=random.uniform(-.3,.3)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.27
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'kenya.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'kenya.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('KENYA AUTHORED')
