from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','motion.mjs']:
 shutil.copy2(S/name,R/name)
for name in ['build.py','viewer.js','template.html','verify_source.py','verify_parity.py','verify_browser.py','package.json']:
 s=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','timor-leste-v1').replace('japan.glb','timor-leste.glb').replace('japan.blend','timor-leste.blend').replace('Japan / Cedar & Moss','Timor-Leste / Tais & Indigo').replace('Japan Cedar and Moss','Timor-Leste Tais and Indigo').replace('Yakushima cedar. Mossed granite. Quiet brass.','Woven cotton rhythm. Indigo stripes. Quiet brass.').replace('inspired by the original Japan concept','inspired by Timor-Leste’s Tais textile tradition; invented stripes, not a reproduction of a community motif').replace('JAPAN ·','TIMOR-LESTE ·')
 (R/name).write_text(s,encoding='utf8')
s=(S/'author.py').read_text()
s=s[:s.index('wood=mat')]+s[s.index('def uv('):s.index('for o in bpy.data.objects:')]+'''wood=mat('Timber / dark warm frame',(.16,.065,.025),.5);maptex(wood,'wood.png','Base Color')
cloth=mat('Tais inspired / invented striped cotton',(.4,.1,.06),.85);maptex(cloth,'textile.png','Base Color');maptex(cloth,'roughness.png','Roughness',True)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / indigo',(.018,.028,.055),.9)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o,'Y' if 'end' in o.name else 'X')
for sy in [-1,1]:
 cube('Frame / long',(0,sy*1.145,.83),(3.72,.19,1.46),wood)
 o=cube('Cloth / long panel',(0,sy*1.246,.84),(3.25,.018,.96),cloth,bevel=.003)
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers.active.data[li].uv=(co.x/3.25+.5,co.z/.96+.5)
for sx in [-1,1]:
 cube('Frame / end',(sx*1.745,0,.83),(.23,2.48,1.46),wood,axis='Y')
 o=cube('Cloth / end panel',(sx*1.868,0,.84),(.018,1.98,.96),cloth,bevel=.003)
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;o.data.uv_layers.active.data[li].uv=(co.y/1.98+.5,co.z/.96+.5)
cube('Frame / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:
  cube('Frame / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
  cube('Foot / timber',(sx*1.47,sy*.91,-.10),(.48,.4,.32),wood,bevel=.045)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# Low waved cotton runner with closed perimeter down to lid.
verts=[];faces=[];nx=48;ny=24
for j in range(ny+1):
 for i in range(nx+1):
  x=-1.55+3.1*i/nx;y=-.82+1.64*j/ny
  verts.append((x,y,2.03+.014*math.sin(x*7+y*2)+.006*math.sin(y*13)))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
for k,a in enumerate(boundary):
 b=boundary[(k+1)%len(boundary)];n=len(verts);verts.extend([(verts[a][0],verts[a][1],1.978),(verts[b][0],verts[b][1],1.978)]);faces.append((a,n,n+1,b))
me=bpy.data.meshes.new('Runner grid');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Runner / waved textile',me);bpy.context.collection.objects.link(o);me.materials.append(cloth)
ul=me.uv_layers.new()
for f in me.polygons:
 for li in f.loop_indices:
  co=me.vertices[me.loops[li].vertex_index].co;ul.data[li].uv=(co.x/3.1+.5,co.y/1.64+.5)
parent(o)
fringe=mat('Cotton / ivory fringe',(.62,.49,.29),.95)
for sx in [-1,1]:
 for i in range(28):
  y=-.78+i*1.56/27
  cube('Fringe / strand',(sx*1.61,y,1.991),(.12,.013,.024),fringe,lid,.004)
'''+s[s.index('# Medallion is solid'):]
s=s.replace('japan.blend','timor-leste.blend').replace('japan.glb','timor-leste.glb').replace('JAPAN AUTHORED','TIMOR-LESTE AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=4').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820').replace('(-5.6,-7.8,4.5)','(-5.6,-7.8,6.3)')
(R/'author.py').write_text(s)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
print('Scaffolded scoped pilot')
