"""Reference-led Japan pilot. Authored mesh and maps; no photogrammetry.
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
   u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z
   if axis=='Y' and abs(p.normal.z)>.7:v=co.x
   layer.data[li].uv=(u/3.72+.5,v/1.7+.5)
def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=1;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o
blue=mat('Cobalt / fired glaze',(.025,.08,.27),.27);maptex(blue,'cobalt-color.png','Base Color');maptex(blue,'glaze-roughness.png','Roughness',True)
clay=mat('Ochre / fired clay',(.46,.25,.065),.65);maptex(clay,'ochre-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
dark=mat('Mortar / deep blue',(.015,.025,.045),.9)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(clay if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Narrow brick courses with genuine vertical joints on four exterior faces.
for i in range(8):
 z=.10+(i+.5)*1.46/8;h=1.46/8-.008
 for sy in [-1,1]:
  # alternating offset partition, clipped exactly to silhouette
  cuts=sorted(set([-1.86,1.86]+[v for v in [-2.17+j*.62+(i%2)*.31 for j in range(9)] if -1.85<v<1.85]))
  for l,r in zip(cuts,cuts[1:]):cube('Glazed brick / long',((l+r)/2,sy*1.145,z),(r-l-.008,.19,h),blue,bevel=.004)
 for sx in [-1,1]:
  cuts=sorted(set([-1.04,1.04]+[v for v in [-1.2+j*.52+(i%2)*.26 for j in range(6)] if -1.04<v<1.04]))
  for l,r in zip(cuts,cuts[1:]):cube('Glazed brick / side',(sx*1.745,(l+r)/2,z),(.23,r-l-.008,h),blue,bevel=.004,axis='Y')
cube('Clasp seat',(0,-1.255,1.36),(.56,.075,.47),blue,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),dark,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),dark,bevel=.009)
 for sy in [-1,1]:cube('Rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),blue,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),blue,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Foot / clay',(sx*1.47,sy*.91,-.08),(.48,.42,.30),clay,bevel=.05)
# Ochre border and shallow architecture; all rigidly lid-borne.
for sy in [-1,1]:cube('Lid border / long',(0,sy*.94,1.99),(3.12,.055,.022),clay,lid,.004)
for sx in [-1,1]:cube('Lid border / short',(sx*1.53,0,1.99),(.055,1.88,.022),clay,lid,.004)
for i,(w,d) in enumerate([(1.36,.94),(1.02,.68),(.64,.40)]):
 cube('Babylon tier / '+str(i),(0,.13,2.045+i*.13),(w,d,.13),clay,lid,.015)
# Four compact geometric rosettes with eight bevelled rays; no religious figures.
for sx in [-1,1]:
 for sy in [-1,1]:
  x=sx*1.18;y=sy*.65
  cube('Rosette / center',(x,y,2.01),(.08,.08,.035),gold,lid,.008)
  for k in range(8):
   a=k*math.tau/8;o=cube('Rosette / petal',(x+.115*math.cos(a),y+.115*math.sin(a),2.012),(.105,.042,.026),clay,None,.006);o.rotation_euler.z=a;parent(o)
# Clean obsolete unreferenced theme resources from source.
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
# Studio rendering is a real render of the exact exported mesh.
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,4.5));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'iraq.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'iraq.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('IRAQ AUTHORED')
