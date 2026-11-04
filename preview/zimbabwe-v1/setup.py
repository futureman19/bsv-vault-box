"""Adapt the read-only Japan mechanical/viewer lineage into this new pilot."""
from pathlib import Path
R=Path(__file__).resolve().parent
for name in ['viewer.js','template.html','verify_source.py','verify_parity.py','verify_browser.py','build.py']:
 p=R/name;s=p.read_text(encoding='utf8').replace('japan-cedar-v1','zimbabwe-v1').replace('japan.blend','zimbabwe.blend').replace('japan.glb','zimbabwe.glb').replace('Japan Cedar and Moss','Zimbabwe Granite and Kopjes').replace('Japan / Cedar & Moss','Zimbabwe / Granite & Kopjes').replace('Yakushima cedar. Mossed granite. Quiet brass.','Granite courses. Weathered kopjes. Satin brass.').replace('inspired by the original Japan concept','inspired by Zimbabwe’s granite masonry and landforms').replace('JAPAN ·','ZIMBABWE ·')
 s=s.replace('h1{font-siz... [truncated]','h1{font-size:30px}.foot{flex-direction:column;gap:12px}}')
 p.write_text(s,encoding='utf8')
p=R/'verify_browser.py';s=p.read_text().replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1',timeout=5000);assert page.evaluate('pilot.progress')==1").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0',timeout=5000);assert page.evaluate('pilot.progress')==0")
p.write_text(s)
# Reuse helpers and inherited physical fittings; replace all cedar geometry.
s=(R.parent/'japan-cedar-v1/author.py').read_text()
s=s[:s.index('wood=mat')]+'''stone_mat=mat('Granite / warm mineral grain',(.34,.29,.22),.8);maptex(stone_mat,'granite-color.png','Base Color');maptex(stone_mat,'granite-roughness.png','Roughness',True)
liner=mat('Interior / dark granite',(.12,.105,.08),.8);maptex(liner,'liner-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / charcoal olive',(.045,.05,.03),.9)
earth=mat('Ground / dry ochre',(.24,.15,.06),.95)
def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone projection')
 for p in o.data.polygons:
  normal=p.normal
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   a,b=(co.x,co.y) if abs(normal.z)>.7 else ((co.y,co.z) if abs(normal.x)>.7 else (co.x,co.z))
   layer.data[li].uv=(a*.8+.5,b*.8+.5)
'''+s[s.index('def cube('):s.index('for o in bpy.data.objects:')]
s=s.replace('m.segments=3','m.segments=1')
s+='''for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(liner if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Staggered individual stone blocks, with epsilon-clipped edge partitions.
for row in range(8):
 z=.10+(row+.5)*1.46/8;h=1.46/8-.012
 for sy in [-1,1]:
  cuts=sorted(set([-1.86,1.86]+[round(-1.86+j*.465+(row%2)*.2325,5) for j in range(9) if -1.86+1e-5 < -1.86+j*.465+(row%2)*.2325 < 1.86-1e-5]))
  for a,b in zip(cuts,cuts[1:]):cube('Masonry / front rear block',((a+b)/2,sy*1.145,z),(b-a-.012,.19,h),stone_mat,bevel=.008)
 for sx in [-1,1]:
  cuts=sorted(set([-1.044,1.044]+[round(-1.044+j*.4176+(row%2)*.2088,5) for j in range(6) if -1.044+1e-5 < -1.044+j*.4176+(row%2)*.2088 < 1.044-1e-5]))
  for a,b in zip(cuts,cuts[1:]):cube('Masonry / side block',(sx*1.745,(a+b)/2,z),(.23,b-a-.012,h),stone_mat,bevel=.008)
cube('Granite / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone_mat,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Granite / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone_mat,bevel=.004)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone_mat,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def rock(n,loc,scale,p=None,material=stone_mat):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=1,location=loc);o=bpy.context.object;o.name=n
 for v in o.data.vertices:
  x,y,z=v.co;k=1+.035*math.sin(3*x+2*y)+.025*math.cos(4*z-y)
  v.co=Vector((x*scale[0]*k,y*scale[1]*k,z*scale[2]))
 o.data.materials.append(material);uv(o)
 for f in o.data.polygons:f.use_smooth=True
 if p:parent(o,p)
 return o
for sx in [-1,1]:
 for sy in [-1,1]:rock('Granite foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19))
rock('Terrain / ochre plinth',(0,.10,1.98),(1.20,.79,.075),lid,earth)
rock('Kopje / basal boulder',(.22,.20,2.19),(.70,.49,.25),lid)
rock('Kopje / middle boulder',(.15,.18,2.54),(.51,.38,.24),lid)
rock('Kopje / crown boulder',(.24,.20,2.86),(.61,.36,.20),lid)
rock('Kopje / companion',(-.72,-.18,2.17),(.35,.28,.20),lid)
'''
s+=(R.parent/'japan-cedar-v1/author.py').read_text().split('# Medallion is solid')[1]
s=s.replace(', never an unexplained front opening.',' # Solid family emblem, not a traditional symbol.',1)
s=s.replace('japan.blend','zimbabwe.blend').replace('japan.glb','zimbabwe.glb').replace('JAPAN AUTHORED','ZIMBABWE AUTHORED').replace("scene.cycles.samples=32","scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.use_nodes=False").replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
(R/'author.py').write_text(s)
