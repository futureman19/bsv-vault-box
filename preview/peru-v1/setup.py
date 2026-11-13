from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','THREE-LICENSE.txt','package.json','motion.mjs']:
 shutil.copy2(S/n,R/n)
for n in ['viewer.js','template.html','build.py','verify_source.py','verify_parity.py','verify_browser.py']:
 t=(S/n).read_text(encoding='utf8').replace('japan-cedar-v1','peru-v1').replace('japan.glb','peru.glb').replace('japan.blend','peru.blend').replace('Japan / Cedar & Moss','Peru / Andean Stone & Terraces').replace('Yakushima cedar. Mossed granite. Quiet brass.','Andean stone. Green terraces. Quiet brass.').replace('original Japan concept','research-backed Peruvian landscape brief').replace('JAPAN ·','PERU ·')
 (R/n).write_text(t,encoding='utf8')
t=(S/'author.py').read_text(); start=t[:t.index('wood=mat(')]
helpers=t[t.index('def uv('):t.index('for o in bpy.data.objects:')].replace('m.segments=3','m.segments=1')
# Dominant-normal planar projection, not inherited wood-axis mapping.
a=helpers.index('   u=');b=helpers.index('\ndef cube')
helpers=helpers[:a]+"   co=o.matrix_world@co\n   if abs(p.normal.z)>.7:u,v=co.x,co.y\n   elif abs(p.normal.x)>.7:u,v=co.y,co.z\n   else:u,v=co.x,co.z\n   layer.data[li].uv=(u/2+.5,v/2+.5)\n"+helpers[b:]
stone=t[t.index('def stone('):t.index("stone('Terrain / granite'")]
tail=t[t.index('# Medallion is solid'):].replace('japan','peru').replace('JAPAN','PERU').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=4;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=800')
body='''
stone_mat=mat('Andean / warm grey stone',(.28,.26,.22),.85);maptex(stone_mat,'stone-color.png','Base Color');maptex(stone_mat,'stone-roughness.png','Roughness',True)
granite=stone_mat
wood=stone_mat
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / dark green',(.035,.06,.025),.9)
green=mat('Terrace / grass green',(.16,.23,.09),.95);maptex(green,'green-color.png','Base Color')
'''
body+=helpers
body+='''
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(stone_mat if o.name.startswith('Interior') else gold)
  if o.name.startswith('Interior'):uv(o)
# Geometric staggered masonry shells, with individually separated joints.
for row in range(4):
 z=.10+(row+.5)*1.46/4
 for sy in [-1,1]:
  cuts=[-1.86]+[x for x in [-1.45+row%2*.36,-.7+row%2*.36,.05+row%2*.36,.8+row%2*.36,1.55+row%2*.36] if -1.85<x<1.85]+[1.86]
  for j,(a,b) in enumerate(zip(cuts,cuts[1:])):cube('Masonry / long %s %s %s'%(row,sy,j),((a+b)/2,sy*1.145,z),(b-a-.014,.19,1.46/4-.014),stone_mat,bevel=.018)
 for sx in [-1,1]:
  for j in range(3):cube('Masonry / side %s %s %s'%(row,sx,j),(sx*1.745,-.7+j*.7,z),(.23,.686,1.46/4-.014),stone_mat,bevel=.018)
cube('Stone / clasp seat',(0,-1.255,1.36),(.56,.075,.47),stone_mat,bevel=.025)
for sy in [-1,1]:cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Stone / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),stone_mat,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),stone_mat,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
'''
body+=stone
body+='''
# Five inset contour terraces: each taller/narrower and shifted rearwards.
for i in range(5):
 w=2.9-i*.37; d=1.5-i*.19; cy=-.02+i*.06; z=1.99+i*.115
 cube('Terrace / stone riser '+str(i),(0,cy,z+.052),(w,d,.105),stone_mat,lid,.022)
 cube('Terrace / green tread '+str(i),(0,cy,z+.112),(w-.065,d-.065,.02),green,lid,.006)
# Asymmetric crag behind terrace ascent, silhouette remains under stated cap.
stone('Ridge / west',(-.45,.54,2.72),(.40,.28,.31),lid,sub=2)
stone('Ridge / east',(.12,.60,2.64),(.26,.23,.23),lid,sub=2)
'''
(R/'author.py').write_text(start+body+tail,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n')
print('Peru pipeline initialized; prior pilots unchanged')
