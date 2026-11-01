"""Four scoped corrections; reopen v8, retain stone geometry and articulation."""
import bpy,bmesh,math,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'approved-v8.blend'),use_scripts=False)
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
# Keep actual grain maps; portable multiplication factor, not exposure changes.
for m in bpy.data.materials:
 if not m.name.startswith('Basalt /'):continue
 nt=m.node_tree;p=nt.nodes.get('Principled BSDF');sock=p.inputs['Base Color'];old=sock.links[0].from_socket
 mul=nt.nodes.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=(.28,.28,.28,1);nt.links.new(old,mul.inputs[1]);nt.links.new(mul.outputs[0],sock)
# Compress the existing connected serrated formation, relocate near far screen-right corner.
ice=bpy.data.objects['Glacier / crevassed asymmetric ridge'];inv=ice.matrix_world.inverted()
for v in ice.data.vertices:
 co=ice.matrix_world@v.co;co.x=1.12+co.x*.53;co.y=co.y*.75-1.25;v.co=inv@co
for ca in ice.data.color_attributes:
 for c in ca.data:
  t=max(0,min(1,(c.color[0]-.12)/.53));c.color=(.36+.27*t,.69+.19*t,.83+.13*t,1)
bm=bmesh.new();bm.from_mesh(ice.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=0.000001);bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ice.data);bm.free()
for poly in ice.data.polygons:poly.use_smooth=True
m=ice.data.materials[0];nt=m.node_tree;p=nt.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=.97;p.inputs['Roughness'].default_value=.035;p.inputs['IOR'].default_value=1.31
volume=nt.nodes.new('ShaderNodeVolumeAbsorption');volume.inputs['Color'].default_value=(.58,.84,.96,1);volume.inputs['Density'].default_value=1.6;nt.links.new(volume.outputs['Volume'],nt.nodes.get('Material Output').inputs['Volume'])
group=bpy.data.node_groups.new('glTF Material Output','ShaderNodeTree');group.interface.new_socket(name='Thickness',in_out='INPUT',socket_type='NodeSocketFloat').default_value=.18;node=nt.nodes.new('ShaderNodeGroup');node.node_tree=group;node.inputs['Thickness'].default_value=.18
# Remove the old river in full; reconstruct only slab with identical outer bounds/bevel.
slab=bpy.data.objects['Lid / polished slab'];obsidian=slab.data.materials[0];bpy.data.objects.remove(slab,do_unlink=True)
bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,1.828));slab=bpy.context.object;slab.name='Lid / polished slab';slab.dimensions=(3.72,2.38,.30);select(slab);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);slab.data.materials.append(obsidian);bevel=slab.modifiers.new('Original perimeter bevel','BEVEL');bevel.width=.055;bevel.segments=3;bpy.ops.object.modifier_apply(modifier=bevel.name);parent(slab)
for o in list(bpy.data.objects):
 if o.name.startswith('River /'):bpy.data.objects.remove(o,do_unlink=True)
blue=bpy.data.materials['River / deep glacial blue'];edge=bpy.data.materials['River / icy bank reflections']
path=[]
for i in range(81):
 t=i/80;x=-1.89+3.19*t;y=-.22-.53*t+.075*math.sin(t*math.pi*4);w=.063+.022*math.sin(t*8+.5)**2+.014*math.sin(t*15)**2;path.append((x,y,w))
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
 for a in fractions:v.append((x,y+w*a,1.966+.009*abs(a)**4))
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
# Enlarge existing shaped corner plates inward, not their pivot/lowest extent.
wraps=[]
for o in bpy.data.objects:
 if o.parent!=lid or not o.name.startswith('Corner strap /'):continue
 inv=o.matrix_world.inverted();world=[o.matrix_world@v.co for v in o.data.vertices];sx=1 if sum(v.x for v in world)>0 else -1;sy=1 if sum(v.y for v in world)>0 else -1
 for v,co in zip(o.data.vertices,world):
  if o.name.startswith('Corner strap / folded top'):co.x=sx*(1.86-(1.86-sx*co.x)*1.20);co.y=sy*(1.19-(1.19-sy*co.y)*1.24);co.z+=.006
  elif o.name.startswith('Corner strap / wrapped x'):co.y=sy*(1.19-(1.19-sy*co.y)*1.20);co.x+=sx*.004
  else:co.x=sx*(1.86-(1.86-sx*co.x)*1.20);co.y+=sy*.004
  v.co=inv@co
 wraps.append(o.name)
# Raised top fasteners, shared low-poly geometry: four corner pairs, not extra pivots.
brass=bpy.data.objects['Corner strap / folded top'].data.materials[0]
for sx in [-1,1]:
 for sy in [-1,1]:
  for j,(a,b) in enumerate([(.10,.095),(.40,.065)]):
   bpy.ops.mesh.primitive_uv_sphere_add(segments=10,ring_count=5,radius=1,location=(sx*(1.86-a),sy*(1.19-b),2.019));o=bpy.context.object;o.name=f'Corner cap / top rivet {sx} {sy} {j}';o.scale=(.033,.033,.014);o.data.materials.append(brass);parent(o)
# Clean only recreated slab Boolean numerical crumbs, preserving rock completely.
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
(R/'authorship.json').write_text(json.dumps({'base':'immutable v8','rock_color_multiplier':.28,'glacier_x_transform':[.53,1.12],'glacier_y_transform':[.75,-1.25],'river_centerline':path,'wraps':wraps,'glass':{'transmission':.97,'roughness':.035,'ior':1.31,'thickness':.18},'front_caps':'decorative protectors; no extra pivot','rear_hinges':'original mechanical coaxial bearings and attachment bridges retained'},indent=2))
bpy.context.scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('V9_AUTHORED')
