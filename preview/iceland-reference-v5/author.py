"""Reference-led structural reconstruction. Run with Blender. Prior versions remain immutable.
Uses bundled baseline helper/studio source only; no external authoring inputs required.
"""
from pathlib import Path
BASE=(Path(__file__).parent/'baseline_author.py').read_text()
exec(BASE[:BASE.index('# Irregular vertical')])
random.seed(305)
obsidian.name='Polished black obsidian'
p=obsidian.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.002,.003,.004,1);p.inputs['Roughness'].default_value=.13;p.inputs['Metallic'].default_value=.22
brass.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.48,.30,.105,1)
blue.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.015,.25,.46,1)
blue.node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=.12
mossm=[material('Moss / sheltered olive '+str(i),(.085+i*.018,.12+i*.023,.018+i*.006),0,.94) for i in range(4)]
ice=material('Glacier translucent cyan',(.17,.58,.72),.03,.19)
ip=ice.node_tree.nodes.get('Principled BSDF');ip.inputs['Transmission Weight'].default_value=.36;ip.inputs['IOR'].default_value=1.31
frost=material('Glacier frosted ridges',(.50,.76,.83),0,.35)
def mesh(name,vs,fs,mat,parent=None):
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);return finish(o,name,mat,parent)
# Segment each column at a different slanted broken stratum. Deliberately omitted
# outer wedges are cavities, not paint: liner remains continuous behind them.
def block(side,c,w,z0,z1,idx):
 recess=random.uniform(.012,.12); n=7
 # 7-sided jagged section; forward shoulder chipped independently at each height.
 vs=[]
 outline=[(-.50,-.04),(-.46,.09),(-.22,.18),(.30,.17),(.50,.07),(.46,-.04),(0,-.075)]
 for level,z in enumerate([z0,(z0+z1)*.5,z1]):
  for j,(a,b) in enumerate(outline):
   a=a*w+random.uniform(-.022,.022); b=b-recess
   if level==1 and j in (2,3) and idx%3==0:b-=.11
   zz=z+random.uniform(-.035,.035)
   if side in ('front','rear'): pos=(c+a,(-1 if side=='front' else 1)*(1.09+b),zz)
   else:pos=((-1 if side=='left' else 1)*(1.67+b),c+a,zz)
   vs.append(pos)
 fs=[tuple(reversed(range(n))),tuple(range(2*n,3*n))]
 for k in range(2):
  for j in range(n):fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 o=mesh('Basalt fracture / '+side,vs,fs,stones[idx%5]);o['recess']=recess
 # Moss grows across sheltered broken ledges and down deep joins, not flat faces.
 if idx%3!=1:
  for q in range(random.randint(3,6)):
   a=c+random.uniform(-w*.4,w*.4); h=z0+random.uniform(-.005,.07)
   d=1.17 if side in ('front','rear') else 1.75
   loc=(a,(-1 if side=='front' else 1)*d,h) if side in ('front','rear') else ((-1 if side=='left' else 1)*d,a,h)
   bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=1,location=loc);m=bpy.context.object;m.scale=(random.uniform(.025,.075),random.uniform(.025,.055),random.uniform(.025,.065));bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);finish(m,'Sheltered moss / cavity',mossm[idx%4])
for side,span,count in [('front',3.46,11),('rear',3.46,11),('left',1.95,7),('right',1.95,7)]:
 widths=[random.uniform(.7,1.4) for _ in range(count)];widths=[w/sum(widths)*span for w in widths];at=-span/2
 for i,w in enumerate(widths):
  c=at+w/2;at+=w;cut=random.uniform(.48,.95)
  block(side,c,w,.08,cut-.045,i*2);block(side,c,w,cut+.035,1.39,i*2+1)
# Original motion anchors; every lid ornament shares the same parent.
lid=empty('Lid_Hinge',(0,1.32,1.5));lid['mechanism']='negative X 105 degrees; original staged latch'
slab=cube('Lid / polished slab',(0,0,1.66),(3.72,2.38,.30),obsidian,.055,lid)
cube('Lid / recessed inner face',(0,0,1.509),(3.31,1.98,.018),inside,.005,lid)
# Smooth organically meandering ribbon, boolean-cut into actual obsidian surface.
path=[]
for i in range(45):
 t=i/44;x=-1.88+2.5*t;y=-.22+.86*t+.085*math.sin(t*math.pi*4);width=.043+.025*math.sin(t*9)**2+.018*t
 path.append((x,y,width))
