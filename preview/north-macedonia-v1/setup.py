from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for f in ['mechanism.blend','THREE-LICENSE.txt','package.json','motion.mjs']:
 shutil.copy2(S/f,R/f)
for f in ['viewer.js','template.html','build.py','verify_browser.py','verify_source.py','verify_parity.py']:
 t=(S/f).read_text(encoding='utf8').replace('japan-cedar-v1','north-macedonia-v1').replace('japan.glb','north-macedonia.glb').replace('japan.blend','north-macedonia.blend').replace('Japan / Cedar & Moss','North Macedonia / Ohrid').replace('Yakushima cedar. Mossed granite. Quiet brass.','Ancient lake blue. Pale mineral shores. Quiet brass.').replace('original Japan concept','Ohrid landscape written brief').replace('JAPAN','NORTH MACEDONIA')
 (R/f).write_text(t,encoding='utf8')
a=(S/'author.py').read_text();a=a[:a.index('wood=mat')]+'''stone_mat=mat('Limestone / pale mineral',(.65,.60,.48),.7);maptex(stone_mat,'stone-color.png','Base Color');maptex(stone_mat,'stone-roughness.png','Roughness',True)
granite=stone_mat;wood=stone_mat
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / deep teal',(.025,.065,.065),.8)
water=mat('Ohrid / lake blue',(.025,.24,.38),.21);maptex(water,'lake-color.png','Base Color')
'''+a[a.index('def uv('):a.index('# Exterior skins')]+'''for sy in [-1,1]:cube('Limestone / long wall',(0,sy*1.145,.83),(3.72,.19,1.46),stone_mat,bevel=.018)
for sx in [-1,1]:cube('Limestone / end wall',(sx*1.745,0,.83),(.23,2.10,1.46),stone_mat,bevel=.018)
'''+a[a.index('# Small collar'):a.index('# A thin satin')]+a[a.index('# Restrained brass'):a.index("stone('Terrain / granite'")]+'''# Low irregular lake polygon and surrounding mineral shore.
def polygon(n,scale,z,material):
 pts=[]
 for i in range(64):
  a=i*math.tau/64;r=1+.07*math.sin(3*a)+.04*math.cos(7*a)
  pts.append((math.cos(a)*scale[0]*r,math.sin(a)*scale[1]*r,z))
 me=bpy.data.meshes.new(n);me.from_pydata([(0,0,z)]+pts,[],[(0,i+1,(i+1)%64+1) for i in range(64)]);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o);return o
polygon('Shore / irregular limestone',(1.48,.87),1.988,stone_mat)
polygon('Lake / continuous blue inset',(1.29,.69),1.996,water)
for i,(x,y,s) in enumerate([(-.92,.69,.20),(-.35,.79,.35),(.30,.83,.24)]):
 stone('Ridge / limestone '+str(i),(x,y,2.02),(.40,.22,s),lid,stone_mat,2)
'''+a[a.index('# Medallion is solid'):]
a=a.replace('japan.blend','north-macedonia.blend').replace('japan.glb','north-macedonia.glb').replace('JAPAN AUTHORED','NORTH MACEDONIA AUTHORED').replace('Cedar /','Limestone /').replace('Granite foot','Limestone foot')
a=a.replace("scene.cycles.samples=32;", "scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;")
a=a.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z", "u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z")
(R/'author.py').write_text(a)
(R/'.gitattributes').write_text('* -text\n')
print('SETUP PASS')
