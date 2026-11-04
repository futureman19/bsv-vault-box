"""Adapt the checked-in Japan mechanics; write only this new preview folder."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','THREE-LICENSE.txt']:
 shutil.copy2(S/n,R/n)
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
for n in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','package.json']:
 s=(S/n).read_text(encoding='utf8').replace('japan-cedar-v1','germany-v1').replace('japan','germany').replace('Japan Cedar and Moss','Germany Erzgebirge Woodcraft')
 if n=='viewer.js':s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.3,7)').replace('controls.maxDistance=11','controls.maxDistance=14')
 if n=='verify_browser.py':s=s.replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1');assert page.evaluate('pilot.progress')==1").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0');assert page.evaluate('pilot.progress')==0")
 (R/n).write_text(s,encoding='utf8')
s=(S/'maps.py').read_text().replace('cedar','wood').replace('167*v,87*v,46*v','190*v,145*v,88*v')
(R/'maps.py').write_text(s)
s=(S/'author.py').read_text()
s=s.replace('Reference-led Japan pilot','Germany Erzgebirge Woodcraft pilot').replace('japan','germany').replace('JAPAN AUTHORED','GERMANY AUTHORED').replace('cedar-','wood-').replace('Cedar','Woodcraft').replace("(.035,.07,.032)","(.07,.035,.012)")
a=s.index('for sx in [-1,1]:\n for sy in [-1,1]:stone(')
b=s.index('# Medallion is solid',a)
s=s[:a]+'''# Squat wooden feet and a lathe-turned village vignette.
for sx in [-1,1]:
 for sy in [-1,1]:cube('Wood foot',(sx*1.47,sy*.91,-.10),(.50,.42,.30),end,bevel=.055)
cream=mat('Village / pale wood',(.64,.43,.22),.56)
roofmat=mat('Village / oxblood stain',(.16,.031,.017),.56)
# Low elliptical base, top at 2.04, seated in the slab.
bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=1,depth=.07,location=(0,0,2.005))
base=bpy.context.object;base.name='Village / oval base';base.scale=(1.325,.775,1);select(base);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);base.data.materials.append(end);uv(base);parent(base)
def turned(n,x,y,h):
 # One continuous closed lathed profile with three flared foliage tiers.
 profile=[(.045,0),(.045,.12),(.27,.12),(.10,.39),(.23,.39),(.07,.65),(.17,.65),(.012,1)]
 vs=[];faces=[];N=32
 for rad,z in profile:
  for j in range(N):
   t=j*math.tau/N;vs.append((x+rad*h*math.cos(t),y+rad*h*math.sin(t),2.04+z*h))
 for i in range(len(profile)-1):
  for j in range(N):
   a=i*N+j;b=i*N+(j+1)%N;faces.append((a,b,b+N,a+N))
 faces.extend([tuple(reversed(range(N))),tuple((len(profile)-1)*N+j for j in range(N))])
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(wood);uv(o);parent(o)
 for f in me.polygons:f.use_smooth=len(f.vertices)==4
for i,(x,y,h) in enumerate([(-.85,.40,.65),(0,.48,.86),(.85,.40,.70)]):turned('Village / turned tree '+str(i),x,y,h)
for i,x in enumerate([-.52,.49]):
 y=-.30;w=.55;d=.48;z=2.04;h=.32
 cube('Village / house '+str(i),(x,y,z+h/2),(w,d,h),cream,lid,.008)
 # Solid triangular-prism gable roof, not an image card.
 verts=[(x-w*.62,y-d*.62,z+h),(x+w*.62,y-d*.62,z+h),(x,y-d*.62,z+h+.23),(x-w*.62,y+d*.62,z+h),(x+w*.62,y+d*.62,z+h),(x,y+d*.62,z+h+.23)]
 me=bpy.data.meshes.new('Gable roof');me.from_pydata(verts,[],[(0,1,2),(5,4,3),(0,3,4,1),(1,4,5,2),(2,5,3,0)]);me.update();o=bpy.data.objects.new('Village / roof '+str(i),me);bpy.context.collection.objects.link(o);me.materials.append(roofmat);parent(o)
 cube('Village / door '+str(i),(x,y-d/2-.006,z+.085),(.09,.018,.17),end,lid,.002)
 for dx in [-.17,.17]:cube('Village / window',(x+dx,y-d/2-.007,z+.20),(.075,.02,.075),gold,lid,.002)
''' +s[b:]
s=s.replace("location=(-5.6,-7.8,4.5)","location=(-5.6,-7.8,6.6)")
s=s.replace("scene.cycles.samples=32;scene.render.resolution_x=1100;scene.render.resolution_y=1000", "scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.render.resolution_x=960;scene.render.resolution_y=880")
(R/'author.py').write_text(s,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
print('Germany scripts prepared; original pilots untouched')
