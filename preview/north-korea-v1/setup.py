from pathlib import Path
import shutil
R=Path(__file__).resolve().parent;B=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','THREE-LICENSE.txt','motion.mjs','package.json']:
 shutil.copy2(B/n,R/n)
for n in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html']:
 s=(B/n).read_text(encoding='utf8').replace('japan-cedar-v1','north-korea-v1').replace('japan.glb','north-korea.glb').replace('japan.blend','north-korea.blend').replace('Japan / Cedar & Moss','North Korea / Paektu Caldera').replace('Japan Cedar and Moss','North Korea Paektu Caldera').replace('Yakushima cedar. Mossed granite. Quiet brass.','Volcanic stone. Caldera lake. Quiet brass.').replace('the original Japan concept','the Paektu volcanic landscape').replace('JAPAN ·','NORTH KOREA ·')
 s=s.replace('h1{font-siz... [truncated]','h1{font-size:30px}.foot{flex-direction:column}}')
 if n=='viewer.js':s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.8,7)').replace('controls.maxDistance=11','controls.maxDistance=14')
 if n=='verify_browser.py':s=s.replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1');assert page.evaluate('pilot.progress')==1").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0');assert page.evaluate('pilot.progress')==0")
 (R/n).write_text(s,encoding='utf8')
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
s=(B/'author.py').read_text()
s=s[:s.index('stone(\'Terrain / granite')]+s[s.index('# Medallion is solid'):]
s=s.replace("'japan.blend'","'north-korea.blend'").replace("'japan.glb'","'north-korea.glb'")
s=s.replace("'cedar-color.png'","'stone-color.png'").replace("'cedar-roughness.png'","'stone-roughness.png'").replace("'cedar-end.png'","'stone-color.png'").replace("'granite.png'","'stone-color.png'")
s=s.replace('Cedar','Volcanic stone').replace("(.035,.07,.032)","(.035,.065,.085)").replace('moss green','blue gray')
start=s.index('for i in range(8):');end=s.index('# Small collar')
s=s[:start]+'''for sy in [-1,1]:
 cube('Volcanic shell / front rear',(0,sy*1.145,.83),(3.26,.19,1.46),wood,bevel=.018)
for sx in [-1,1]:
 cube('Volcanic shell / sides',(sx*1.745,0,.83),(.23,2.48,1.46),wood,bevel=.018,axis='Y')
'''+s[end:]
a=s.index('for sx in [-1,1]:',s.index('# A thin satin'));b=s.index('# Restrained brass',a);s=s[:a]+s[b:]
s=s.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z","u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z")
s=s.replace('layer.data[li].uv=(u/3.72+.5,v/1.7+.5)','layer.data[li].uv=(u*.7+.5,v*.7+.5)')
orn='''# Closed miniature volcanic caldera: outer skirt, rim, inner slope.
ash=mat('Paektu / pale ash rock',(.42,.43,.40),.87)
water=mat('Lake Chon / deep blue',(.015,.13,.24),.19,.18)
N=96;verts=[];faces=[]
for ring in range(4):
 for j in range(N):
  a=j*math.tau/N;wave=.035*math.sin(7*a)+.022*math.sin(13*a)
  rx,ry=[(1.32,.82),(1.02,.64),(.73,.46),(.68,.42)][ring]
  z=[1.977,2.43+.10*math.sin(3*a)+.04*math.cos(7*a),2.18+wave,2.045][ring]
  verts.append(((rx+wave)*math.cos(a),(ry+wave*.5)*math.sin(a),z))
for k in range(3):
 for j in range(N):
  a=k*N+j;b=k*N+(j+1)%N;faces.append((a,b,b+N,a+N))
me=bpy.data.meshes.new('Caldera ring');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / Paektu caldera',me);bpy.context.collection.objects.link(o);me.materials.append(ash);parent(o)
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=1,depth=.025,location=(0,0,2.0675));o=bpy.context.object;o.name='Terrain / Lake Chon';o.scale=(.70,.44,1);select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(water);parent(o)
'''
s=s.replace('# Medallion is solid',orn+'\n# Medallion is solid')
s=s.replace('location=(-5.6,-7.8,4.5)','location=(-5.6,-7.8,6.7)').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False').replace('JAPAN AUTHORED','NORTH KOREA AUTHORED')
(R/'author.py').write_text(s)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
print('scoped scripts ready')
