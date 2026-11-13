"""One-time scoped adaptation of the existing Japan mechanism/tooling."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
J=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','THREE-LICENSE.txt']:
 shutil.copyfile(J/n,R/n)
shutil.copyfile(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
for n in ['verify_source.py','verify_parity.py','verify_browser.py','build.py','viewer.js','template.html','package.json']:
 s=(J/n).read_text(encoding='utf8').replace('japan-cedar-v1','armenia-v1').replace('japan.blend','armenia.blend').replace('japan.glb','armenia.glb').replace('Japan','Armenia').replace('JAPAN','ARMENIA').replace('Cedar & Moss','Rose Tuff Arcade').replace('Cedar and Moss','Rose Tuff Arcade').replace('Yakushima cedar. Mossed granite. Quiet brass.','Rose volcanic stone. Open arcades. Warm brass.').replace('inspired by the original Armenia concept','inspired by Armenian tuff architecture; an invented arcade, not a building replica')
 if n=='template.html':
  s=s.replace('h1{font-siz... [truncated]','h1{font-size:30px}.foot{flex-direction:column;gap:12px}}')
 if n=='viewer.js':
  s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,4.8,7)').replace('controls.maxDistance=11','controls.maxDistance=14')
  s=s.replace("bindAction(open,()=>{target=target?0:1;", "function snap(){progress=target;const p=pose(progress);lid.rotation.x=p.lid;latch.rotation.x=p.latch;window.pilot.progress=progress;window.pilot.lid=p.lid;window.pilot.latch=p.latch;}\n bindAction(open,()=>{target=target?0:1;if(reduced.matches)snap();")
  s=s.replace('controls.reset();open.textContent','controls.reset();snap();open.textContent')
 if n=='build.py':s=s.replace('quality=90','quality=85')
 (R/n).write_text(s,encoding='utf8')
s=(J/'author.py').read_text()
s=s[:s.index('wood=mat')]+'''wood=mat('Tuff / rose volcanic ash',(.55,.28,.22),.72);maptex(wood,'tuff-color.png','Base Color');maptex(wood,'tuff-roughness.png','Roughness',True)
granite=mat('Volcanic stone / charcoal',(.12,.10,.11),.85);maptex(granite,'basalt-color.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Mineral seam / charcoal',(.04,.028,.03),.9)
'''+s[s.index('def uv('):s.index('# Exterior skins')]+'''# Continuous stone skins, shortened front/rear to avoid overlapping corners.
for sy in [-1,1]:cube('Tuff / front' if sy<0 else 'Tuff / rear',(0,sy*1.145,.83),(3.26,.19,1.46),wood,bevel=.012)
for sx in [-1,1]:cube('Tuff / side',(sx*1.745,0,.83),(.23,2.48,1.46),wood,bevel=.012)
'''+s[s.index('# Small collar'):s.index('# A thin satin')]+s[s.index('# Restrained brass'):s.index("stone('Terrain / granite'")]+'''# A low, open three-arch architectural miniature. All stone travels with lid.
for cx in [-.95,0,.95]:
 for side in [-1,1]:cube('Arcade / pier',(cx+side*.34,.35,2.149),(.10,.20,.342),wood,lid,.008)
 verts=[];faces=[];N=24
 for i in range(N+1):
  a=i*math.pi/N
  for y in [.25,.45]:
   for r in [.29,.39]:verts.append((cx+r*math.cos(a),y,2.32+r*math.sin(a)))
 for i in range(N):
  k=4*i;q=k+4
  faces.extend([(k,q,q+1,k+1),(k+2,k+3,q+3,q+2),(k,k+2,q+2,q),(k+1,q+1,q+3,k+3)])
 faces.extend([(0,1,3,2),(4*N,4*N+2,4*N+3,4*N+1)])
 me=bpy.data.meshes.new('Tuff arch');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Arcade / arch',me);bpy.context.collection.objects.link(o);me.materials.append(wood);uv(o);parent(o)
'''+s[s.index('# Medallion'):]
s=s.replace('Cedar /','Tuff /').replace('japan.blend','armenia.blend').replace('japan.glb','armenia.glb').replace('JAPAN AUTHORED','ARMENIA AUTHORED')
a=s.index("def uv(");b=s.index('def cube(',a)
s=s[:a]+'''def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone planar projection')
 for p in o.data.polygons:
  axis=max(range(3),key=lambda i:abs(p.normal[i]));axes=[i for i in range(3) if i!=axis]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;layer.data[li].uv=(co[axes[0]]*.7,co[axes[1]]*.7)
'''+s[b:]
s=s.replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=2;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
(R/'author.py').write_text(s)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
print('Scoped tooling and author created')
