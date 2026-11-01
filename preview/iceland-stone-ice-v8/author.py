"""Bounded structural refinement of actual packed v7 source; seeded procedural art."""
from pathlib import Path
import bpy,bmesh,random,math,json
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(R/'approved-v7.blend'),use_scripts=False)
rng=random.Random(808);bpy.context.view_layer.update();lid=bpy.data.objects['Lid_Hinge']
def select(o):
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
def normals(o):
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
def mesh(name,vs,fs,mat,parent=None):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(mat)
 if parent:
  bpy.context.view_layer.update();mw=o.matrix_world.copy();o.parent=parent;o.matrix_world=mw
 return o
def material(name,col,rough=.4,trans=0):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*col,1);p.inputs['Roughness'].default_value=rough;p.inputs['Transmission Weight'].default_value=trans;p.inputs['IOR'].default_value=1.31;return m
# Real missing edge wedges on each separate column, never cutting structural liner.
records=[]
for o in [x for x in bpy.data.objects if x.name.startswith('Basalt fracture')]:
 side=o.name.split('/ ')[1].split('.')[0];axis=1 if side in ['front','rear'] else 0;tan=1-axis;sgn=-1 if side in ['front','left'] else 1
 normals(o);world=[o.matrix_world@v.co for v in o.data.vertices];lo=[min(v[a] for v in world) for a in range(3)];hi=[max(v[a] for v in world) for a in range(3)];outer=max(v[axis]*sgn for v in world)
 before=len(o.data.vertices);depths=[]
 for k in range(rng.choice([1,2,2,3])):
  depth=rng.uniform(.065,.155);width=rng.uniform(.095,.205);height=rng.uniform(.065,.18)
  if k==0 and len(records)%7==2:
   depth=rng.uniform(.19,.235);width=rng.uniform(.28,.36);height=rng.uniform(.24,.33)
  # Cuts enter from a lateral shoulder or stratum edge: no isolated punched holes.
  edge=(-1 if (k+len(records))%2 else 1);c=[0,0,0];c[tan]=(lo[tan] if edge<0 else hi[tan])+edge*width*.06;c[axis]=sgn*(outer+.055-depth*.5);c[2]=rng.uniform(lo[2]+.05,hi[2]-.05)
  # Irregular tapered fracture prism: angled overlapping break planes, no rectangular slots.
  poly=[(-.61,-.13),(-.23,-.61),(.43,-.31),(.59,.24),(-.18,.58)];cv=[]
  for layer,d in enumerate([-depth*.5,.17]):
   for a,b in poly:
    co=c.copy();co[tan]+=a*width*(.68 if layer==0 else 1.25);co[2]+=b*height*(.80 if layer==0 else 1.15);co[axis]+=sgn*d;cv.append(co)
  cf=[(4,3,2,1,0),(5,6,7,8,9)]+[(j,(j+1)%5,(j+1)%5+5,j+5) for j in range(5)]
  cut=mesh('temporary fracture cutter',cv,cf,o.data.materials[0]);normals(cut)
  select(o);mod=o.modifiers.new('Missing weathered corner','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cut;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True);depths.append(depth)
 # Keep actual hard break planes; portable face UVs at fine grain scale.
 normals(o);uv=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone fracture planar')
 for f in o.data.polygons:
  a=max(range(3),key=lambda a:abs(f.normal[a]));axes=[x for x in range(3) if x!=a]
  for li in f.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]]*1.35+len(records)*.131,co[axes[1]]*1.35)
 o['notch_count']=len(depths);o['max_notch_depth']=max(depths)
 records.append({'name':o.name,'depths':depths,'vertices_before':before,'vertices_after':len(o.data.vertices)})
images={}
for k in ['color','normal','rough']:
 im=bpy.data.images.load(str(R/'textures'/('stone-'+k+'.jpg')));im.colorspace_settings.name='sRGB' if k=='color' else 'Non-Color';im.pack();images[k]=im
for mat in bpy.data.materials:
 if not mat.name.startswith('Basalt /'):continue
 nt=mat.node_tree
 for node in nt.nodes:
  if node.type=='TEX_IMAGE':
   key='normal' if 'normal' in node.image.name else ('rough' if 'rough' in node.image.name else 'color');node.image=images[key]
  if node.type=='NORMAL_MAP':node.inputs['Strength'].default_value=.62