def ribbon(name,zlo,zhi,mat,parent):
 vs=[]
 for z in [zlo,zhi]:
  for x,y,w in path:vs.extend([(x,y-w,z),(x,y+w,z)])
 n=len(path)*2;fs=[]
 for i in range(len(path)-1):
  a=i*2;fs.extend([(a,a+2,a+3,a+1),(n+a+1,n+a+3,n+a+2,n+a),(a,n+a,n+a+2,a+2),(a+1,a+3,n+a+3,n+a+1)])
 fs.extend([(0,1,n+1,n),(n-2,2*n-2,2*n-1,n-1)])
 o=mesh(name,vs,fs,mat,parent)
 # recalc outward normals for robust boolean operand
 bpy.context.view_layer.objects.active=o;bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT');return o
cutter=ribbon('channel cutter',1.777,1.88,blue,None)
bpy.context.view_layer.objects.active=slab
for mod in list(slab.modifiers):bpy.ops.object.modifier_apply(modifier=mod.name)
bo=slab.modifiers.new('Real shallow river inlay channel','BOOLEAN');bo.operation='DIFFERENCE';bo.solver='EXACT';bo.object=cutter;bpy.ops.object.modifier_apply(modifier=bo.name)
parts.remove(cutter);bpy.data.objects.remove(cutter,do_unlink=True)
ribbon('River / inset organic blue',1.779,1.799,blue,lid)
# Descending ice is contained above body seam and follows left fascia.
mesh('River / left edge cascade',[(-1.863,-.29,1.80),(-1.863,-.16,1.80),(-1.87,-.13,1.62),(-1.87,-.18,1.56),(-1.87,-.22,1.64),(-1.87,-.27,1.57),(-1.87,-.31,1.67)],[(0,1,2),(0,2,4),(2,3,4),(0,4,6),(4,5,6)],blue,lid)
# Low asymmetric glacier ridge, triangulated crystalline terrain rather than cone trees.
vs=[];nx=15;ny=9
for j in range(ny):
 for i in range(nx):
  x=-.24+i*.087;y=.32+j*.072
  edge=min(i,nx-1-i,j,ny-1-j)
  h=max(.0,.28*math.exp(-((x-.43)**2/.028+(y-.64)**2/.023)),.20*math.exp(-((x-.10)**2/.018+(y-.58)**2/.02)),.16*math.exp(-((x-.72)**2/.025+(y-.68)**2/.013)))
  h=h+random.uniform(-.025,.025) if edge else .002
  # Meandering shelf silhouette, not rectangular terrain tile.
  y+=.055*math.sin(i*1.9)*(1 if edge==0 else .25)
  x+=.04*math.sin(j*2.1)*(1 if edge==0 else .25)
  vs.append((x+random.uniform(-.017,.017),y+random.uniform(-.012,.012),1.813+max(.002,h)))
fs=[]
for j in range(ny-1):
 for i in range(nx-1):
  a=j*nx+i;fs.extend([(a,a+1,a+nx),(a+1,a+nx+1,a+nx)])
g=mesh('Glacier / asymmetric raised ice ridge',vs,fs,ice,lid);g.data.materials.append(frost)
for f in g.data.polygons:
 if f.center.z>2.0 or random.random()<.16:f.material_index=1
# Shaped sheet guards with broad arms and shorter stepped tongues on both faces.
# Each guard is three real polygon plates folded round an edge, not square pads.
def sheet(name,poly,axis,constant,thick,mat,parent):
 vs=[]
 for d in [constant-thick/2,constant+thick/2]:
  for a,b in poly:vs.append((a,b,d) if axis=='z' else ((a,d,b) if axis=='y' else (d,a,b)))
 n=len(poly);fs=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
 o=mesh(name,vs,fs,mat,parent);mod=o.modifiers.new('Worn rolled brass edge','BEVEL');mod.width=.009;mod.segments=2;o.modifiers.new('Plate normals','WEIGHTED_NORMAL');return o
