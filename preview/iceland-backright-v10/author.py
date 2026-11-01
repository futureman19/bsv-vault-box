"""Four scoped corrections; reopen v8, retain stone geometry and articulation."""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'approved-v9.blend'),use_scripts=False)
lid=bpy.data.objects['Lid_Hinge'];bpy.context.view_layer.update()
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def parent(o):
 bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=lid;o.matrix_world=mw
 return o
def mesh(name,v,f,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(mat);return parent(o)
def normals(o):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
# Physical axes established from unchanged latch y=-1.29 and hinge y=+1.32.
# Head-on latch view: +X is right, +Y back. Never use screen X.
old=bpy.data.objects['Glacier / crevassed asymmetric ridge'];mat=old.data.materials[0];bpy.data.objects.remove(old,do_unlink=True)
v=[];f=[]
profile=[0,.08,.17,.12,.245,.29,.16,.09,0]
for i in range(9):
 x=.86+.79*i/8
 for j in range(5):
  y=.68+(j-2)*.15*(.69+.31*math.sin(math.pi*i/8))
  z=1.977+profile[i]*[0,.62,1,.53,0][j]
  v.append((x,y,z))
for i in range(8):
 for j in range(4):
  a=i*5+j
  f.extend([(a,a+5,a+6),(a,a+6,a+1)] if (i+j)%2 else [(a,a+5,a+1),(a+1,a+5,a+6)])
boundary=[i*5 for i in range(9)]+[40+j for j in range(1,5)]+[i*5+4 for i in range(7,-1,-1)]+[j for j in range(3,0,-1)]
f.append(tuple(reversed(boundary)))
ice=mesh('Glacier / crevassed asymmetric ridge',v,f,mat);normals(ice)
ca=ice.data.color_attributes.new(name='Ice depth',type='FLOAT_COLOR',domain='CORNER')
for poly in ice.data.polygons:
 for li in poly.loop_indices:
  z=ice.data.vertices[ice.data.loops[li].vertex_index].co.z;t=max(0,min(1,(z-1.977)/.29));ca.data[li].color=(.36+.27*t,.69+.19*t,.83+.13*t,1)
for node in mat.node_tree.nodes:
 if node.type=='VERTEX_COLOR':node.layer_name=ca.name

slab=bpy.data.objects['Lid / polished slab'];obsidian=slab.data.materials[0];bpy.data.objects.remove(slab,do_unlink=True)
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,1.828));slab=bpy.context.object;slab.name='Lid / polished slab';slab.dimensions=(3.72,2.38,.30);select(slab);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);slab.data.materials.append(obsidian);bevel=slab.modifiers.new('Original perimeter bevel','BEVEL');bevel.width=.055;bevel.segments=3;bpy.ops.object.modifier_apply(modifier=bevel.name);parent(slab)
for o in list(bpy.data.objects):
 if o.name.startswith('River /'):bpy.data.objects.remove(o,do_unlink=True)
blue=bpy.data.materials['River / deep glacial blue'];edge=bpy.data.materials['River / icy bank reflections']
path=[]
for i in range(81):
 t=i/80;x=-1.89+3.14*t;y=-.22+.90*t+.045*math.sin(t*math.pi*4);w=.063+.022*math.sin(t*8+.5)**2+.014*math.sin(t*15)**2;path.append((x,y,w))
v=[]
for z in [1.94,2.06]:
 for x,y,w in path:v.extend([(x,y-w,z),(x,y+w,z)])
n=2*len(path);f=[]
for i in range(len(path)-1):
 a=2*i;f.extend([(a,a+2,a+3,a+1),(n+a+1,n+a+3,n+a+2,n+a),(a,n+a,n+a+2,a+2),(a+1,a+3,n+a+3,n+a+1)])
