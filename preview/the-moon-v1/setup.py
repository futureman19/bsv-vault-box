from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','THREE-LICENSE.txt','package.json']:
 shutil.copy2(S/n,R/n)
for n in ['build.py','viewer.js','template.html','verify_browser.py','verify_source.py','verify_parity.py']:
 t=(S/n).read_text(encoding='utf8').replace('japan-cedar-v1','the-moon-v1').replace('japan.glb','the-moon.glb').replace('japan.blend','the-moon.blend').replace('Japan / Cedar & Moss','The Moon / Regolith & Impact').replace('Japan Cedar and Moss','The Moon Regolith and Impact').replace('Yakushima cedar. Mossed granite. Quiet brass.','Ancient impacts. Silver highlands. Dark basalt seas.').replace('inspired by the original Japan concept','inspired by lunar regolith, highlands and impact basins').replace('JAPAN · 3D / 001','THE MOON · 3D / 001')
 if n=='viewer.js':
  t=t.replace('camera.position.set(-5,3.7,7)','camera.position.set(-4.7,6.6,6.4)')
  t=t.replace("open.setAttribute('aria-pressed',String(!!target));", "open.setAttribute('aria-pressed',String(!!target));if(reduced.matches){progress=target;const p=pose(progress);lid.rotation.x=p.lid;latch.rotation.x=p.latch;window.pilot.progress=progress;}")
  t=t.replace("controls.reset();open.textContent", "controls.reset();lid.rotation.x=latch.rotation.x=0;window.pilot.progress=0;open.textContent")
 (R/n).write_text(t,encoding='utf8')
(R/'.gitattributes').write_text('* -text whitespace=cr-at-eol\n')
t=(S/'author.py').read_text(); pre=t[:t.index("wood=mat")]
helpers=t[t.index('def uv('):t.index('for o in bpy.data.objects:')]
helpers=helpers[:helpers.index('def cube')]+helpers[helpers.index('def cube'):]
# Replace wood-oriented UV projection with dominant-normal physical axes.
a=helpers.index('def uv'); b=helpers.index('def cube')
helpers='''def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Rock projection')
 for p in o.data.polygons:
  axes=sorted(range(3),key=lambda i:abs(p.normal[i]))[:2]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]/2+.5,co[axes[1]]/2+.5)
'''+helpers[b:]
ending=t[t.index('# Medallion is solid'):].replace('japan','the-moon').replace('JAPAN','THE MOON')
ending=ending.replace("scene.cycles.samples=32", "scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.use_nodes=False") .replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=800')
(R/'author.py').write_text(pre+(R/'geometry.txt').read_text()+helpers+(R/'geometry-body.txt').read_text()+ending)
print('Prepared scoped author/viewer/test scripts')