# Re-seat pre-existing moss onto the new stone. Leave pattern/colors/mesh count unchanged.
vs=[];fs=[]
for o in bpy.data.objects:
 if o.type=='MESH' and o.name.startswith(('Basalt fracture','Interior wall')):
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();off=len(vs);vs.extend([o.matrix_world@v.co for v in me.vertices]);fs.extend([tuple(off+i for i in f.vertices) for f in me.polygons]);ev.to_mesh_clear()
tree=BVHTree.FromPolygons(vs,fs)
for o in bpy.data.objects:
 if not o.name.startswith('Sheltered moss v7'):continue
 inv=o.matrix_world.inverted()
 for v in o.data.vertices:
  co=o.matrix_world@v.co;axis=0 if abs(co.x)>1.55 else 1;sgn=1 if co[axis]>0 else -1;origin=co.copy();origin[axis]=sgn*3;direction=Vector((0,0,0));direction[axis]=-sgn;hit,_,_,_=tree.ray_cast(origin,direction,4)
  if hit is not None and co[axis]*sgn>hit[axis]*sgn+.035:co[axis]=hit[axis]+sgn*.012;v.co=inv@co
# Replace only ice/water, same overall route and rear formation region.
for o in list(bpy.data.objects):
 if o.name.startswith(('River /','Glacier /')):bpy.data.objects.remove(o,do_unlink=True)
blue=material('River / deep glacial blue',(.018,.19,.29),.115,.28)
edge=material('River / icy bank reflections',(.16,.46,.55),.22,.24)
ice=material('Glacier / blue depth',(.105,.38,.52),.16,.48)
frost=material('Glacier / snow ridge',(.55,.73,.78),.32,.14)
mid=material('Glacier / weathered ice face',(.24,.51,.64),.22,.40)
path=[]
for i in range(65):
 t=i/64;x=-1.89+2.51*t;y=-.22+.86*t+.085*math.sin(t*math.pi*4);w=.081+.035*math.sin(t*8+.5)**2+.028*math.sin(t*15)**2+.012*t;path.append((x,y,w))
def ribbon(name,low,high,mat):
 v=[]
 for z in [low,high]:
  for x,y,w in path:v.extend([(x,y-w,z),(x,y+w,z)])
 n=2*len(path);f=[]
 for i in range(len(path)-1):
  a=2*i;f.extend([(a,a+2,a+3,a+1),(n+a+1,n+a+3,n+a+2,n+a),(a,n+a,n+a+2,a+2),(a+1,a+3,n+a+3,n+a+1)])
 f.extend([(0,1,n+1,n),(n-2,2*n-2,2*n-1,n-1)])
 o=mesh(name,v,f,mat,lid);normals(o);return o