f.extend([(0,1,n+1,n),(n-2,2*n-2,2*n-1,n-1)])
cut=mesh('temporary new channel',v,f,blue);normals(cut);select(slab);mod=slab.modifiers.new('Relocated continuous inset','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
fractions=[-1,-.90,-.60,.60,.90,1];v=[]
for x,y,w in path:
 for a in fractions:v.append((x,y+w*a,1.966+.009*abs(a)**4+.016*max(0,min(1,(x-.65)/.25))))
f=[]
for i in range(len(path)-1):
 for j in range(5):a=i*6+j;f.extend([(a,a+6,a+7),(a,a+7,a+1)])
o=mesh('River / depth graded connected channel',v,f,blue);o.data.materials.append(edge)
for p in o.data.polygons:p.material_index=1 if (p.index//2)%5 in [0,4] else 0
x,y,w=path[0];v=[]
for level,(z,ww,yy) in enumerate([(1.966,w,y),(1.91,w*.90,y+.012),(1.80,w*.67,y+.025),(1.74,w*.33,y+.03)]):
 for a in fractions:v.append((x if level==0 else -1.875,yy+ww*a,z+(.009*abs(a)**4 if level==0 else 0)))
f=[]
for i in range(3):
 for j in range(5):a=i*6+j;f.extend([(a,a+6,a+7),(a,a+7,a+1)])
o=mesh('River / connected side cascade',v,f,blue);o.data.materials.append(edge)
for p in o.data.polygons:p.material_index=1 if (p.index//2)%5 in [0,4] else 0
bm=bmesh.new();bm.from_mesh(slab.data);bmesh.ops.dissolve_degenerate(bm,dist=.000002,edges=list(bm.edges));bmesh.ops.triangulate(bm,faces=list(bm.faces));bad=[f for f in bm.faces if f.calc_area()<1e-9]
if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
bm.to_mesh(slab.data);bm.free()
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'iceland.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'iceland.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
# Blender 5.2 simplification drops the disconnected thickness setting and multiply
# factor. Serialize those exact saved-source node inputs, without altering buffer bytes.
import struct
raw=(R/'iceland.glb').read_bytes();jn=struct.unpack_from('<I',raw,12)[0];doc=json.loads(raw[20:20+jn]);tail=raw[20+jn:]
for mat in doc['materials']:
 source=bpy.data.materials[mat['name']]
 if mat['name'].startswith('Basalt /'):
  factor=next(n for n in source.node_tree.nodes if n.type=='MIX_RGB').inputs[2].default_value
  mat['pbrMetallicRoughness']['baseColorFactor']=list(factor)
 if mat['name']=='Glacier / blue depth':
  nt=source.node_tree;absorb=next(n for n in nt.nodes if n.type=='VOLUME_ABSORPTION');thick=next(n for n in nt.nodes if n.type=='GROUP' and 'Thickness' in n.inputs).inputs['Thickness'].default_value
  mat['extensions']['KHR_materials_volume']={'thicknessFactor':thick,'attenuationColor':list(absorb.inputs['Color'].default_value)[:3],'attenuationDistance':1/absorb.inputs['Density'].default_value}
if 'KHR_materials_volume' not in doc['extensionsUsed']:doc['extensionsUsed'].append('KHR_materials_volume')
payload=json.dumps(doc,separators=(',',':')).encode();payload+=b' '*((-len(payload))%4);(R/'iceland.glb').write_bytes(struct.pack('<III',0x46546c67,2,20+len(payload)+len(tail))+struct.pack('<II',len(payload),0x4e4f534a)+payload+tail)

(R/'authorship.json').write_text(json.dumps({'base':'immutable v9','axes':{'front_latch_y':-1.29,'rear_hinge_y':1.32,'head_on_right':'+X','back':'+Y'},'glacier_bounds':[[.86,.38,1.977],[1.65,.98,2.267]],'river_centerline':path,'scope':'only glacier, river and rebuilt original-dimension cut slab; materials and camera unchanged'},indent=2))
bpy.context.scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('V10_AUTHORED')
