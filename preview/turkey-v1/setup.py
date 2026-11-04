from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','THREE-LICENSE.txt','motion.mjs','viewer.js','template.html','build.py','verify_source.py','verify_parity.py','verify_browser.py','package.json']:
 if n.endswith(('.blend','.txt')):shutil.copy2(S/n,R/n);continue
 t=(S/n).read_text(encoding='utf8').replace('japan-cedar-v1','turkey-v1').replace('japan.glb','turkey.glb').replace('japan.blend','turkey.blend').replace('Japan','Turkey').replace('JAPAN','TURKEY').replace('Cedar & Moss','Iznik Tulip').replace('Cedar and Moss','Iznik Tulip').replace('Yakushima cedar. Mossed granite. Quiet brass.','Ivory glaze. Cobalt flowers. Scarlet tulips.').replace('inspired by the original Turkey concept','inspired by Iznik floral ceramics; an original composition, not an antique replica')
 (R/n).write_text(t,encoding='utf8')
# Timing assertions observe the renderer instead of assuming wall-clock frame delivery.
p=R/'verify_browser.py';t=p.read_text().replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1',timeout=5000)").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0',timeout=5000)");p.write_text(t)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
# Reuse authored mechanical helpers, never the Japan theme geometry.
s=(S/'author.py').read_text();prefix=s[s.index('import bpy'):s.index("wood=mat(")]
helpers=s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
helpers=helpers[:helpers.index('def cube(')]+helpers[helpers.index('def cube('):]
# Isotropic face projection prevents stretched wood-oriented mapping on ceramic.
a=helpers.index('def uv(');b=helpers.index('def cube(')
helpers='''def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Ceramic face UV')
 for face in o.data.polygons:
  ax=max(range(3),key=lambda i:abs(face.normal[i])); axes=[i for i in range(3) if i!=ax]
  for li in face.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]/.82+.5,co[axes[1]]/.82+.5)

'''+helpers[b:]
tube=s[s.index('def tube('):s.index('trunk=[')]
end=s[s.index('# Medallion is solid'):]
end=end.replace('japan.blend','turkey.blend').replace('japan.glb','turkey.glb').replace('JAPAN AUTHORED','TURKEY AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=4').replace('resolution_x=1100','resolution_x=960').replace('resolution_y=1000','resolution_y=880').replace('(-5.6,-7.8,4.5)','(-5.6,-7.8,6.5)')
(R/'author.py').write_text(prefix+helpers+(R/'theme_geometry.py').read_text()+tube+(R/'ornament.py').read_text()+end)
print('Prepared Turkey-specific author and inherited mechanical/browser harnesses')
