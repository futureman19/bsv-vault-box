"""One-time scaffold from read-only Japan mechanical/viewer lineage."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; B=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','package.json']:
 shutil.copyfile(B/name,R/name)
for name in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','motion.mjs','template.html']:
 s=(B/name).read_text(encoding='utf8').replace('japan-cedar-v1','colombia-v1').replace('japan.glb','colombia.glb').replace('japan.blend','colombia.blend').replace('Japan','Colombia').replace('JAPAN','COLOMBIA').replace('Cedar & Moss','Coffee Cordillera').replace('Cedar and Moss','Coffee Cordillera').replace('Yakushima cedar. Mossed granite. Quiet brass.','Honey bamboo. Mountain coffee. Warm brass.').replace('inspired by the original Colombia concept','inspired by Colombia’s coffee cultural landscape')
 (R/name).write_text(s,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n')
s=(B/'author.py').read_text()
# Retain helpers and established mechanism, not the old visible cedar artwork.
a=s[:s.index('wood=mat')]
a+='''wood=mat('Guadua / honey bamboo',(.45,.28,.09),.48);maptex(wood,'bamboo-color.png','Base Color');maptex(wood,'bamboo-roughness.png','Roughness',True)
end=mat('Coffee / dark trim',(.10,.045,.018),.5)
granite=mat('Stone / dark feet',(.12,.13,.10),.85);maptex(granite,'stone.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / deep green',(.025,.05,.018),.9)
grass=mat('Cordillera / meadow',(.20,.32,.075),.95)
shrubs=mat('Coffee / foliage',(.035,.105,.018),.9)
cream=mat('Farmhouse / ivory plaster',(.76,.69,.48),.85)
roof=mat('Farmhouse / terracotta',(.40,.115,.047),.8)
'''
a+=s[s.index('def uv('):s.index('# Exterior skins')]
a+='''for sy in [-1,1]:cube('Guadua / long panel',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.012)
for sx in [-1,1]:cube('Guadua / side panel',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.012,axis='Y')
'''
a+=s[s.index('# Small collar'):s.index('slab=cube')].replace('Cedar /','Guadua /')
a+=s[s.index('slab=cube'):s.index('# A thin satin')]
a+=s[s.index('# Restrained brass'):s.index("stone('Terrain / granite'")]
a+='''# Irregular continuous hill surface, not isolated pebbles.
def height(x,y):
 return 2.005 + .47*math.exp(-((x+.62)**2/.39+(y-.10)**2/.23)) + .53*math.exp(-((x-.60)**2/.30+(y-.35)**2/.22)) + .22*math.exp(-((x-.05)**2/.37+(y+.42)**2/.16))
verts=[];faces=[];nx=55;ny=33
for j in range(ny):
 y=-.80+1.60*j/(ny-1)
 for i in range(nx):
  x=-1.40+2.80*i/(nx-1); edge=max(abs(x)/1.4,abs(y)/.8); z=height(x,y) if edge<.90 else 1.984+(height(x,y)-1.984)*max(0,(1-edge)/.10)
  verts.append((x,y,z))
for j in range(ny-1):
 for i in range(nx-1):
  a=j*nx+i;faces.append((a,a+1,a+1+nx,a+nx))
me=bpy.data.meshes.new('Rolling coffee hills');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Cordillera / planted hills',me);bpy.context.collection.objects.link(o);me.materials.append(grass);parent(o)
for f in me.polygons:f.use_smooth=True
# Curving shrub rows, spaced across the exposed front and western slopes.
for row in range(5):
 for col in range(12):
  x=-1.18+col*.205; y=-.63+row*.24+.06*math.sin(x*2.5+row*.3)
  if x>.33 and y>.15:continue
  stone('Coffee shrub / row %02d plant %02d'%(row,col),(x,y,height(x,y)+.035),(.066,.058,.059),lid,shrubs,2)
# Hilltop farmhouse: invented vernacular-inspired form, not a named building.
z=height(.60,.35)
cube('Farmhouse / plaster',(.60,.35,z+.10),(.38,.27,.23),cream,lid,.008)
cube('Farmhouse / door',(.60,.211,z+.06),(.067,.012,.13),end,lid,.002)
for side in [-1,1]:
 o=cube('Farmhouse / roof',(.60,.35+side*.086,z+.252),(.46,.205,.027),roof,None,.006);o.rotation_euler.x=-side*.49;parent(o)
'''
a+=s[s.index('# Medallion is solid'):]
a=a.replace('japan.blend','colombia.blend').replace('japan.glb','colombia.glb').replace('JAPAN AUTHORED','COLOMBIA AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=1000').replace('resolution_y=1000','resolution_y=900')
a=a.replace('Reference-led Japan pilot.','Brief-led Colombia pilot.').replace('random.seed(521)','random.seed(1121)')
(R/'author.py').write_text(a)
print('Scaffold authored; no prior output/evidence copied')
