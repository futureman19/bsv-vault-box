"""Build a standalone author script from the reviewed mechanism helper lineage."""
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
head=s[:s.index('wood=mat')]
helpers=s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
tube=s[s.index('def tube('):s.index('trunk=[')]
disk=s[s.index('def disk('):s.index('# Clean obsolete')]
end=s[s.index('# Clean obsolete'):].replace('japan','mongolia').replace('JAPAN','MONGOLIA').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
body='''
felt=mat('Felt / ivory fibers',(.65,.58,.42),.88);maptex(felt,'felt-color.png','Base Color');maptex(felt,'felt-roughness.png','Roughness',True)
wood=mat('Frame / ochre red lacquer',(.25,.055,.022),.38)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / midnight blue',(.018,.047,.065),.85)
grass=mat('Steppe / olive grass',(.18,.23,.055),.95);maptex(grass,'steppe-color.png','Base Color')
stone=mat('Foot / dark stone',(.07,.065,.05),.85)
rope=mat('Ger / dark ropes',(.085,.055,.025),.85)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
for sy in [-1,1]:
 cube('Felt / long panel',(0,sy*1.145,.83),(3.72,.19,1.46),felt,bevel=.025)
 for z in [.16,1.49]:cube('Frame / long rail',(0,sy*1.247,z),(3.72,.035,.11),wood,bevel=.012)
for sx in [-1,1]:
 cube('Felt / side panel',(sx*1.745,0,.83),(.23,2.10,1.46),felt,bevel=.025,axis='Y')
 for z in [.16,1.49]:cube('Frame / side rail',(sx*1.875,0,z),(.035,2.38,.11),wood,bevel=.012)
 for sy in [-1,1]:
  cube('Frame / corner binding',(sx*1.74,sy*1.248,.83),(.12,.04,1.46),wood,bevel=.01)
  cube('Stone foot',(sx*1.47,sy*.91,-.10),(.48,.42,.29),stone,bevel=.08)
cube('Frame / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Frame / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# Closed oval relief: top rings plus skirt reaching the actual lid.
verts=[(0,0,2.10)];faces=[];rings=12;segs=80
for k in range(1,rings+1):
 r=k/rings
 for j in range(segs):
  a=j*math.tau/segs;x=1.48*r*math.cos(a);y=.83*r*math.sin(a)
  z=2.06+.045*math.sin(x*2.7)*math.cos(y*3.1)
  if (x-.55)**2+(y-.25)**2<.46**2:z=2.10
  verts.append((x,y,z))
for j in range(segs):faces.append((0,1+j,1+(j+1)%segs))
for k in range(rings-1):
 for j in range(segs):
  a=1+k*segs+j;b=1+k*segs+(j+1)%segs;faces.append((a,a+segs,b+segs,b))
start=len(verts)
for j in range(segs):a=j*math.tau/segs;verts.append((1.48*math.cos(a),.83*math.sin(a),1.97))
for j in range(segs):a=1+(rings-1)*segs+j;b=1+(rings-1)*segs+(j+1)%segs;faces.append((a,start+j,start+(j+1)%segs,b))
faces.append(tuple(reversed(range(start,start+segs))))
me=bpy.data.meshes.new('Steppe closed relief');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Steppe / rolling oval',me);bpy.context.collection.objects.link(o);me.materials.append(grass);uv(o);parent(o)
def cone(n,z,r1,r2,depth,material):
 bpy.ops.mesh.primitive_cone_add(vertices=64,radius1=r1,radius2=r2,depth=depth,location=(.55,.25,z));o=bpy.context.object;o.name=n;o.data.materials.append(material);uv(o);parent(o)
 for p in o.data.polygons:p.use_smooth=len(p.vertices)==4
 return o
cone('Ger / felt wall',2.25,.40,.40,.30,felt)
cone('Ger / peaked felt roof',2.525,.42,.105,.25,felt)
cone('Ger / crown',2.655,.105,.105,.018,wood)
cube('Ger / red door',(.55,-.153,2.235),(.16,.018,.25),wood,lid,.008)
cube('Ger / door brass pull',(.595,-.169,2.235),(.013,.015,.035),gold,lid,.004)
for z in [2.17,2.34]:
 bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=6,major_radius=.401,minor_radius=.009,location=(.55,.25,z));o=bpy.context.object;o.name='Ger / rope band';o.data.materials.append(rope);parent(o)
'''
cords='''
for j in range(12):
 a=j*math.tau/12
 tube('Ger / roof cord',[(.55+.108*math.cos(a),.25+.108*math.sin(a),2.654),(.55+.425*math.cos(a),.25+.425*math.sin(a),2.403)],[.005,.005],rope,sides=6)
'''
(R/'author.py').write_text(head+helpers+body+tube+cords+disk+end)
print('Standalone author.py created')
