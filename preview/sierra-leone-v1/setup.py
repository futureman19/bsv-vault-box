from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for f in ['mechanism.blend','THREE-LICENSE.txt','package.json','motion.mjs']:
 shutil.copy2(S/f,R/f)
for f in ['build.py','viewer.js','template.html','verify_browser.py','verify_source.py','verify_parity.py']:
 s=(S/f).read_text(encoding='utf8').replace('japan-cedar-v1','sierra-leone-v1').replace('japan.glb','sierra-leone.glb').replace('japan.blend','sierra-leone.blend').replace('Japan / Cedar & Moss','Sierra Leone / Gola Canopy').replace('Interactive Japan Cedar and Moss','Interactive Sierra Leone Gola Canopy').replace('Yakushima cedar. Mossed granite. Quiet brass.','Rainforest canopy. Earth-bark relief. Satin brass.').replace('the original Japan concept','the Gola rainforest landscape').replace('JAPAN ·','SIERRA LEONE ·')
 (R/f).write_text(s,encoding='utf8')
s=(S/'author.py').read_text();s=s.replace('japan.blend','sierra-leone.blend').replace('japan.glb','sierra-leone.glb').replace('JAPAN AUTHORED','SIERRA LEONE AUTHORED')
s=s.replace("wood=mat('Cedar / fine longitudinal grain'","wood=mat('Earth bark / vertical grain'").replace('cedar-color.png','earth-color.png').replace('cedar-roughness.png','earth-roughness.png').replace('cedar-end.png','earth-end.png')
s=s.replace("leafm=[mat('Cedar foliage / '","leafm=[mat('Broadleaf canopy / '")
a=s.index('# Exterior skins');b=s.index('# Small collar')
s=s[:a]+'''# Continuous earth/bark skins, not horizontal timber courses.
for sy in [-1,1]:cube('Earth / front rear',(0,sy*1.145,.83),(3.26,.19,1.46),wood)
for sx in [-1,1]:cube('Earth / side',(sx*1.745,0,.83),(.23,2.48,1.46),wood,axis='Y')
for sy in [-1,1]:
 for j in range(23):
  x=-1.55+j*.14
  if abs(x)<.33:continue
  cube('Bark relief / vertical furrow',(x,sy*1.247,.82+random.uniform(-.07,.07)),(.018+random.random()*.025,.025,.95+random.random()*.25),bark,bevel=.008)
''' +s[b:]
s=s.replace('1.618),(3.28,.16 if sy<0 else .08,.108)','1.618),(3.28,.16 if sy<0 else .08,.08)').replace('(.16,2.05,.108)','(.16,2.05,.08)')
a=s.index('slab=cube');b=s.index('# Restrained brass')
s=s[:a]+'''green=mat('Lid / forest green',(.025,.095,.045),.45)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),green,lid,.045)
'''+s[b:]
a=s.index("stone('Terrain / granite'");b=s.index('def tube')
s=s[:a]+"stone('Forest floor / island',(0,.38,1.99),(1.22,.64,.105),lid,moss,3)\n"+s[b:]
a=s.index('trunk=[');b=s.index('# Medallion')
s=s[:a]+'''for ti,(x,y,h) in enumerate([(-.70,.35,.74),(.08,.65,.91),(.75,.35,.68)]):
 base=2.045
 trunk=[(x,y,base),(x+.035,y,base+.22),(x-.025,y+.02,base+h*.68),(x+.035,y,base+h)]
 tube('Gola / trunk '+str(ti),trunk,[.085,.06,.043,.018],bark)
 for j in range(6):
  a=j*math.tau/6
  tube('Gola / buttress',[(x+math.cos(a)*.22,y+math.sin(a)*.18,2.03),(x+math.cos(a)*.10,y+math.sin(a)*.08,2.10),trunk[1]],[.018,.038,.043],bark)
 for j in range(12):
  a=j*2.399;rad=.15+.17*(j%4)/3;z=base+h-.13+(j%3)*.055
  tip=(x+math.cos(a)*rad,y+math.sin(a)*rad,z)
  tube('Gola / branch',[trunk[2],tip],[.019,.006],bark,sides=7)
  stone('Gola / broadleaf cluster',tip,(.22,.17,.075),lid,leafm[j%4],2)
'''+s[b:]
s=s.replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=4').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
(R/'author.py').write_text(s)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
