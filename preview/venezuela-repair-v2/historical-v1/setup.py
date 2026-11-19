"""One-time adaptation of read-only Japan mechanical/viewer lineage."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','package.json','motion.mjs','viewer.js','template.html','build.py','verify_source.py','verify_parity.py','verify_browser.py']:
 if name.endswith(('.py','.js','.mjs','.html')):
  s=(S/name).read_text();s=s.replace('japan-cedar-v1','venezuela-v1').replace('japan.glb','venezuela.glb').replace('japan.blend','venezuela.blend').replace('Japan / Cedar & Moss','Venezuela / Tepui & Cascade').replace('Yakushima cedar. Mossed granite. Quiet brass.','Sandstone heights. Pale cascades. Quiet brass.').replace('the original Japan concept','the Canaima landscape brief').replace('JAPAN ·','VENEZUELA ·').replace('Japan','Venezuela')
  (R/name).write_text(s)
 else:shutil.copy2(S/name,R/name)
a=(S/'author.py').read_text();a=a[:a.index('wood=mat')]+a[a.index('def uv('):a.index('for o in bpy.data.objects:')]+'''stone_mat=mat('Sandstone / weathered strata',(.4,.18,.10),.82)
maptex(stone_mat,'stone-color.png','Base Color');maptex(stone_mat,'stone-roughness.png','Roughness',True)
cap=mat('Summit / olive vegetation',(.10,.16,.055),.92);maptex(cap,'summit.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Weathered dark seam',(.045,.035,.025),.92)
water=mat('Cascade / pale mineral water',(.58,.78,.79),.22)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone_mat if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
for sy in [-1,1]:cube('Sandstone / wall',(0,sy*1.145,.83),(3.72,.19,1.46),stone_mat,bevel=.016)
for sx in [-1,1]:cube('Sandstone / side',(sx*1.745,0,.83),(.23,2.10,1.46),stone_mat,bevel=.016)
cube('Sandstone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone_mat,bevel=.025)
for sy in [-1,1]:cube('Weathered seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Weathered seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Sandstone / rim',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone_mat,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone_mat,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Stone foot',(sx*1.47,sy*.91,-.10),(.55,.46,.35),stone_mat,bevel=.09)
# Irregular flat-topped cliff: disconnected strata are not used; one closed solid.
outline=[(-.95,-.40),(-.55,-.52),(-.12,-.50),(.25,-.42),(.77,-.38),(.91,-.05),(.79,.52),(.34,.64),(-.25,.59),(-.82,.42),(-1.01,.08)]
verts=[];faces=[];N=len(outline)
for z,scale in [(1.97,1.05),(2.15,1.0),(2.48,.98),(2.82,.93)]:
 for x,y in outline:verts.append((x*scale+.15,y*scale+.15,z))
faces.append(tuple(reversed(range(N))))
for k in range(3):
 for j in range(N):faces.append((k*N+j,k*N+(j+1)%N,(k+1)*N+(j+1)%N,(k+1)*N+j))
faces.append(tuple(3*N+j for j in range(N)))
me=bpy.data.meshes.new('Tepui cliff');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Tepui / sandstone massif',me);bpy.context.collection.objects.link(o);me.materials.append(stone_mat);uv(o);parent(o)
# Thin summit polygon cap, inset to preserve bare cliff edge.
v=[(x*.88+.15,y*.88+.15,2.824) for x,y in outline];me=bpy.data.meshes.new('Summit');me.from_pydata(v,[],[tuple(range(N))]);me.update();o=bpy.data.objects.new('Tepui / summit vegetation',me);bpy.context.collection.objects.link(o);me.materials.append(cap);uv(o);parent(o)
# Continuous narrow water ribbon from summit over front cliff into a lid basin.
points=[(-.12,-.12,2.838),(-.12,-.30,2.838),(-.12,-.355,2.81),(-.12,-.38,2.50),(-.12,-.40,2.17),(-.12,-.48,2.015),(-.12,-.72,2.015)]
v=[]
for x,y,z in points:v.extend([(x-.027,y,z),(x+.027,y,z)])
f=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(points)-1)];me=bpy.data.meshes.new('Cascade');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new('Tepui / continuous cascade',me);bpy.context.collection.objects.link(o);me.materials.append(water);parent(o)
bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=12,radius=1,location=(-.12,-.73,2.003));o=bpy.context.object;o.name='Tepui / basin';o.scale=(.25,.18,.025);select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(water);parent(o)
'''+a[a.index('# Medallion is solid'):]
a=a.replace('japan.blend','venezuela.blend').replace('japan.glb','venezuela.glb').replace('JAPAN AUTHORED','VENEZUELA AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
# Stone UVs use dominant-face projection rather than wood-oriented axes.
a=a.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z", "u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z")
a=a.replace('Reference-led Japan pilot.','Brief-led Venezuela pilot.')
(R/'author.py').write_text(a)
(R/'.gitattributes').write_text('* -text\n')
print('Adapted lineage; no historical evidence copied')
