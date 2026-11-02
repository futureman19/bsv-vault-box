"""Script-authored Kuwait Sadu & Sand. No scans or photographic textures."""
from pathlib import Path
exec((Path(__file__).resolve().parent/'author-helpers.txt').read_text())
wood=mat('Wood / dark warm frame',(.12,.06,.03),.52);maptex(wood,'wood-color.png','Base Color')
textile=mat('Sadu / invented woven bands',(.4,.05,.03),.86);maptex(textile,'sadu-color.png','Base Color');maptex(textile,'sadu-roughness.png','Roughness',True)
sand=mat('Sand / sculpted desert relief',(.57,.38,.18),.84);maptex(sand,'sand-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / charcoal',(.025,.018,.014),.9)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o,'Y' if 'end' in o.name else 'X')
# Continuous wooden backing with textile faces inset between frame rails.
for sy in [-1,1]:
 cube('Body / wood backing',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.015)
 panel=cube('Sadu / front panel' if sy<0 else 'Sadu / rear panel',(0,sy*1.245,.83),(3.28,.018,1.20),textile,bevel=.003)
 for z in [.17,1.49]:cube('Frame / horizontal rail',(0,sy*1.26,z),(3.72,.065,.12),wood,bevel=.015)
for sx in [-1,1]:
 cube('Body / side backing',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.015,axis='Y')
 cube('Sadu / side panel',(sx*1.869,0,.83),(.018,2.04,1.20),textile,bevel=.003,axis='Y')
 for z in [.17,1.49]:cube('Frame / side rail',(sx*1.885,0,z),(.065,2.38,.12),wood,bevel=.015,axis='Y')
 for sy in [-1,1]:
  cube('Frame / corner post',(sx*1.745,sy*1.20,.83),(.23,.14,1.34),wood,bevel=.015)
  cube('Brass / foot',(sx*1.47,sy*.91,-.10),(.39,.36,.34),gold,bevel=.055)
  cube('Brass / corner shoe',(sx*1.75,sy*1.265,.25),(.20,.035,.23),gold,bevel=.01)
cube('Wood / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.08),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.08),seam,bevel=.009)
 for sy in [-1,1]:cube('Frame / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
for sy in [-1,1]:cube('Sadu / lid band',(0,sy*.94,1.985),(3.20,.22,.012),textile,lid,.003)
for sx in [-1,1]:
 cube('Sadu / lid side band',(sx*1.52,0,1.985),(.22,1.65,.012),textile,lid,.003,axis='Y')
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# Low, watertight relief with three asymmetric curved crests, no display plinth.
nx,ny=64,36;verts=[];faces=[]
for j in range(ny+1):
 y=-.65+1.3*j/ny
 for i in range(nx+1):
  x=-1.25+2.5*i/nx
  fade=max(0,math.sin(math.pi*i/nx)*math.sin(math.pi*j/ny))**.65
  crest=sum(amp*math.exp(-((y-(yc+.15*math.sin(x*2.2+phase)))/width)**2) for yc,amp,width,phase in [(-.35,.23,.14,.2),(.03,.32,.15,1.4),(.38,.20,.12,2.6)])
  verts.append((x,y,1.981+fade*(.025+crest)))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
# Seal the bottom with perimeter walls and a downward-facing n-gon.
edge=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
bottom=[]
for idx in edge:bottom.append(len(verts));x,y,z=verts[idx];verts.append((x,y,1.975))
for k in range(len(edge)):
 q=(k+1)%len(edge);faces.append((edge[k],bottom[k],bottom[q],edge[q]))
faces.append(tuple(reversed(bottom)))
me=bpy.data.meshes.new('Dune sculpt / three crests');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Dune / sculpted relief',me);bpy.context.collection.objects.link(o);me.materials.append(sand);uv(o);parent(o,lid)
for f in me.polygons:f.use_smooth=len(f.vertices)==4
exec((R/'author-studio.txt').read_text())
