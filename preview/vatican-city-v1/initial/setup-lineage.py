"""Copy read-only mechanical/viewer lineage; generate the Vatican author script."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','package.json','motion.mjs','build.py','verify_browser.py','verify_source.py','verify_parity.py','viewer.js','template.html']:
 if name.endswith('.blend'):shutil.copyfile(S/name,R/name);continue
 s=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','vatican-city-v1').replace('japan.glb','vatican-city.glb').replace('japan.blend','vatican-city.blend').replace('Japan / Cedar & Moss','Vatican City / Travertine & Mosaic').replace('Japan Cedar and Moss','Vatican City Travertine and Mosaic').replace('Yakushima cedar. Mossed granite. Quiet brass.','Ivory stone. An open colonnade. Enamel and brass.').replace('inspired by the original Japan concept','inspired by Vatican stone architecture and mosaic craft').replace('JAPAN ·','VATICAN CITY ·')
 (R/name).write_text(s,encoding='utf8')
s=(S/'author.py').read_text()
# Keep mechanical helpers, explicit parenting and proven skin/hinge fit, not cedar art.
a=s[s.index('import bpy'):s.index('wood=mat')]
a+='''stone_mat=mat('Travertine / warm ivory',(.62,.54,.41),.55);maptex(stone_mat,'stone-color.png','Base Color');maptex(stone_mat,'stone-roughness.png','Roughness',True)
granite=mat('Stone foot / warm limestone',(.35,.30,.22),.8);maptex(granite,'foot-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
blue=mat('Enamel / deep lapis blue',(.018,.075,.19),.22)
ivory=mat('Enamel / ivory',(.75,.69,.53),.25)
seam=mat('Seam / dark bronze',(.055,.043,.025),.6,.35)
'''
a+='''def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone face projection')
 for p in o.data.polygons:
  normal=p.normal
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   if abs(normal.z)>.7:u,v=co.x,co.y
   elif abs(normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u/2+.5,v/2+.5)
'''
a+=s[s.index('def cube'):s.index('for o in bpy.data.objects:')].replace('m.segments=3','m.segments=1')
a+='''for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone_mat if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Travertine / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),stone_mat,bevel=.025)
for sx in [-1,1]:cube('Travertine / end wall',(sx*1.745,0,.83),(.23,2.1,1.46),stone_mat,bevel=.025)
cube('Travertine / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone_mat,bevel=.025)
for sy in [-1,1]:cube('Bronze seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Bronze seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Travertine / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone_mat,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone_mat,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
'''
a+=s[s.index('def stone'):s.index("stone('Terrain")]
a+='''# Original miniature: two opposing curved arcades, with unobstructed oval center.
def arc(n,a0,a1,z,height,material):
 vs=[];fs=[];steps=40
 for i in range(steps+1):
  a=a0+(a1-a0)*i/steps
  for dz in [0,height]:
   for d in [-.075,.075]:vs.append(((1.06+d)*math.cos(a),(.57+d)*math.sin(a),z+dz))
 for i in range(steps):
  k=i*4;j=k+4
  fs.extend([(k,j,j+1,k+1),(k+2,k+3,j+3,j+2),(k,k+2,j+2,j),(k+1,j+1,j+3,k+3)])
 fs.extend([(0,1,3,2),(steps*4,steps*4+2,steps*4+3,steps*4+1)])
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o);return o
for side in [0,1]:
 a0=math.radians(22+side*180);a1=math.radians(158+side*180)
 arc('Arcade / foundation '+str(side),a0,a1,1.978,.045,stone_mat)
 arc('Arcade / cornice '+str(side),a0,a1,2.388,.065,stone_mat)
 for i in range(12):
  a=a0+(a1-a0)*i/11;x=1.06*math.cos(a);y=.57*math.sin(a)
  cube('Arcade / column base',(x,y,2.046),(.105,.105,.048),stone_mat,lid,.008)
  bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=.038,depth=.30,location=(x,y,2.218));o=bpy.context.object;o.name='Arcade / column';o.data.materials.append(stone_mat);uv(o);parent(o)
  cube('Arcade / capital',(x,y,2.378),(.105,.105,.04),stone_mat,lid,.006)
# Blue and ivory mosaic tesserae are authored enamel chips, not a copied sacred pattern.
for sy in [-1,1]:
 for i in range(34):cube('Mosaic / tessera',( -1.51+i*.0915,sy*.91,1.996),(.074,.074,.034),blue if i%3 else ivory,lid,.004)
for sx in [-1,1]:
 for i in range(18):cube('Mosaic / tessera',(sx*1.51,-.78+i*.0915,1.996),(.074,.074,.034),blue if i%3 else gold,lid,.004)
'''
a+=s[s.index('# Medallion'):]
a=a.replace("R/'japan.blend'","R/'vatican-city.blend'").replace("R/'japan.glb'","R/'vatican-city.glb'").replace('JAPAN AUTHORED','VATICAN CITY AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=2;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
(R/'author.py').write_text(a,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n',encoding='utf8')
print('Prepared isolated authoring and verification lineage')
