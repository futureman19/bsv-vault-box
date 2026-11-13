"""Brief-led Southern Ocean pilot. Authored mesh and maps; no photogrammetry.
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
   if abs(p.normal.z)>.7:u,v=co.x,co.y
   elif abs(p.normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u/3.72+.5,v/1.7+.5)

def cube(n,loc,dim,material,p=None,bevel=.012,axis='X'):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material);uv(o,axis)
 if bevel:
  m=o.modifiers.new('Soft machined edges','BEVEL');m.width=min(bevel,min(dim)*.35);m.segments=3;bpy.ops.object.modifier_apply(modifier=m.name)
 if p:parent(o,p)
 return o

water=mat('Polar enamel / blue currents',(.025,.10,.15),.34)
maptex(water,'ocean-color.png','Base Color');maptex(water,'ocean-roughness.png','Roughness',True)
tex=water.node_tree.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(R/'maps/ocean-normal.png'));tex.image.colorspace_settings.name='Non-Color';tex.image.pack()
norm=water.node_tree.nodes.new('ShaderNodeNormalMap');norm.inputs['Strength'].default_value=.25;water.node_tree.links.new(tex.outputs['Color'],norm.inputs['Color']);water.node_tree.links.new(norm.outputs['Normal'],water.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
ice=mat('Ice / blue walls',(.28,.64,.73),.35)
snow=mat('Ice / snow plateau',(.72,.86,.90),.63)
liner=mat('Interior / midnight blue',(.018,.043,.055),.62)
seam=mat('Seam / dark cyan',(.017,.06,.075),.75)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(liner if o.name.startswith('Interior') else gold)
for sy in [-1,1]:cube('Ocean shell / front rear',(0,sy*1.145,.83),(3.72,.19,1.46),water,bevel=.025)
for sx in [-1,1]:cube('Ocean shell / side',(sx*1.745,0,.83),(.23,2.10,1.46),water,bevel=.025)
cube('Ocean shell / clasp seat',(0,-1.255,1.36),(.56,.075,.47),water,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Ocean rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),water,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),water,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Polar foot',(sx*1.47,sy*.91,-.07),(.49,.43,.29),liner,bevel=.06)
# Separate closed irregular prisms: level snow tops, cyan vertical calving edges.
def floe(name,x,y,rx,ry,height,count=7):
 angles=[i*math.tau/count for i in range(count)]
 outline=[(x+math.cos(a)*rx*random.uniform(.84,1),y+math.sin(a)*ry*random.uniform(.84,1)) for a in angles]
 verts=[(xx,yy,z) for z in [1.974,1.974+height] for xx,yy in outline]
 faces=[tuple(reversed(range(count))),tuple(range(count,2*count))]+[(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)]
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(ice);me.materials.append(snow);me.polygons[1].material_index=1;uv(o);parent(o);return o
floe('Tabular iceberg',.58,.48,.60,.36,.44,9)
for i,(x,y,rx,ry,h) in enumerate([(-1.18,-.68,.28,.22,.065),(-.48,-.67,.32,.19,.09),(.25,-.65,.29,.23,.06),(.98,-.57,.36,.21,.10),(-1.18,-.04,.24,.26,.075),(-.54,.03,.25,.23,.10),(-1.03,.61,.38,.24,.08),(-.23,.68,.19,.22,.07),(1.35,.48,.19,.29,.075)]):floe('Pack floe / '+str(i),x,y,rx,ry,h)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for i in list(bpy.data.images):
 if i.users==0:bpy.data.images.remove(i)
for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.23
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.8));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=1000;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.use_nodes=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'southern-ocean.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'southern-ocean.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('SOUTHERN OCEAN AUTHORED')
