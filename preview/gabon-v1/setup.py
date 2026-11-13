from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for f in ['mechanism.blend','viewer.js','motion.mjs','template.html','build.py','verify_source.py','verify_parity.py','verify_browser.py','package.json','THREE-LICENSE.txt','maps.py','author.py']:
 if f.endswith(('.py','.js','.html','.json','.mjs')):
  t=(S/f).read_text(encoding='utf8').replace('japan-cedar-v1','gabon-v1').replace('japan.glb','gabon.glb').replace('japan.blend','gabon.blend').replace('Japan','Gabon').replace('JAPAN','GABON').replace('Cedar &amp; Moss','Okoume &amp; Loango').replace('Cedar & Moss','Okoume & Loango').replace('Cedar','Okoume').replace('cedar','okoume')
  (R/f).write_text(t,encoding='utf8')
 else:shutil.copy2(S/f,R/f)
p=R/'maps.py';t=p.read_text().replace('167*v,87*v,46*v','178*v,118*v,92*v').replace('y*115+0.5*np.sin(x*9+y*8)+.16*np.sin(x*21+y*15)','y*85+1.2*np.sin(x*7+y*5)+.35*np.sin(x*19+y*11)');p.write_text(t)
p=R/'author.py';t=p.read_text();a=t.index('# Exterior skins');b=t.index('# Small collar');t=t[:a]+'''# Continuous okoume panels, no cedar finger-joint composition.
for sy in [-1,1]:cube('Okoume / '+('front' if sy<0 else 'rear'),(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.025)
for sx in [-1,1]:cube('Okoume / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.025,axis='Y')
'''+t[b:];a=t.index('# A thin satin');b=t.index('# Restrained brass');t=t[:a]+t[b:];t=t.replace('.108)', '.080)');a=t.index("stone('Terrain / granite'");b=t.index('def tube',a);t=t[:a]+t[b:];a=t.index('trunk=[');b=t.index('# Medallion',a);t=t[:a]+'''# Loango-inspired abstract coast: a continuous lagoon and raised sand shores.
water=mat('Lagoon / blue green',(.025,.115,.13),.23,.15)
sand=mat('Coast / warm sand',(.48,.37,.22),.84)
def ribbon(name,width,z,material):
 verts=[];faces=[]
 for i in range(41):
  x=-1.45+i*2.9/40; y=-.20+.23*math.sin(x*2.25)
  verts.extend([(x,y-width/2,z),(x,y+width/2,z)])
 for i in range(40):faces.append((2*i,2*i+2,2*i+3,2*i+1))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(material);parent(o)
 return o
ribbon('Coast / sand bank',.49,1.988,sand)
ribbon('Lagoon / continuous winding water',.30,1.994,water)
# Low forested rear bank and three broadleaf tree groupings.
for k,(x,y,h) in enumerate([(-.98,.48,.51),(-.12,.65,.66),(.84,.51,.57)]):
 stone('Coast / forest bank '+str(k),(x,y,2.035),(.46,.35,.09),lid,moss,2)
 tube('Forest / trunk '+str(k),[(x,y,2.04),(x+.035,y,2.20),(x-.025,y,2.0+h)],[.047,.035,.018],bark)
 for j in range(5):
  az=j*math.tau/5;tx=x+math.cos(az)*.23;ty=y+math.sin(az)*.19;z=2.0+h-.06+random.uniform(-.05,.04)
  tube('Forest / branch',[(x,y,2.20),(tx,ty,z)],[.022,.009],bark,sides=7)
  stone('Forest / canopy '+str(k),(tx,ty,z),(.25,.20,.105),lid,leafm[(j+k)%4],2)
'''+t[b:];t=t.replace("print('GABON AUTHORED')","print('GABON AUTHORED')");p.write_text(t)
print('Gabon source and inherited mechanics/viewer prepared')
