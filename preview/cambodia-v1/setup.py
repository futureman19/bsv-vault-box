from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; B=R.parent/'japan-cedar-v1'
for f in ['mechanism.blend','motion.mjs','verify_source.py','verify_parity.py','verify_browser.py','build.py','viewer.js','template.html','package.json']:
 if f.endswith('.blend'):shutil.copyfile(B/f,R/f);continue
 s=(B/f).read_text(encoding='utf8').replace('japan-cedar-v1','cambodia-v1').replace('japan.blend','cambodia.blend').replace('japan.glb','cambodia.glb').replace('Japan / Cedar & Moss','Cambodia / Sandstone & Baray').replace('Interactive Japan Cedar and Moss','Interactive Cambodia Sandstone and Baray').replace('Yakushima cedar. Mossed granite. Quiet brass.','Warm sandstone. Still water. Quiet brass.').replace('inspired by the original Japan concept','inspired by Cambodian sandstone architecture and reservoirs').replace('JAPAN ·','CAMBODIA ·')
 if f=='template.html':s=s[:s.index('@media')]+'''@media(max-width:600px){main{padding:18px}header{margin-top:20px}.top{gap:10px}.tag{max-width:150px;text-align:right}#stage{height:350px}h1{font-size:30px}.foot{flex-direction:column;gap:12px}button{padding:0 20px}}</style>'''+s.split('</style>',1)[1]
 if f=='viewer.js':s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.5,7)').replace('controls.maxDistance=11','controls.maxDistance=14')
 if f=='verify_browser.py':s=s.replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1');assert page.evaluate('pilot.progress')==1").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0');assert page.evaluate('pilot.progress')==0")
 (R/f).write_text(s,encoding='utf8')
shutil.copyfile(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
shutil.copyfile(R.parent/'iceland-pilot/THREE-LICENSE.txt',R/'THREE-LICENSE.txt')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
(R/'.gitattributes').write_text('* -text\n')
s=(B/'author.py').read_text();prefix=s[:s.index('wood=mat')];helpers=s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
# Stone UV projection uses dominant normal, not inherited wood axes.
helpers=helpers[:helpers.index('def uv(')]+'''def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone projection')
 for p in o.data.polygons:
  a=max(range(3),key=lambda i:abs(p.normal[i]));axes=[i for i in range(3) if i!=a]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]*.7+.5,co[axes[1]]*.7+.5)
'''+helpers[helpers.index('def cube('):]
materials='''stone_mat=mat('Sandstone / warm ashlar',(.47,.31,.16),.8);maptex(stone_mat,'stone-color.png','Base Color');maptex(stone_mat,'stone-roughness.png','Roughness',True)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
granite=mat('Stone / dark footing',(.18,.17,.13),.9);maptex(granite,'foot-color.png','Base Color')
seam=mat('Mineral seam / deep olive',(.035,.055,.022),.9)
moss=mat('Moss / low cushions',(.095,.16,.035),.95)
water=mat('Baray / blue green',(.035,.23,.22),.20,.12)
wood=stone_mat
'''
body='''for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone_mat if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Solid side skins with shallow individual ashlar relief; corners butt, never overlap.
for sx in [-1,1]:cube('Sandstone / side skin',(sx*1.745,0,.83),(.23,2.48,1.46),stone_mat,bevel=.009)
for sy in [-1,1]:cube('Sandstone / long skin',(0,sy*1.145,.83),(3.26,.19,1.46),stone_mat,bevel=.009)
for row in range(5):
 z=.10+(row+.5)*1.46/5
 # inset joint strips leave solid liner behind every recess
 for sy in [-1,1]:
  for j in range(7):cube('Ashlar / long block',( -1.62+(j+.5)*3.24/7,sy*1.244,z),(3.24/7-.012,.018,1.46/5-.012),stone_mat,bevel=.002)
 for sx in [-1,1]:
  for j in range(5):cube('Ashlar / side block',(sx*1.864,-1.22+(j+.5)*2.44/5,z),(.018,2.44/5-.012,1.46/5-.012),stone_mat,bevel=.002)
cube('Sandstone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone_mat,bevel=.025)
'''
seams=s[s.index('for sy in [-1,1]:\n cube(\'Mineral seam'):s.index('# A thin satin')].replace('Cedar / rim corner','Sandstone / rim corner')
caps=s[s.index('# Restrained brass'):s.index("stone('Terrain / granite'")]
orn='''# Original invented reservoir-and-stepped-architecture composition.
cube('Baray / water',(-.65,-.05,1.991),(1.05,1.34,.028),water,lid,.008)
for x in [-1.21,-.09]:cube('Baray / rim side',(x,-.05,2.015),(.06,1.46,.074),stone_mat,lid,.006)
for y in [-.75,.65]:cube('Baray / rim end',(-.65,y,2.015),(1.06,.06,.074),stone_mat,lid,.006)
for i,(w,z,h) in enumerate([(1.0,2.052,.15),(.78,2.207,.16),(.56,2.382,.19)]):
 cube('Sanctuary / tier '+str(i),(.60,.35,z),(w,w,h),stone_mat,lid,.012)
# Ribbed taper: angular lotus-bud-inspired silhouette, no sacred figures.
for i in range(5):
 w=.42-i*.063;z=2.52+i*.075
 cube('Sanctuary / pinnacle '+str(i),(.60,.35,z),(w,w,.083),stone_mat,lid,.009)
for x,y in [(-1.44,.80),(-1.45,.47),(.18,-.82),(.46,-.85),(1.34,.68)]:
 stone('Garden / moss',(x,y,1.992),(.13,.10,.035),lid,moss,2)
'''
tail=s[s.index('# Medallion is solid'):].replace('japan.blend','cambodia.blend').replace('japan.glb','cambodia.glb').replace('JAPAN AUTHORED','CAMBODIA AUTHORED').replace('location=(-5.6,-7.8,4.5)','location=(-5.6,-7.8,6.5)').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
(R/'author.py').write_text(prefix+materials+helpers+body+seams+caps+orn+tail)
print('Scoped scripts prepared; brief existed before generator.')