cutter=ribbon('temporary river cutter',1.94,2.06,blue);slab=bpy.data.objects['Lid / polished slab'];select(slab)
for mod in list(slab.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
mod=slab.modifiers.new('Widen natural inset river','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter;bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cutter,do_unlink=True)
# Cross-section bands are real continuous strips, dark center and narrow pale banks.
v=[];fractions=[-1,-.90,-.60,.60,.90,1]
for i,(x,y,w) in enumerate(path):
 for f in fractions:v.append((x,y+w*f,1.966+(.009*abs(f)**4)))
f=[]
for i in range(len(path)-1):
 for j in range(5):a=i*6+j;f.extend([(a,a+6,a+7),(a,a+7,a+1)])
o=mesh('River / depth graded connected channel',v,f,blue,lid);o.data.materials.append(edge)
for p in o.data.polygons:p.material_index=1 if (p.index//2)%5 in [0,4] else 0
# Same edge and above-body termination, with narrow center and irregular lip.
x,y,w=path[0];v=[]
for level,(z,ww,yy) in enumerate([(1.966,w,y),(1.91,w*.90,y+.012),(1.80,w*.67,y+.025),(1.74,w*.33,y+.03)]):
 for f in fractions:v.append((x if level==0 else -1.875,yy+ww*f,z+(.009*abs(f)**4 if level==0 else 0)))
f=[]
for i in range(3):
 for j in range(5):a=i*6+j;f.extend([(a,a+6,a+7),(a,a+7,a+1)])
o=mesh('River / connected side cascade',v,f,blue,lid);o.data.materials.append(edge)
for p in o.data.polygons:p.material_index=1 if (p.index//2)%5 in [0,4] else 0
# Continuous asymmetric glacier with a low apron and three diagonal deep crevasses.
v=[];nx=43;ny=23
for j in range(ny):
 for i in range(nx):
  u=i/(nx-1);t=j/(ny-1);x=-.26+1.27*u;y=.29+.64*t;boundary=min(i,nx-1-i,j,ny-1-j)
  peaks=[(.48,.69,.36,.10,.14),(.11,.61,.23,.12,.12),(.77,.71,.20,.10,.10),(.32,.52,.14,.12,.12)]
  spine=.62+.065*math.sin(x*5)+.022*math.sin(x*19)
  along=.13+.19*math.exp(-((x-.46)/.13)**2)+.09*math.exp(-((x-.09)/.12)**2)
  h=.025+along*max(0,1-abs(y-spine)/(.21 if y<spine else .14))
  # Connected serrated ridge and broad thick terminus, not isolated cones.
  h*=.90+.10*math.sin(x*61+y*17);h+=rng.uniform(-.007,.010)
  for cx,cy in [(.24,.61),(.59,.69),(.83,.72)]:
   line=cx+.35*(y-cy);dist=abs(x-line)
   if dist<.018 and abs(y-cy)<.15:h*=.26+dist/.018*.34
  h=.012+max(.009,h)*min(1,boundary/2)
  x+=.021*math.sin(j*2.1)*(1 if boundary==0 else .12);y+=.027*math.sin(i*1.3)*(1 if boundary==0 else .12)
  v.append((x,y,1.982+h))
f=[]
for j in range(ny-1):
 for i in range(nx-1):
  a=j*nx+i;f.extend([(a,a+1,a+nx),(a+1,a+nx+1,a+nx)])
perimeter=list(range(nx))+[j*nx+nx-1 for j in range(1,ny)]+[(ny-1)*nx+i for i in range(nx-2,-1,-1)]+[j*nx for j in range(ny-2,0,-1)]
for index,a in enumerate(perimeter):
 b=perimeter[(index+1)%len(perimeter)];k=len(v);v.extend([(v[a][0],v[a][1],1.977),(v[b][0],v[b][1],1.977)]);f.extend([(a,k,k+1),(a,k+1,b)])
o=mesh('Glacier / crevassed asymmetric ridge',v,f,ice,lid);o['crevasse_count']=3
col=o.data.color_attributes.new(name='Ice depth to frost',type='FLOAT_COLOR',domain='CORNER')
for p in o.data.polygons:
 for li in p.loop_indices:
  co=o.data.vertices[o.data.loops[li].vertex_index].co;t=max(0,min(1,(co.z-2.035)/.22))
  col.data[li].color=(.12+.53*t,.39+.39*t,.53+.29*t,1)
nt=ice.node_tree;vc=nt.nodes.new('ShaderNodeVertexColor');vc.layer_name=col.name;nt.links.new(vc.outputs['Color'],nt.nodes.get('Principled BSDF').inputs['Base Color'])
# Boolean triangulation cleanup before export, not a relaxed browser threshold.
for ob in bpy.data.objects:
 if ob.type!='MESH' or not ob.name.startswith(('Basalt fracture','Lid / polished slab')):continue
 bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.dissolve_degenerate(bm,dist=0.000002,edges=list(bm.edges));bmesh.ops.triangulate(bm,faces=list(bm.faces))
 bad=[f for f in bm.faces if f.calc_area()<1e-9]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
 bm.to_mesh(ob.data);bm.free()
# Source stays packed and named; all hardware, liner, motion pivots and studio unchanged.
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'iceland.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid
bpy.ops.export_scene.gltf(filepath=str(R/'iceland.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
(R/'authorship.json').write_text(json.dumps({'seed':808,'fractures':records,'river_sections':len(path),'river_width_range':[min(x[2]*2 for x in path),max(x[2]*2 for x in path)],'glacier_grid':[nx,ny],'notes':'Wedge-cut exterior cladding; unchanged continuous liner and hardware; generated shared 512 maps; re-seated existing moss'},indent=2))
bpy.context.scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('V8_AUTHORED')
