"""One-time scoped adaptation of the repository's mechanical pilot."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','THREE-LICENSE.txt','motion.mjs']:
 shutil.copyfile(S/n,R/n)
for n in ['build.py','verify_browser.py','verify_source.py','verify_parity.py','viewer.js','template.html','package.json']:
 s=(S/n).read_text(encoding='utf8').replace('japan-cedar-v1','tunisia-v1').replace('japan.blend','tunisia.blend').replace('japan.glb','tunisia.glb').replace('Japan','Tunisia').replace('JAPAN','TUNISIA').replace('Cedar & Moss','Sejnane Clay').replace('Cedar and Moss','Sejnane Clay')
 s=s.replace('Yakushima cedar. Mossed granite. Quiet brass.','Cream clay. Red ochre. Charcoal geometry.').replace('inspired by the original Tunisia concept','inspired by Sejnane pottery materials; abstract motifs are invented')
 s=s.replace('h1{font-siz... [truncated]','h1{font-size:30px}.foot{flex-direction:column;gap:8px}}')
 if n=='viewer.js':s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.6,7)').replace('controls.maxDistance=11','controls.maxDistance=14')
 if n=='verify_browser.py':
  s=s.replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1')").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0')")
  s=s.replace("context.close();browser.close()","context.close()\n context=browser.new_context(offline=True,java_script_enabled=False,viewport={'width':390,'height':844})\n page=context.new_page();page.goto((ROOT/'tunisia-v1.html').as_uri());assert page.locator('#fallback').is_visible();page.screenshot(path=str(ROOT/'mobile-nojs.png'));results.append({'case':'no JS','poster':True});context.close();browser.close()")
 (R/n).write_text(s,encoding='utf8')
s=(S/'author.py').read_text()
s=s[:s.index('# Exterior skins')]+'''# Continuous ceramic skins; butted corners avoid overlapping coplanar faces.
for sy in [-1,1]:cube('Clay / front rear',(0,sy*1.145,.83),(3.26,.19,1.46),wood,bevel=.012)
for sx in [-1,1]:cube('Clay / side',(sx*1.745,0,.83),(.23,2.48,1.46),wood,bevel=.012,axis='Y')
'''+s[s.index('# Small collar'):s.index('# A thin satin')]+s[s.index('# Restrained brass'):s.index("stone('Terrain / granite'")]+'''# Wheel-profile dish, a stylized interpretation rather than an authentic object.
N=96
profile=[(0,2.015),(.42,2.015),(.53,2.04),(.61,2.10),(.70,2.19),(.73,2.20),(.73,2.17),(.64,2.07),(.52,1.99),(0,1.99)]
verts=[];faces=[]
for r,z in profile:
 for i in range(N):
  a=i*math.tau/N;verts.append((r*math.cos(a),r*math.sin(a),z))
# Pole fans avoid degenerate zero-radius quads.
for j in range(len(profile)-1):
 for i in range(N):
  k=(i+1)%N
  if j==0:faces.append((i,N+i,N+k))
  elif j==len(profile)-2:faces.append((j*N+i,(j+1)*N+i,j*N+k))
  else:faces.append((j*N+i,(j+1)*N+i,(j+1)*N+k,j*N+k))
me=bpy.data.meshes.new('Concave dish');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Sejnane / shallow dish',me);bpy.context.collection.objects.link(o);me.materials.append(end);uv(o);parent(o)
for f in me.polygons:f.use_smooth=True
# Raised red and charcoal radial lip accents follow the dish profile.
charcoal=mat('Clay pigment / charcoal',(.026,.018,.013),.73)
ochre=mat('Clay pigment / red ochre',(.28,.055,.024),.75)
for i in range(12):
 a=i*math.tau/12
 o=cube('Sejnane / lip accent %02d'%i,(.687*math.cos(a),.687*math.sin(a),2.181),(.067,.027,.012),charcoal if i%2 else ochre,lid,.002)
 o.rotation_euler=(0,-.64,a)
'''+s[s.index('# Medallion'):]
s=s.replace('japan','tunisia').replace('JAPAN','TUNISIA').replace('Cedar / fine longitudinal grain','Clay / cream geometric slip').replace('Cedar / dark finger endgrain','Clay / ochre body').replace('cedar-color.png','clay-color.png').replace('cedar-roughness.png','clay-roughness.png').replace('cedar-end.png','clay-plain.png').replace('granite.png','clay-plain.png').replace('Granite / salt and pepper','Clay / fired feet').replace('Cedar /','Clay /').replace('Mineral seam / moss green','Seam / dark earth').replace("(.035,.07,.032)","(.045,.026,.014)")
s=s.replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820').replace('(-5.6,-7.8,4.5)','(-5.6,-7.8,6.3)')
(R/'author.py').write_text(s)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
shutil.copyfile(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
print('Scoped adaptation ready')
