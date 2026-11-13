from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
s=s.replace('Reference-led Japan pilot','Brief-led Malaysia songket pilot').replace("random.seed(521)","random.seed(1505)")
a=s.index("wood=mat(");b=s.index('def uv(')
s=s[:a]+'''wood=mat('Songket / crimson ground',(.16,.02,.04),.7);maptex(wood,'songket-color.png','Base Color');maptex(wood,'songket-roughness.png','Roughness',True)
end=mat('Lining / burgundy',(.08,.01,.025),.8);maptex(end,'lining.png','Base Color')
granite=mat('Feet / dark lacquer',(.035,.012,.018),.28)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / burgundy',(.025,.005,.012),.9)
'''+s[b:]
a=s.index('# Exterior skins');b=s.index('# Small collar')
s=s[:a]+'''# Continuous textile-clad skins; butt joints avoid coplanar corner overlap.
for sy in [-1,1]:cube('Songket / front rear skin',(0,sy*1.145,.83),(3.26,.19,1.46),wood,bevel=.015)
for sx in [-1,1]:cube('Songket / side skin',(sx*1.745,0,.83),(.23,2.48,1.46),wood,bevel=.015,axis='Y')
'''+s[b:]
a=s.index('# A thin satin');b=s.index('# Restrained brass')
s=s[:a]+s[b:]
a=s.index("stone('Terrain / granite'");b=s.index('def tube(')
s=s[:a]+s[b:]
a=s.index('trunk=[');b=s.index('# Medallion')
s=s[:a]+'''# Original abstract raised thread diamonds, not a copied named motif.
carrier=cube('Songket / crimson carrier',(0,0,1.987),(3.18,1.84,.018),end,lid,.004)
for iy in range(3):
 for ix in range(5):
  x=(ix-2)*.59;y=(iy-1)*.53
  pts=[(x-.22,y,2.010),(x,y+.20,2.010),(x+.22,y,2.010),(x,y-.20,2.010)]
  for j in range(4):tube('Songket thread / diamond %d %d edge %d'%(ix,iy,j),[pts[j],pts[(j+1)%4]],[.015,.015],gold,sides=6)
for sy in [-1,1]:cube('Songket / gold border long',(0,sy*.89,2.005),(3.10,.018,.018),gold,lid,.003)
for sx in [-1,1]:cube('Songket / gold border side',(sx*1.55,0,2.005),(.018,1.78,.018),gold,lid,.003)
'''+s[b:]
s=s.replace('Cedar /','Songket /').replace('japan.blend','malaysia.blend').replace('japan.glb','malaysia.glb').replace('JAPAN AUTHORED','MALAYSIA AUTHORED')
s=s.replace("scene.cycles.samples=32","scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.use_nodes=False")
s=s.replace('resolution_x=1100','resolution_x=960').replace('resolution_y=1000','resolution_y=880')
(R/'author.py').write_text(s)
print('author.py assembled; self-contained mechanism source included')
