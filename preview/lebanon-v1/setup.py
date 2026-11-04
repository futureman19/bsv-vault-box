from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','THREE-LICENSE.txt','package.json']:
 shutil.copy2(S/n,R/n)
for n in ['viewer.js','template.html','build.py','verify_source.py','verify_parity.py','verify_browser.py']:
 s=(S/n).read_text(encoding='utf8').replace('japan-cedar-v1','lebanon-v1').replace('japan.glb','lebanon.glb').replace('japan.blend','lebanon.blend').replace('Japan','Lebanon').replace('JAPAN','LEBANON').replace('Cedar & Moss','Cedar & Limestone').replace('Yakushima cedar. Mossed granite. Quiet brass.','Layered limestone. Broad cedar boughs. Quiet brass.').replace('inspired by the original Lebanon concept','inspired by Lebanon’s cedar forests and rocky valleys')
 (R/n).write_text(s,encoding='utf8')
s=(S/'author.py').read_text();s=s.replace('Japan','Lebanon').replace('japan','lebanon').replace('JAPAN','LEBANON')
a=s.index('# Exterior skins');b=s.index('# Small collar')
s=s[:a]+'''# Monolithic limestone skins, separate from the continuous inner shell.
limestone=mat('Limestone / warm layered chalk',(.64,.59,.48),.8);maptex(limestone,'limestone-color.png','Base Color');maptex(limestone,'limestone-roughness.png','Roughness',True)
for sy in [-1,1]:cube('Limestone / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),limestone,bevel=.018)
for sx in [-1,1]:cube('Limestone / end wall',(sx*1.745,0,.83),(.23,2.10,1.46),limestone,bevel=.018,axis='Y')
''' +s[b:]
s=s.replace("(.56,.075,.47),wood", "(.56,.075,.47),limestone")
a=s.index("stone('Terrain / granite'");b=s.index('def tube',a)
s=s[:a]+"stone('Terrain / limestone root bed',(.55,.35,2.02),(.48,.36,.13),lid,limestone,sub=3)\n"+s[b:]
a=s.index('trunk=[');b=s.index('# Medallion',a)
s=s[:a]+'''# Lebanon cedar: broad horizontal branches and irregular flattened foliage pads.
trunk=[(.55,.35,2.08),(.53,.35,2.30),(.57,.36,2.55),(.55,.35,2.82)]
tube('Lebanon cedar / trunk',trunk,[.075,.055,.035,.012],bark)
for j in range(6):
 a=j*math.tau/6;tube('Lebanon cedar / root',[(.55+math.cos(a)*.24,.35+math.sin(a)*.18,2.09),(.55,.35,2.18),trunk[1]],[.014,.03,.03],bark)
for level,(z,radius) in enumerate([(2.39,.52),(2.59,.43),(2.77,.30)]):
 for j in range(5):
  a=j*math.tau/5+level*.5;tip=(.55+math.cos(a)*radius,.35+math.sin(a)*radius,z+.025)
  tube('Lebanon cedar / branch',[(.55,.35,z-.09),(.55+math.cos(a)*radius*.45,.35+math.sin(a)*radius*.45,z-.01),tip],[.025,.016,.005],bark)
  stone('Lebanon cedar / canopy tier '+str(level),tip,(.23,.18,.065),lid,leafm[(j+level)%4],sub=2)
stone('Lebanon cedar / crown',(.55,.35,2.86),(.25,.22,.065),lid,leafm[1],sub=2)
''' +s[b:]
s=s.replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=2;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=750')
(R/'author.py').write_text(s)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
print('Setup complete')
