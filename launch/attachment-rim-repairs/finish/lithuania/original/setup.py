from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; B=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','viewer.js','template.html','build.py','verify_source.py','verify_parity.py','verify_browser.py','package.json','THREE-LICENSE.txt']:
 if n.endswith(('.blend','.txt')):shutil.copy2(B/n,R/n);continue
 s=(B/n).read_text();s=s.replace('japan-cedar-v1','lithuania-v1').replace('japan.blend','lithuania.blend').replace('japan.glb','lithuania.glb').replace('Japan / Cedar & Moss','Lithuania / Curonian Dune & Lagoon').replace('Japan Cedar and Moss','Lithuania Curonian Dune and Lagoon').replace('Yakushima cedar. Mossed granite. Quiet brass.','Wind-shaped sand. Sheltered lagoon. Quiet brass.').replace('the original Japan concept','the Curonian coastal landscape').replace('JAPAN ·','LITHUANIA ·')
 (R/n).write_text(s)
s=(B/'author.py').read_text();s=s[:s.index('wood=mat')]+s[s.index('def uv('):s.index('for o in bpy.data.objects:')]+'''sand=mat('Sand / wind ripple',(.65,.49,.28),.8);maptex(sand,'sand-color.png','Base Color');maptex(sand,'sand-roughness.png','Roughness',True)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Lagoon / dark seam',(.025,.07,.065),.7)
water=mat('Lagoon / teal ceramic',(.035,.24,.25),.24);maptex(water,'lagoon.png','Base Color')
green=mat('Dune / stabilization green',(.08,.15,.065),.9)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(sand if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Sand body / long',(0,sy*1.145,.83),(3.72,.19,1.46),sand,bevel=.025)
for sx in [-1,1]:cube('Sand body / end',(sx*1.745,0,.83),(.23,2.48,1.46),sand,bevel=.025)
cube('Sand / clasp seat',(0,-1.255,1.36),(.56,.075,.47),sand,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / end',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:
  cube('Sand / rim',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),sand,bevel=.004)
  cube('Sand / foot',(sx*1.47,sy*.91,-.08),(.55,.46,.32),sand,bevel=.05)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),sand,lid,.045)
cube('Lagoon / inset',(0,0,1.988),(3.16,1.8,.022),water,lid,.008)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# Closed curved dune volume. Sand ridges are geometry, not painted terrain.
verts=[];faces=[];nx=64;ny=16
for i in range(nx+1):
 x=-1.4+2.8*i/nx;u=i/nx;cy=.15*math.sin(u*math.pi*1.7);width=.24+.07*math.sin(math.pi*u)
 for j in range(ny+1):
  t=-1+2*j/ny;y=cy+t*width
  z=2.035+.40*max(0,math.sin(math.pi*u))**.65*max(0,1-abs(t)**1.4)*(.83+.17*math.sin(u*math.pi*3))
  verts.append((x,y,z))
for i in range(nx):
 for j in range(ny):
  a=i*(ny+1)+j;faces.append((a,a+ny+1,a+ny+2,a+1))
border=list(range(ny+1))+[i*(ny+1)+ny for i in range(1,nx+1)]+[nx*(ny+1)+j for j in range(ny-1,-1,-1)]+[i*(ny+1) for i in range(nx-1,0,-1)]
for k,a in enumerate(border):
 b=border[(k+1)%len(border)];v=len(verts);verts.extend([(verts[a][0],verts[a][1],1.995),(verts[b][0],verts[b][1],1.995)]);faces.append((a,v,v+1,b))
me=bpy.data.meshes.new('Curved dune volume');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Dune / continuous ridge',me);bpy.context.collection.objects.link(o);me.materials.append(sand);uv(o);parent(o)
for f in me.polygons:f.use_smooth=True
# Coherent shoulder planting: low irregular clusters rooted into sand.
for i in range(22):
 u=.13+.74*i/21;x=-1.4+2.8*u;cy=.15*math.sin(u*math.pi*1.7);t=.72;y=cy+t*(.24+.07*math.sin(math.pi*u));z=2.035+.40*math.sin(math.pi*u)**.65*(1-t**1.4)*(.83+.17*math.sin(u*math.pi*3))
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=1,location=(x,y,z));o=bpy.context.object;o.name='Vegetation / shoulder';o.scale=(.09,.065,.055);o.data.materials.append(green);parent(o)
'''+s[s.index('# Clean obsolete'):]
s=s.replace('japan.blend','lithuania.blend').replace('japan.glb','lithuania.glb').replace('JAPAN AUTHORED','LITHUANIA AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4').replace('location=(-5.6,-7.8,4.5)','location=(-5.6,-7.8,6.5)')
(R/'author.py').write_text(s)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
# Improve default terrain visibility.
p=R/'viewer.js';s=p.read_text().replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.3,7)');p.write_text(s)
print('Scoped pipeline prepared')
