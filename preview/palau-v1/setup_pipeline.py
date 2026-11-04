"""Copy read-only pilot mechanics; create only Palau-local sources."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','motion.mjs','THREE-LICENSE.txt','package.json']:
 shutil.copyfile(S/name,R/name)
for name in ['viewer.js','template.html','verify_source.py','verify_parity.py','verify_browser.py','build.py']:
 s=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','palau-v1').replace('japan.glb','palau.glb').replace('japan.blend','palau.blend').replace('Japan','Palau').replace('JAPAN','PALAU').replace('Cedar & Moss','Rock Islands & Lagoon').replace('Cedar and Moss','Rock Islands and Lagoon').replace('Yakushima cedar. Mossed granite. Quiet brass.','Forested limestone. Turquoise lagoon. Satin brass.').replace('inspired by the original Palau concept','inspired by Palau’s Rock Islands landscape')
 if name=='viewer.js':
  s=s.replace("camera.position.set(-5,3.7,7)","camera.position.set(-5,4.8,7)")
  s=s.replace("bindAction(open,()=>{target=target?0:1;", "function snap(){if(!reduced.matches)return;progress=target;const p=pose(progress);lid.rotation.x=p.lid;latch.rotation.x=p.latch;window.pilot.progress=progress;window.pilot.lid=p.lid;window.pilot.latch=p.latch;}\n bindAction(open,()=>{target=target?0:1;snap();")
  s=s.replace("controls.reset();open.textContent", "controls.reset();snap();open.textContent")
 (R/name).write_text(s,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n')
# Preserve vetted construction helpers but replace all cedar-specific skins/terrain.
s=(S/'author.py').read_text(encoding='utf8')
head=s[:s.index('wood=mat(')]
helpers=s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
helpers=helpers[:helpers.index('def cube(')].replace("layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Oriented grain')","layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone planar UV')")+helpers[helpers.index('def cube('):]
# Isotropic dominant-normal planar mapping avoids inherited longitudinal wood mapping.
a=helpers.index("   u=co.y");b=helpers.index('def cube(')
helpers=helpers[:a]+'''   normal=p.normal
   if abs(normal.z)>.7:u,v=co.x,co.y
   elif abs(normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u*.5+.5,v*.5+.5)
'''+helpers[b:]
stone=s[s.index('def stone('):s.index("for sx in [-1,1]:\n for sy in [-1,1]:stone")]
metal=s[s.index('# Medallion is solid'):s.index('# Clean obsolete')]
cleanup=s[s.index('# Clean obsolete'):s.index('# Studio rendering')]
(R/'author.py').write_text(head.replace('Reference-led Japan pilot','Brief-led Palau pilot')+'''limestone=mat('Limestone / warm coralline',(.65,.61,.48),.78)
maptex(limestone,'limestone-color.png','Base Color');maptex(limestone,'limestone-roughness.png','Roughness',True)
water=mat('Lagoon / turquoise enamel',(.026,.34,.36),.23,.12)
maptex(water,'lagoon-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Lagoon / deep teal seam',(.016,.075,.07),.8)
forest=mat('Forest / evergreen crowns',(.07,.20,.085),.86)
maptex(forest,'forest-color.png','Base Color')
granite=limestone
'''+helpers+'''for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(limestone if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Limestone / front' if sy<0 else 'Limestone / rear',(0,sy*1.145,.83),(3.72,.19,1.46),limestone,bevel=.025)
for sx in [-1,1]:cube('Limestone / side',(sx*1.745,0,.83),(.23,2.10,1.46),limestone,bevel=.025)
cube('Limestone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),limestone,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Limestone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),limestone,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),limestone,lid,.045)
cube('Lagoon / inset',(0,0,1.982),(3.30,1.95,.035),water,lid,.014)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
'''+stone+'''for sx in [-1,1]:
 for sy in [-1,1]:stone('Limestone foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=3)
# Original ring-stack island profiles: undercut pale shoreline, wide forested crown.
# One connected closed triangulated surface per island, with material bands.
islands=[(-1.05,.38,.40,.29,.43),(-.22,.50,.34,.28,.53),(.66,.45,.43,.29,.58),(1.12,-.37,.28,.24,.34),(.24,-.40,.38,.25,.39),(-.72,-.43,.31,.21,.30)]
for k,(x,y,rx,ry,h) in enumerate(islands):
 verts=[];faces=[];N=28
 rings=[(0,.65),(.07,.73),(.19,1),(.42,.98),(.68,.80),(.88,.48)]
 for level,rad in rings:
  for j in range(N):
   a=j*math.tau/N;rough=1+.075*math.sin(a*3+k)+.045*math.cos(a*7+2*k)
   verts.append((x+rx*rad*rough*math.cos(a),y+ry*rad*rough*math.sin(a),1.987+h*level+.012*math.sin(a*4+k)*level))
 verts.extend([(x,y,1.987),(x+.02,y,1.987+h)])
 for r in range(len(rings)-1):
  for j in range(N):
   a=r*N+j;b=r*N+(j+1)%N;c=b+N;d=a+N
   faces.extend([(a,b,c),(a,c,d)])
 for j in range(N):faces.extend([(len(verts)-2,(j+1)%N,j),((len(rings)-1)*N+j,(len(rings)-1)*N+(j+1)%N,len(verts)-1)])
 me=bpy.data.meshes.new('Island triangulated terrain');me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new('Island / '+str(k),me);bpy.context.collection.objects.link(o);me.materials.append(limestone);me.materials.append(forest)
 for f in me.polygons:
  f.material_index=1 if f.center.z>1.987+h*.39 else 0
  f.use_smooth=True
 uv(o);parent(o)
'''+metal+cleanup+'''for o in bpy.data.objects:
 if o.name=='Studio / shadow floor':o.location.z=-.32
bpy.ops.object.camera_add(location=(-5.6,-7.8,5.7));cam=bpy.context.object;cam.name='Studio / camera';cam.rotation_euler=(Vector((0,0,1.17))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=5.9
scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.use_compositing=False;scene.render.threads_mode='FIXED';scene.render.threads=2
scene.render.resolution_x=900;scene.render.resolution_y=760;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(R/'palau.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.data.objects:
 if not o.name.startswith('Studio') and o.type in ['MESH','EMPTY']:o.select_set(True)
bpy.context.view_layer.objects.active=lid;bpy.ops.export_scene.gltf(filepath=str(R/'palau.glb'),export_format='GLB',use_selection=True,export_apply=True,export_animations=False)
scene.render.filepath=str(R/'poster.png');bpy.ops.render.render(write_still=True)
print('PALAU AUTHORED')
''',encoding='utf8')
print('Palau-local pipeline created')
