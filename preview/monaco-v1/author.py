"""Monaco fictional Rock/Riviera miniature, authored after design-brief.md."""
import bpy,math,random
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent;random.seed(421)
bpy.ops.wm.open_mainfile(filepath=str(R/'mechanism.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];latch=bpy.data.objects['Latch_Pivot']
exec((R/'helpers.py').read_text())
stone_mat=mat('Limestone-inspired / cream mineral',(.60,.53,.40),.75)
maptex(stone_mat,'stone-color.png','Base Color');maptex(stone_mat,'stone-roughness.png','Roughness',True)
t=stone_mat.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/stone-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack();n=stone_mat.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.3;stone_mat.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);stone_mat.node_tree.links.new(n.outputs['Normal'],stone_mat.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / satin',(.48,.30,.10),.28,.8);sea=mat('Mediterranean / azure enamel',(.012,.17,.26),.24,.15);red=mat('Riviera / crimson enamel',(.42,.018,.025),.32);ivory=mat('Ivory / architectural plaster',(.78,.72,.59),.72);roof=mat('Terracotta / roofs',(.38,.095,.045),.8);green=mat('Garden / muted evergreen',(.06,.13,.045),.9);seam=mat('Seam / deep azure',(.008,.035,.045),.8)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone_mat if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Stone / front' if sy<0 else 'Stone / rear',(0,sy*1.145,.83),(3.72,.19,1.46),stone_mat,bevel=.022)
for sx in [-1,1]:cube('Stone / side',(sx*1.745,0,.83),(.23,2.10,1.46),stone_mat,bevel=.022)
cube('Stone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone_mat,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Stone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone_mat,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone_mat,lid,.045)
cube('Riviera / sea inset',(0,0,1.982),(3.21,1.92,.025),sea,lid,.008)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  stone('Stone foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),material=stone_mat,sub=2)
# Architectural red/ivory inset, separated from mechanism swept volume.
for sx in [-1,1]:
 cube('Inlay / ivory frame',(sx*1.02,-1.246,.83),(.98,.018,.68),ivory,bevel=.005)
 for j in range(5):
  ob=cube('Inlay / crimson diamond',(sx*1.02+(j-2)*.17,-1.260,.83),(.115,.012,.115),red,bevel=.002);ob.rotation_euler.y=math.pi/4
 cube('Inlay / side ivory',(sx*1.866,0,.83),(.016,1.42,.48),ivory,bevel=.004)
 cube('Inlay / side crimson',(sx*1.877,0,.83),(.012,1.28,.13),red,bevel=.003)
# Irregular sheer-sided promontory with flat urban terrace and stepped coves.
outline=[(-1.30,.78),(-.92,.91),(-.35,.87),(.32,.89),(1.17,.71),(1.35,.40),(1.03,.16),(.64,.06),(.32,-.18),(-.08,-.26),(-.45,-.05),(-.85,-.02),(-1.18,.20)]
verts=[(x,y,1.99) for x,y in outline]+[(x*.94,y*.94,2.30+(.025 if i%3==0 else 0)) for i,(x,y) in enumerate(outline)]
k=len(outline);faces=[tuple(reversed(range(k))),tuple(range(k,2*k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
me=bpy.data.meshes.new('Rock terrace');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Riviera / Rock promontory',me);bpy.context.collection.objects.link(o);o.data.materials.append(stone_mat);uv(o);parent(o)
# Cream courses and tiny roof silhouettes, kept within terrace footprint.
for i,(x,y,w,d,h) in enumerate([(-.86,.48,.32,.29,.22),(-.42,.45,.34,.32,.30),(0,.48,.34,.29,.25),(.43,.49,.32,.30,.32),(.87,.43,.27,.27,.22),(-.38,.08,.24,.22,.20),(.09,.10,.24,.24,.24)]):
 z=2.31;cube('Old town / building '+str(i),(x,y,z+h/2),(w,d,h),ivory,lid,.006)
 # true pitched roof prism
 v=[(x-w*.56,y-d*.56,z+h),(x+w*.56,y-d*.56,z+h),(x+w*.56,y+d*.56,z+h),(x-w*.56,y+d*.56,z+h),(x,y-d*.56,z+h+.10),(x,y+d*.56,z+h+.10)]
 m=bpy.data.meshes.new('Pitched roof');m.from_pydata(v,[],[(0,3,2,1),(0,1,4),(3,5,2),(0,4,5,3),(1,2,5,4)]);m.update();ob=bpy.data.objects.new('Old town / roof '+str(i),m);bpy.context.collection.objects.link(ob);m.materials.append(roof);parent(ob)
 for dx in [-.07,.07]:cube('Old town / window',(x+dx,y-d/2-.004,z+h*.55),(.035,.008,.065),sea,lid,.001)
for x,y in [(-1.04,.28),(-.69,.20),(.68,.28),(.42,.10),(1.05,.54),(-.13,.70)]:
 stone('Garden / canopy',(x,y,2.39),(.10,.075,.12),lid,green,2)
# Pale contour ledges are subordinate to the broad blue foreground.
for i in range(8):
 x=-1.1+i*.30;stone('Rock / coastal ledge',(x,-.18+.08*math.sin(i),2.04),(.16,.09,.06),lid,stone_mat,1)
for m in list(bpy.data.materials):
 if m.users==0:bpy.data.materials.remove(m)
for im in list(bpy.data.images):
 if im.users==0:bpy.data.images.remove(im)
for ob in bpy.data.objects:
 if ob.name=='Studio / shadow floor':ob.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.6));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.7
sc=bpy.context.scene;sc.camera=cam;sc.render.engine='CYCLES';sc.cycles.samples=24;sc.cycles.use_denoising=False;sc.render.threads_mode='FIXED';sc.render.threads=4;sc.render.resolution_x=900;sc.render.resolution_y=720;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.use_nodes=False
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'monaco.blend'))
bpy.ops.object.select_all(action='DESELECT')
for ob in bpy.data.objects:
 if not ob.name.startswith('Studio') and ob.type in ['MESH','EMPTY']:ob.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'monaco.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
sc.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('MONACO_AUTHORED')
