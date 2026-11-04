from pathlib import Path
import shutil,json
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for f in ['mechanism.blend','motion.mjs','THREE-LICENSE.txt','package.json']:
 shutil.copy2(S/f,R/f)
for f in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html']:
 t=(S/f).read_text(encoding='utf8').replace('japan-cedar-v1','costa-rica-v1').replace('japan.glb','costa-rica.glb').replace('japan.blend','costa-rica.blend').replace('Japan / Cedar & Moss','Costa Rica / Arenal & Rainforest').replace('Japan Cedar and Moss','Costa Rica Arenal and Rainforest').replace('Yakushima cedar. Mossed granite. Quiet brass.','Volcanic stone. Emerald canopy. Quiet brass.').replace('inspired by the original Japan concept','inspired by Arenal volcano and Costa Rican rainforest').replace('JAPAN ·','COSTA RICA ·')
 (R/f).write_text(t,encoding='utf8')
a=(S/'author.py').read_text()
a=a.replace('japan.blend','costa-rica.blend').replace('japan.glb','costa-rica.glb').replace('JAPAN AUTHORED','COSTA RICA AUTHORED')
a=a.replace("wood=mat('Cedar / fine longitudinal grain'","wood=mat('Volcanic stone / forest patina'").replace("'cedar-color.png'","'stone-color.png'").replace("'cedar-roughness.png'","'stone-roughness.png'").replace("'cedar-end.png'","'stone-dark.png'")
a=a[:a.index('# Exterior skins')]+'''# Continuous volcanic exterior, not reused cedar finger courses.
for sy in [-1,1]:
 cube('Volcanic wall / front rear',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.018)
for sx in [-1,1]:
 cube('Volcanic wall / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.018,axis='Y')
'''+a[a.index('# Small collar'):]
a=a[:a.index('# A thin satin')]+a[a.index('# Restrained brass'):]
a=a[:a.index("stone('Terrain / granite'")]+a[a.index('# Medallion'):]
# Add authored thematic landscape before medallion.
land='''# Low island and fluted Arenal-inspired cone; all travel with the lid.
forest=mat('Rainforest ground',(.035,.105,.045),.94)
rock=mat('Arenal / weathered volcanic slopes',(.09,.12,.105),.85)
stone('Rainforest / island',(0,0,2.005),(1.46,.86,.10),lid,forest,3)
verts=[];faces=[];N=48
for k,(rad,z) in enumerate([(1,2.035),(.76,2.22),(.49,2.48),(.24,2.72),(.105,2.88),(.047,2.84)]):
 for j in range(N):
  angle=j*math.tau/N;flute=1+.045*math.sin(j*2.3)+.035*math.sin(j*4.7)
  verts.append((.45+.68*rad*flute*math.cos(angle),.25+.59*rad*flute*math.sin(angle),z+.012*math.sin(j*1.7)*rad))
for k in range(5):
 for j in range(N):
  a=k*N+j;b=k*N+(j+1)%N;faces.extend([(a,b,b+N),(a,b+N,a+N)])
faces.append(tuple(5*N+j for j in range(N)))
me=bpy.data.meshes.new('Fluted volcanic cone');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Arenal / cone',me);bpy.context.collection.objects.link(o);me.materials.append(rock);parent(o)
for i in range(24):
 angle=i*math.tau/24
 x=-.08+1.11*math.cos(angle);y=.67*math.sin(angle)
 stone('Rainforest / canopy '+str(i),(x,y,2.12+random.uniform(0,.06)),(.17,.14,.13),lid,leafm[i%4],2)
'''
a=a.replace('# Medallion is solid',land+'\n# Medallion is solid')
a=a.replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
a=a.replace('Reference-led Japan pilot.','Brief-led Costa Rica pilot.')
(R/'author.py').write_text(a,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n')
print('Prepared isolated Costa Rica source scripts')
