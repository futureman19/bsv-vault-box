from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','motion.mjs','THREE-LICENSE.txt','package.json']:
 shutil.copyfile(S/name,R/name)
for name in ['build.py','viewer.js','template.html','verify_source.py','verify_parity.py','verify_browser.py']:
 s=(S/name).read_text('utf8').replace('japan-cedar-v1','tonga-v1').replace('japan.glb','tonga.glb').replace('japan.blend','tonga.blend').replace('Japan / Cedar & Moss','Tonga / Ngatu & Ochre').replace('Japan Cedar and Moss','Tonga Ngatu and Ochre').replace('Yakushima cedar. Mossed granite. Quiet brass.','Ochre barkcloth patterns. Raised diamond inlays. Satin brass.').replace('inspired by the original Japan concept','inspired by Tongan ngatu material traditions; invented motifs, not traditional pattern reproductions').replace('JAPAN ·','TONGA ·')
 if name=='verify_browser.py':
  s=s.replace("page.wait_for_timeout(70);assert", "page.wait_for_function('pilot.progress===1');assert").replace("page.wait_for_timeout(60);assert", "page.wait_for_function('pilot.progress===0');assert")
 (R/name).write_text(s,'utf8')
a=(S/'author.py').read_text('utf8'); start=a[:a.index('wood=mat(')]; helpers=a[a.index('def uv('):a.index('for o in bpy.data.objects:')]
body='''
wood=mat('Timber / dark supporting frame',(.075,.035,.018),.6)
cloth=mat('Ngatu / invented ochre geometry',(.6,.4,.2),.85);maptex(cloth,'ngatu-color.png','Base Color');maptex(cloth,'ngatu-roughness.png','Roughness',True)
cream=mat('Ngatu / cream relief panel',(.60,.40,.21),.85);maptex(cream,'fiber-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
ink=mat('Dyed relief / dark brown',(.09,.025,.009),.9)
seam=mat('Seam / shadow',(.025,.015,.01),.9)
'''
body+=helpers
body+='''
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
for sy in [-1,1]:
 cube('Ngatu / broad panel',(0,sy*1.145,.83),(3.72,.19,1.46),cloth,bevel=.012)
for sx in [-1,1]:
 cube('Ngatu / side panel',(sx*1.745,0,.83),(.23,2.48,1.46),cloth,axis='Y')
 for sy in [-1,1]:cube('Timber / corner',(sx*1.75,sy*1.15,.83),(.24,.24,1.47),wood)
for z in [.16,1.50]:
 for sy in [-1,1]:cube('Timber / long rail',(0,sy*1.24,z),(3.72,.055,.10),wood)
 for sx in [-1,1]:cube('Timber / short rail',(sx*1.87,0,z),(.055,2.48,.10),wood)
cube('Timber / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam)
for sx in [-1,1]:cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
cube('Lid / ngatu panel',(0,0,1.995),(3.10,1.75,.04),cream,lid,.012)
for sy in [-1,1]:cube('Lid / border long',(0,sy*.91,2.005),(3.25,.055,.055),ink,lid,.008)
for sx in [-1,1]:cube('Lid / border short',(sx*1.60,0,2.005),(.055,1.86,.055),ink,lid,.008)
# Six hollow diamonds: mesh bars retain a real open center.
for i,x in enumerate([-1.03,0,1.03]):
 for j,y in enumerate([-.43,.43]):
  outer=[(x,y-.27),(x+.33,y),(x,y+.27),(x-.33,y)];inner=[(x,y-.215),(x+.265,y),(x,y+.215),(x-.265,y)]
  vs=[(a,b,z) for z in [2.013,2.038] for ring in [outer,inner] for a,b in ring];fs=[]
  for k in range(4):
   n=(k+1)%4;fs += [(k,n,n+8,k+8),(k+4,k+12,n+12,n+4),(k+8,n+8,n+12,k+12),(k,k+4,n+4,n)]
  me=bpy.data.meshes.new('Diamond');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Lid / diamond '+str(i*2+j),me);bpy.context.collection.objects.link(o);me.materials.append(ink);parent(o)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Timber / foot',(sx*1.47,sy*.91,-.10),(.48,.42,.35),wood,bevel=.05)
'''
end=a[a.index('# Medallion is solid'):].replace('japan.blend','tonga.blend').replace('japan.glb','tonga.glb').replace('JAPAN AUTHORED','TONGA AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=2;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=800')
(R/'author.py').write_text(start+body+end,'utf8')
(R/'.gitattributes').write_text('* -text\n','utf8')
print('SETUP PASS')
