stone=mat('Limestone / mottled ashlar',(.55,.52,.46),.82);maptex(stone,'stone-color.png','Base Color');maptex(stone,'stone-roughness.png','Roughness',True)
roofmat=mat('Slate / silver grey',(.18,.22,.26),.69);maptex(roofmat,'slate-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / charcoal',(.025,.031,.035),.9)
plaster=mat('House / warm pale limestone',(.66,.62,.52),.88)
window=mat('House / recessed dark glazing',(.025,.046,.06),.32)
# HELPERS
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Butt-jointed stone skins, not overlapping exterior faces.
for sy in [-1,1]:cube('Stone / front' if sy<0 else 'Stone / rear',(0,sy*1.095,.83),(3.32,.19,1.46),stone,bevel=.015)
for sx in [-1,1]:cube('Stone / side',(sx*1.76,0,.83),(.20,2.38,1.46),stone,bevel=.015)
cube('Stone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Stone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),roofmat,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Stone / foot',(sx*1.47,sy*.91,-.08),(.50,.42,.32),stone,bevel=.06)
# Solid closed hipped roof, layered overhanging slab courses.
def hip(n,x,y,z,w,d,h):
 vs=[(x-w/2,y-d/2,z),(x+w/2,y-d/2,z),(x+w/2,y+d/2,z),(x-w/2,y+d/2,z),(x-.16*w,y,z+h),(x+.16*w,y,z+h)]
 faces=[(3,2,1,0),(0,1,5,4),(1,2,5),(2,3,4,5),(3,0,4)]
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(roofmat);uv(o);parent(o);return o
for i,(x,y,h) in enumerate([(-.95,.20,.45),(0,.35,.64),(.95,.20,.48)]):
 z=1.978
 cube(f'House {i} / walls',(x,y,z+h/2),(.65,.58,h),plaster,lid,.012)
 # Three progressively smaller closed stone roof tiers preserve a stepped silhouette.
 for k in range(3):hip(f'House {i} / roof {k}',x,y,z+h+k*.065,.78-k*.16,.72-k*.17,.22-k*.04)
 for dx in [-.18,.18]:
  cube(f'House {i} / front window',(x+dx,y-.295,z+h*.65),(.10,.018,.15),window,lid,.003)
  cube(f'House {i} / side window',(x-.33,y+dx,z+h*.65),(.018,.10,.15),window,lid,.003)
 cube(f'House {i} / door',(x,y-.298,z+.10),(.11,.018,.20),window,lid,.003)
