from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'japan-cedar-v1/author.py').read_text()
s=s.replace('Japan','Brunei').replace('JAPAN','BRUNEI').replace('japan.blend','brunei.blend').replace('japan.glb','brunei.glb')
s=s.replace('Cedar /','Tenunan /').replace('Cedar foot','Stone foot').replace('Mineral seam / moss green','Textile seam / burgundy').replace('(.035,.07,.032)','(.075,.008,.025)')
s=s[:s.index("stone('Terrain / granite'")]+s[s.index('def tube('):]
a=s.index('trunk=[');b=s.index('# Medallion',a)
s=s[:a]+'''# Fifteen closed gold-thread diamond loops: original geometric interpretation.
for i,x in enumerate([-1.2,-.6,0,.6,1.2]):
 for j,y in enumerate([-.65,0,.65]):
  pts=[(x-.24,y,1.985),(x,y-.20,1.985),(x+.24,y,1.985),(x,y+.20,1.985),(x-.24,y,1.985)]
  tube('Tenunan diamond / %d %d'%(i,j),pts,[.012]*5,gold,sides=8)
''' +s[b:]
s=s.replace("scene.cycles.samples=32", "scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.use_nodes=False")
s=s.replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
(R/'author.py').write_text(s)
