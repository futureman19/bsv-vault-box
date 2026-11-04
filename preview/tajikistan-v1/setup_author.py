"""Derive reusable helper/mechanical sections, never copy Japan artwork."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
start=s[s.index('import bpy'):s.index('wood=mat')]
materials='''wood=mat('Pamir / mineral stone',(.3,.28,.25),.65);maptex(wood,'stone-color.png','Base Color');maptex(wood,'stone-roughness.png','Roughness',True)
granite=mat('Pamir / granular rock',(.26,.25,.23),.8);maptex(granite,'mineral.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / charcoal',(.035,.04,.045),.9)
snow=mat('Pamir / ivory snow',(.85,.90,.94),.74)
water=mat('Pamir / alpine blue',(.018,.23,.34),.20,.12)
'''
helpers=s[s.index('def uv('):s.index('# Exterior skins')]
# Replace wood-oriented projection by physical face projection.
a=helpers.index('   u=');b=helpers.index('\ndef cube',a)
helpers=helpers[:a]+'''   if abs(p.normal.z)>.7: u,v=co.x,co.y
   elif abs(p.normal.x)>.7: u,v=co.y,co.z
   else: u,v=co.x,co.z
   layer.data[li].uv=(u/1.4+.5,v/1.4+.5)
'''+helpers[b:]
body='''for sy in [-1,1]:cube('Mineral body / long',(0,sy*1.095,.83),(3.72,.19,1.46),wood,bevel=.025)
for sx in [-1,1]:cube('Mineral body / end',(sx*1.745,0,.83),(.23,2.0,1.46),wood,bevel=.025)
'''
rim=s[s.index('# Small collar'):s.index('# A thin satin')].replace('Cedar /','Mineral body /')
corners=s[s.index('# Restrained brass'):s.index('def stone')]
stone=s[s.index('def stone'):s.index("stone('Terrain / granite'")]
terrain='''# Continuous closed ridge relief, with three asymmetric summits.
verts=[]; faces=[]; nx=64; ny=28
for j in range(ny+1):
 t=j/ny; y=-.10+1.04*t
 for i in range(nx+1):
  x=-1.45+2.9*i/nx
  envelope=max(0,math.sin(math.pi*i/nx))*max(0,math.sin(math.pi*t))
  peaks=sum(h*math.exp(-((x-c)/w)**2) for c,h,w in [(-.94,.60,.28),(-.10,.85,.32),(.91,.67,.29)])
  z=1.986+envelope**.55*(.07+peaks*(.72+.28*math.sin(t*math.pi))+.035*math.sin(x*34+t*13))
  verts.append((x,y,z))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.extend([(a,a+1,a+nx+2),(a,a+nx+2,a+nx+1)])
bound=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
base=len(verts)
for i in bound:verts.append((verts[i][0],verts[i][1],1.972))
for k,a in enumerate(bound):
 q=(k+1)%len(bound);faces.append((a,base+k,base+q,bound[q]))
faces.append(tuple(reversed(range(base,len(verts)))))
me=bpy.data.meshes.new('Pamir ridge closed relief');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / Pamir ridge',me);bpy.context.collection.objects.link(o);me.materials.append(granite);me.materials.append(snow);uv(o)
for f in me.polygons:
 z=sum(me.vertices[i].co.z for i in f.vertices)/len(f.vertices)
 x=sum(me.vertices[i].co.x for i in f.vertices)/len(f.vertices)
 f.material_index=1 if z>2.43+.065*math.sin(x*17) else 0
parent(o)
# Single irregular lake inset: 64 perimeter points, actual raised blue surface.
v=[(.10,-.48,2.002)];n=64
for i in range(n):
 a=i*math.tau/n;r=1+.08*math.sin(3*a)+.045*math.sin(7*a)
 v.append((.10+.82*r*math.cos(a),-.48+.32*r*math.sin(a),2.002))
f=[(0,i+1,(i+1)%n+1) for i in range(n)]
me=bpy.data.meshes.new('Alpine lake surface');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new('Terrain / Alpine lake',me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o)
'''
end=s[s.index('# Medallion'):].replace('japan.blend','tajikistan.blend').replace('japan.glb','tajikistan.glb').replace('JAPAN AUTHORED','TAJIKISTAN AUTHORED').replace('location=(-5.6,-7.8,4.5)','location=(-5.6,-7.8,6.2)').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=1000').replace('resolution_y=1000','resolution_y=900')
(R/'author.py').write_text('"""Tajikistan procedural source author. Frozen brief precedes model."""\n'+start+materials+helpers+body+rim+corners+stone+terrain+end)
print('Created self-contained author.py; setup helper depends on repository Japan source only.')
