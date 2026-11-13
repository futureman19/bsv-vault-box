from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','motion.mjs','THREE-LICENSE.txt']:
 shutil.copy2(S/name,R/name)
for name in ['verify_source.py','verify_parity.py','build.py','verify_browser.py','viewer.js','template.html','package.json']:
 s=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','liechtenstein-v1').replace('japan.blend','liechtenstein.blend').replace('japan.glb','liechtenstein.glb').replace('Japan / Cedar & Moss','Liechtenstein / Three Sisters Limestone').replace('Japan Cedar and Moss','Liechtenstein Three Sisters Limestone').replace('Yakushima cedar. Mossed granite. Quiet brass.','Alpine limestone. Three rocky summits. Satin brass.').replace('inspired by the original Japan concept','inspired by the Liechtenstein Three Sisters landscape').replace('JAPAN ·','LIECHTENSTEIN ·')
 if name=='viewer.js':
  s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.3,7)').replace('controls.maxDistance=11','controls.maxDistance=14')
 if name=='verify_browser.py':
  s=s.replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1');assert page.evaluate('pilot.progress')==1").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0');assert page.evaluate('pilot.progress')==0")
 (R/name).write_text(s,encoding='utf8')
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
s=(S/'author.py').read_text()
start=s[:s.index('# Exterior skins')]
start=start.replace("wood=mat('Cedar / fine longitudinal grain'","wood=mat('Limestone / fine mineral skin'").replace('cedar-color.png','limestone-color.png').replace('cedar-roughness.png','limestone-roughness.png').replace('cedar-end.png','rock-detail.png').replace('granite.png','rock-detail.png')
# Dominant-axis mapping avoids stretching stone side panels.
a=start.index('def uv('); b=start.index('\ndef cube(',a)
start=start[:a]+'''def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone planar')
 for f in o.data.polygons:
  axis=max(range(3),key=lambda a:abs(f.normal[a])); axes=[a for a in range(3) if a!=axis]
  for li in f.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]/2+.5,co[axes[1]]/2+.5)
''' +start[b:]
body='''# Continuous limestone skins, butt-joined at corners.
for sy in [-1,1]:
 cube('Limestone / front' if sy<0 else 'Limestone / rear',(0,sy*1.145,.83),(3.26,.19,1.46),wood,bevel=.012)
for sx in [-1,1]:
 cube('Limestone / side',(sx*1.745,0,.83),(.23,2.48,1.46),wood,bevel=.012)
'''
middle=s[s.index('# Small collar'):s.index('stone(\'Terrain / granite')]
# Remove inherited lid end-grain fingers.
a=middle.index('# A thin satin');b=middle.index('# Restrained brass',a);middle=middle[:a]+middle[b:]
terrain='''# Three individually shaped rocky massifs rooted in the lid.
base=cube('Terrain / alpine meadow',(0,.20,2.005),(2.80,1.16,.075),moss,lid,.025)
for k,(cx,height) in enumerate([(-.8,.65),(0,.94),(.8,.76)]):
 verts=[]; faces=[]; sides=9
 for ring,(radius,z) in enumerate([(.43,2.025),(.35,2.20),(.22,2.025+height*.70)]):
  for j in range(sides):
   a=j*math.tau/sides; r=radius*(1+.12*math.sin(j*2.7+k))
   verts.append((cx+math.cos(a)*r,.22+math.sin(a)*r*.78,z+.025*math.sin(j*2+k)))
 verts.append((cx+.07,.20,2.025+height))
 for ring in range(2):
  for j in range(sides):
   a=ring*sides+j;b=ring*sides+(j+1)%sides
   faces.append((a,b,b+sides,a+sides))
 for j in range(sides):faces.append((18+j,18+(j+1)%sides,27))
 faces.append(tuple(reversed(range(sides))))
 me=bpy.data.meshes.new('Ridge fractured limestone');me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new('Three Sisters / peak '+str(k+1),me);bpy.context.collection.objects.link(o);me.materials.append(granite);uv(o);parent(o)
'''
end=s[s.index('# Medallion is solid'):]
s=start+body+middle+terrain+end
s=s.replace('japan.blend','liechtenstein.blend').replace('japan.glb','liechtenstein.glb').replace('JAPAN AUTHORED','LIECHTENSTEIN AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=800')
(R/'author.py').write_text(s)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
print('Scoped scripts prepared')