for sx in [-1,1]:
 for sy in [-1,1]:
  for upper in [True,False]:
   z=1.827 if upper else .058; par=lid if upper else None
   poly=[(sx*(1.86-a),sy*(1.19-b)) for a,b in [(0,0),(.47,0),(.47,.12),(.20,.12),(.20,.22),(.12,.22),(.12,.40),(0,.40)]]
   sheet('Corner strap / folded top' if upper else 'Corner strap / lower sole',poly,'z',z,.023,brass,par)
   # upper: broad top arm and stepped descending tongue; bottom inverted.
   outline=[(0,0),(.47,0),(.47,.095),(.23,.095),(.23,.18),(.13,.18),(.13,.26),(0,.26)]
   for axis in ['y','x']:
    outer=1.86 if axis=='y' else 1.19;sign=sx if axis=='y' else sy
    pp=[(sign*(outer-a),z+(-b if upper else b)) for a,b in outline]
    sheet('Corner strap / wrapped '+axis,pp,axis,(sy*1.198 if axis=='y' else sx*1.868),.025,brass,par)
    for a,b in [(.35,.05),(.075,.18)]:
     zz=z+(-b if upper else b)
     loc=(sx*(1.86-a),sy*1.219,zz) if axis=='y' else (sx*1.889,sy*(1.19-a),zz)
     cyl('Strap rivet / domed',loc,.025,.015,brass,(math.pi/2,0,0) if axis=='y' else (0,math.pi/2,0),par,12)
# Reuse working hinge/latch choreography and attachment components.
exec(BASE[BASE.index('for x in [-1.13,1.13]:'):BASE.index("cyl('Medallion / inset'")])
# Physical attachment bridge from each rear wall to the bearing mount.
for x in [-1.13,1.13]:
 cube('Hinge / body attachment bridge',(x,1.14,1.21),(.26,.25,.09),brass,.012)
 cube('Hinge / bearing mounting stem',(x,1.29,1.42),(.22,.06,.09),brass,.01)
# Plain reference medallion and side ring; no invented authenticity symbol.
for x in [-1.84,1.84]:
 for y in [-.18,.18]:cyl('Ring / mounting stud',(x,y,.94),.065,.06,brass,(0,math.pi/2,0))
 pts=[]
 for i in range(33):
  a=math.tau*i/32;pts.append((x+(-.05 if x<0 else .05),.19*math.cos(a),.83+.10*math.sin(a)))
 line('Ring / side handle',pts,.026,brass)
# Reference-style ears/fasteners on front keeper; all below moving path.
for x in [-.21,.21]:
 cube('Clasp / keeper mounting ear',(x,-1.29,1.12),(.12,.07,.12),brass,.018)
 cyl('Clasp / keeper screw',(x,-1.335,1.12),.024,.012,obsidian,(math.pi/2,0,0),vertices=12)
exec(BASE[BASE.index('# Lighting and camera'):BASE.index('# Save independent')])
cam.location=(-5,-7,4.0);cam.rotation_euler=(Vector((0,0,1.0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=5.4
scene.render.resolution_x=1200;scene.render.resolution_y=1000;scene.cycles.samples=32
bpy.data.objects['Studio / gold rim'].data.energy=180
bpy.data.objects['Studio / gold rim'].location=(4,4,5)
# Compact portable PBR microstructure; visible large breaks remain geometry.
images={k:bpy.data.images.load(str(ROOT/'textures'/f)) for k,f in [('color','stone-color.jpg'),('normal','stone-normal.png'),('rough','stone-rough.jpg')]}
for k,img in images.items():
 if k!='color':img.colorspace_settings.name='Non-Color'
 img.pack()
for mat in stones:
 nt=mat.node_tree;p=nt.nodes.get('Principled BSDF')
 for k in images:
  tex=nt.nodes.new('ShaderNodeTexImage');tex.image=images[k]
  if k=='normal':
   normal=nt.nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.28;nt.links.new(tex.outputs['Color'],normal.inputs['Color']);nt.links.new(normal.outputs['Normal'],p.inputs['Normal'])
  else:nt.links.new(tex.outputs['Color'],p.inputs['Base Color' if k=='color' else 'Roughness'])
for o in parts:
 if o.name.startswith('Basalt fracture'):
  uv=o.data.uv_layers.new(name='Stone planar')
  for face in o.data.polygons:
   axis=max(range(3),key=lambda a:abs(face.normal[a]));axes=[a for a in range(3) if a!=axis]
   for li in face.loop_indices:
    co=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]]*2,co[axes[1]]*2)
 if o.name.startswith('Sheltered moss'):
  for face in o.data.polygons:face.use_smooth=True
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'iceland.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in parts+[lid,latch]:o.select_set(True)
bpy.context.view_layer.objects.active=lid
bpy.ops.export_scene.gltf(filepath=str(ROOT/'iceland.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(ROOT/'poster.png');bpy.ops.render.render(write_still=True)
print('V5_STRUCTURAL_EXPORT_COMPLETE',len(parts))
