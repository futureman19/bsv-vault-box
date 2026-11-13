from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','package.json','THREE-LICENSE.txt']:
 shutil.copy2(S/n,R/n)
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
for n in ['build.py','viewer.js','template.html','verify_source.py','verify_parity.py','verify_browser.py']:
 s=(S/n).read_text().replace('japan-cedar-v1','belarus-v1').replace('japan','belarus').replace('Japan / Cedar & Moss','Belarus / Golden Straw').replace('Japan Cedar and Moss','Belarus Golden Straw').replace('Japan','Belarus').replace('JAPAN','BELARUS')
 s=s.replace('Yakushima cedar. Mossed granite. Quiet brass.','Golden cereal straw. Woven relief. Satin brass.').replace('inspired by the original Belarus concept','inspired by Belarusian straw craft; an original geometric study, not a traditional pattern')
 (R/n).write_text(s)
s=(S/'author.py').read_text()
s=s.replace('Reference-led Japan pilot','Brief-led Belarus pilot').replace('japan','belarus').replace('JAPAN','BELARUS')
s=s.replace("wood=mat('Cedar / fine longitudinal grain'","wood=mat('Straw / woven golden skin'").replace("end=mat('Cedar / dark finger endgrain'","end=mat('Timber / dark edging'")
s=s.replace("(.035,.07,.032)","(.07,.035,.012)")
s=s.replace("wood,lid,.045)","end,lid,.045)")
# Remove country-specific tree/terrain generation, preserve helpers and family fittings.
a=s.index("stone('Terrain / granite'"); b=s.index('# Medallion is solid')
s=s[:a]+'''# Actual flat-strip interlacing, original geometric pattern rather than ritual imagery.
straw=mat('Straw / pale ribbons',(.65,.43,.13),.57)
straw2=mat('Straw / warm ribbons',(.45,.25,.065),.62)
def ribbon(name,axis,index,count,material):
 verts=[];faces=[]
 # Crossings every .12 units, sampled at 4 intervals per crossing.
 length=1.44 if axis=='Y' else 2.40
 segments=48 if axis=='Y' else 80
 for j in range(segments+1):
  t=-length/2+length*j/segments
  fixed=(index-(count-1)/2)*.12
  phase=(t/.12+(6 if axis=='Y' else 10)+index)*math.pi
  z=2.020+(.018 if axis=='Y' else -.018)*math.cos(phase)
  for side,dz in [(-1,-.009),(1,-.009),(1,.009),(-1,.009)]:
   x,y=(fixed+side*.043,t) if axis=='Y' else (t,fixed+side*.043)
   verts.append((x,y,z+dz))
 for j in range(segments):
  for k in range(4):faces.append((j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4,(j+1)*4+k))
 faces.extend([(3,2,1,0),tuple(segments*4+k for k in range(4))])
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(material);parent(o)
for i in range(21):ribbon('Weave / warp '+str(i),'Y',i,21,straw)
for i in range(13):ribbon('Weave / weft '+str(i),'X',i,13,straw2)
# Underlay touches slab and supports low points of the interlaced ribbons.
cube('Weave / backing',(0,0,1.986),(2.52,1.58,.018),end,lid,.003)
for sy in [-1,1]:cube('Binding / long',(0,sy*.79,2.004),(2.60,.05,.045),gold,lid,.006)
for sx in [-1,1]:cube('Binding / side',(sx*1.29,0,2.004),(.05,1.63,.045),gold,lid,.006)
''' +s[b:]
s=s.replace("material=granite,sub=2","material=end,sub=2").replace("scene.cycles.samples=32","scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.use_nodes=False")
(R/'author.py').write_text(s)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
print('Scoped author/viewer/check lineage copied; brief already written.')
