from pathlib import Path
import shutil
R=Path(__file__).resolve().parent;S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','package.json','motion.mjs','verify_source.py','verify_parity.py','verify_browser.py','build.py','viewer.js','template.html']:
 if name.endswith(('.blend','.txt')):shutil.copy2(S/name,R/name);continue
 t=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','united-kingdom-v1').replace('japan.glb','united-kingdom.glb').replace('japan.blend','united-kingdom.blend').replace('Japan / Cedar & Moss','United Kingdom / Slate & Walled Meadows').replace('Japan Cedar and Moss','United Kingdom Slate and Walled Meadows').replace('Yakushima cedar. Mossed granite. Quiet brass.','Blue slate. Walled meadows. Satin brass.').replace('inspired by the original Japan concept','inspired by Welsh slate and dry-stone field landscapes').replace('JAPAN ·','UNITED KINGDOM ·')
 (R/name).write_text(t,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n')
s=(S/'author.py').read_text();head=s[:s.index('wood=mat(')]
helpers=s[s.index('def uv('):s.index('for o in bpy.data.objects:')].replace('m.segments=3','m.segments=1')
helpers=helpers.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z", "u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z")
stone=s[s.index('def stone('):s.index("stone('Terrain / granite'")]
end=s[s.index('# Medallion is solid'):].replace('japan','united-kingdom').replace('JAPAN','UNITED KINGDOM').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=4;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
materials="""wood=mat('Slate / blue charcoal cleavage',(.18,.20,.25),.68);maptex(wood,'slate-color.png','Base Color');maptex(wood,'slate-roughness.png','Roughness',True)
granite=mat('Wall stone / weathered grey',(.31,.33,.29),.88);maptex(granite,'wall-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / dark green',(.035,.07,.032),.9)
fields=[mat('Meadow / '+str(i),c,.93) for i,c in enumerate([(.12,.21,.055),(.17,.25,.075),(.095,.17,.04),(.20,.28,.085)])]
"""
body="""for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(wood if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Staggered slate joints; continuous inherited liner remains behind them.
for row in range(6):
 z=.10+(row+.5)*1.46/6;h=1.46/6-.012
 for sy in [-1,1]:
  edges=[-1.86]+[x for x in [-1.86+.45*(row%2)+j*.62 for j in range(1,7)] if -1.85<x<1.85]+[1.86]
  for a,b in zip(edges,edges[1:]):cube('Slate / front' if sy<0 else 'Slate / rear',((a+b)/2,sy*1.145,z),(b-a-.012,.19,h),wood,bevel=.009)
 for sx in [-1,1]:
  edges=[-1.04]+[x for x in [-1.04+.20*(row%2)+j*.53 for j in range(1,5)] if -1.03<x<1.03]+[1.04]
  for a,b in zip(edges,edges[1:]):cube('Slate / side',(sx*1.745,(a+b)/2,z),(.23,b-a-.012,h),wood,bevel=.009)
cube('Slate / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Slate / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
"""
terrain="""def height(x,y):
 return 2.005+.28*math.exp(-((x-.65)**2/.55+(y-.32)**2/.45))+.13*math.exp(-((x+.8)**2/.3+(y+.2)**2/.6))
verts=[];faces=[];nx=40;ny=24
for j in range(ny+1):
 for i in range(nx+1):
  x=-1.45+2.9*i/nx;y=-.85+1.7*j/ny;verts.append((x,y,height(x,y)))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
me=bpy.data.meshes.new('Rolling meadow grid');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Terrain / walled meadows',me);bpy.context.collection.objects.link(o);parent(o)
for m in fields:me.materials.append(m)
for f in me.polygons:
 c=f.center;f.material_index=(int(c.x>-.2)+2*int(c.y>.08));f.use_smooth=True
# Exposed terrain edge connects relief down into slab.
boundary=[verts[i] for i in range(nx+1)]+[verts[j*(nx+1)+nx] for j in range(1,ny+1)]+[verts[ny*(nx+1)+i] for i in range(nx-1,-1,-1)]+[verts[j*(nx+1)] for j in range(ny-1,0,-1)]
v=[];f=[]
for p in boundary:v.extend([p,(p[0],p[1],1.975)])
for i in range(len(boundary)):a=2*i;b=2*((i+1)%len(boundary));f.append((a,b,b+1,a+1))
me=bpy.data.meshes.new('Terrain edge');me.from_pydata(v,[],f);me.update();o=bpy.data.objects.new('Terrain / slate edge',me);bpy.context.collection.objects.link(o);me.materials.append(wood);uv(o);parent(o)
for axis,count in [('X',22),('Y',12)]:
 for i in range(count):
  x=-1.37+i*2.74/(count-1) if axis=='X' else -.2
  y=.08 if axis=='X' else -.77+i*1.54/(count-1)
  if axis=='Y' and abs(y-.08)<.13:continue
  z=height(x,y)
  for row in range(2):cube('Field wall / course',(x,y,z+.035+row*.055),(.12,.075,.065) if axis=='X' else (.075,.12,.065),granite,lid,.008)
  cube('Field wall / upright coping',(x,y,z+.155),(.075,.085,.11) if axis=='X' else (.085,.075,.11),granite,lid,.009)
"""
(R/'author.py').write_text(head.replace('Reference-led Japan pilot','Brief-led UK pilot')+materials+helpers+body+stone+terrain+end)
print('Prepared UK source pipeline')
