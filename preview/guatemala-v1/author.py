"""Brief-led Guatemala pilot. Authored mesh and maps; no photogrammetry.
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
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z
   if axis=='Y' and abs(p.normal.z)>.7:v=co.x
   layer.data[li].uv=(u/3.72+.5,v/1.7+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o

cloth=mat('Indigo / original woven stripes',(.04,.07,.15),.8);maptex(cloth,'weave-color.png','Base Color');maptex(cloth,'weave-roughness.png','Roughness',True)
t=cloth.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/weave-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=cloth.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.35;cloth.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);cloth.node_tree.links.new(n.outputs['Normal'],cloth.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
stone=mat('Volcanic / dark grain',(.055,.07,.075),.84);maptex(stone,'stone-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
inside=mat('Interior / indigo lining',(.025,.04,.075),.88)
seam=mat('Seam / dark reveal',(.015,.022,.028),.9)
water=mat('Atitlan / bluegreen enamel',(.025,.24,.30),.22,.25)
peaks=mat('Volcano / forest green slopes',(.07,.13,.09),.86)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(inside if o.name.startswith('Interior') else gold)
for sy in [-1,1]:cube('Textile / front' if sy<0 else 'Textile / rear',(0,sy*1.145,.83),(3.72,.19,1.46),cloth,bevel=.018)
for sx in [-1,1]:cube('Textile / side',(sx*1.745,0,.83),(.23,2.10,1.46),cloth,bevel=.018,axis='Y')
cube('Textile / clasp seat',(0,-1.255,1.36),(.56,.075,.47),cloth,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Rim / corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Volcanic / foot',(sx*1.47,sy*.91,-.08),(.52,.44,.27),stone,bevel=.055)
# A contiguous irregular enamel lake, slightly raised within the stone lid.
N=64
boundary=[(1.35*math.cos(a)*(1+.07*math.sin(3*a)), -.10+.69*math.sin(a)*(1+.09*math.cos(5*a))) for a in [i*math.tau/N for i in range(N)]]
verts=[(x,y,z) for z in [1.966,2.015] for x,y in boundary]
faces=[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
me=bpy.data.meshes.new('Lake contour');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / contiguous lake',me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o)
# Three radial meshes with irregular flank rings, unequal heights/widths.
for k,(cx,cy,r,h) in enumerate([(-.95,.56,.36,.43),(-.12,.65,.43,.68),(.83,.57,.38,.54)]):
 verts=[];faces=[];sides=32
 for j,(fraction,height) in enumerate([(1,0),(.78,.16),(.50,.44),(.23,.77)]):
  for i in range(sides):
   a=i*math.tau/sides;rr=r*fraction*(1+.10*math.sin(a*5+k)+.045*math.cos(a*9));verts.append((cx+rr*math.cos(a),cy+rr*.80*math.sin(a),1.97+h*height+.008*math.sin(a*3)))
 verts.append((cx+.025,cy,1.97+h));top=len(verts)-1
 faces.append(tuple(reversed(range(sides))))
 for j in range(3):
  for i in range(sides):a=j*sides+i;b=j*sides+(i+1)%sides;faces.append((a,b,b+sides,a+sides))
 for i in range(sides):faces.append((3*sides+i,3*sides+(i+1)%sides,top))
 me=bpy.data.meshes.new('Irregular volcanic relief');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / volcano '+str(k+1),me);bpy.context.collection.objects.link(o);me.materials.append(peaks);me.materials.append(stone)
 for p in me.polygons:p.material_index=1 if p.center.z>2.4 else 0
 uv(o);parent(o)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.24
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.4));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.render.resolution_x=1000;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.use_compositing=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'guatemala.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'guatemala.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('GUATEMALA AUTHORED')
