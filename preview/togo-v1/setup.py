"""Scoped adaptation of the frozen Japan mechanism/viewer lineage."""
from pathlib import Path
R=Path(__file__).resolve().parent
for name in ['viewer.js','template.html','build.py','verify_source.py','verify_parity.py','verify_browser.py','package.json']:
 p=R/name;s=p.read_text(encoding='utf8').replace('japan-cedar-v1','togo-v1').replace('japan.blend','togo.blend').replace('japan.glb','togo.glb').replace('Japan / Cedar & Moss','Togo / Earth Towers').replace('Japan Cedar and Moss','Togo Earth Towers').replace('JAPAN','TOGO').replace('Yakushima cedar. Mossed granite. Quiet brass.','Layered earth. Rounded towers. Quiet brass.').replace('inspired by the original Japan concept','inspired by Koutammakou earthen architecture')
 s=s.replace('font-siz... [truncated]','font-size:30px}.foot{flex-direction:column}.folio{margin-top:8px}}')
 if name=='viewer.js':
  s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.1,7)')
  s=s.replace("bindAction(open,()=>{target=target?0:1;", "function snap(){if(reduced.matches&&ready){progress=target;const p=pose(progress);lid.rotation.x=p.lid;latch.rotation.x=p.latch;window.pilot.progress=progress;window.pilot.lid=p.lid;window.pilot.latch=p.latch;}}\n bindAction(open,()=>{target=target?0:1;snap();")
  s=s.replace("controls.reset();open.textContent", "controls.reset();snap();open.textContent")
 p.write_text(s,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
# Reuse primitive author helpers and the proven articulation, not Japan ornament.
s=(R.parent/'japan-cedar-v1/author.py').read_text()
s=s[:s.index('wood=mat')]+'''earth=mat('Earth / layered ochre',(.40,.20,.09),.82);maptex(earth,'earth-color.png','Base Color');maptex(earth,'earth-roughness.png','Roughness',True)
wood=earth
end=earth
granite=mat('Earth / stone feet',(.24,.13,.07),.9);maptex(granite,'stone.png','Base Color')
gold=mat('Brass / antique satin',(.48,.30,.10),.30,.8)
seam=mat('Earth / dark umber seam',(.065,.035,.015),.9)
straw=mat('Straw / warm roof',(.48,.32,.13),.92)
'''+s[s.index('def uv('):s.index('# Exterior skins')]+'''
# Continuous earthen wall skins with butt corners, no overlapping exterior faces.
for sy in [-1,1]:cube('Earth / long skin',(0,sy*1.145,.83),(3.26,.19,1.46),earth,bevel=.018)
for sx in [-1,1]:cube('Earth / side skin',(sx*1.745,0,.83),(.23,2.48,1.46),earth,bevel=.018,axis='Y')
'''+s[s.index('# Small collar'):s.index('# A thin satin')]+s[s.index('# Restrained brass'):s.index("stone('Terrain / granite'")]+'''
# Rotationally formed tower surfaces; closed bases, side courses, flat tops.
def lathe(name,x,y,profile,material):
 verts=[];faces=[];N=40
 for z,r in profile:
  for j in range(N):
   a=j*math.tau/N;verts.append((x+r*math.cos(a),y+r*math.sin(a),z))
 for k in range(len(profile)-1):
  for j in range(N):
   a=k*N+j;b=k*N+(j+1)%N;faces.append((a,b,b+N,a+N))
 faces += [tuple(reversed(range(N))),tuple((len(profile)-1)*N+j for j in range(N))]
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);me.materials.append(material);uv(o);parent(o)
 for f in me.polygons:f.use_smooth=len(f.vertices)==4
 return o
for x in [-.66,.66]:
 for y in [-.43,.43]:
  top=2.58 if y>0 else 2.48
  profile=[]
  for i in range(17):
   t=i/16;profile.append((1.978+t*(top-1.978),.25-.025*t+.006*math.sin(i*math.pi*.5)))
  lathe('Compound / tower',x,y,profile,earth)
  if y>0:
   lathe('Compound / granary',x,y,[(2.57,.14),(2.62,.21),(2.71,.245),(2.79,.22),(2.83,.16)],earth)
   lathe('Compound / thatch cap',x,y,[(2.81,.28),(2.84,.28),(3.09,.015),(3.10,.008)],straw)
for sy in [-1,1]:cube('Compound / linking wall X',(0,sy*.43,2.16),(1.32,.13,.364),earth,lid,.02)
for sx in [-1,1]:cube('Compound / linking wall Y',(sx*.66,0,2.16),(.13,.86,.364),earth,lid,.02)
'''+s[s.index('# Medallion'):]
s=s.replace('japan.blend','togo.blend').replace('japan.glb','togo.glb').replace('JAPAN AUTHORED','TOGO AUTHORED').replace('Reference-led Japan pilot','Brief-led Togo pilot').replace('Cedar /','Earth /').replace('Granite foot','Earth foot')
s=s.replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
# Face-normal projection gives comparable grain on all wall directions.
a=s.index("   u=co.y if axis");b=s.index('def cube(',a)
s=s[:a]+'''   if abs(p.normal.z)>.7:u,v=co.x,co.y
   elif abs(p.normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u/3.72+.5,v/1.7+.5)
'''+s[b:]
(R/'author.py').write_text(s)
print('Scoped Togo scripts prepared')
