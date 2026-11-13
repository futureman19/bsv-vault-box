"""One-time bounded reuse of the existing pilot's mechanical/viewer harness."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','package.json']:
 shutil.copy2(S/name,R/name)
for name in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','motion.mjs','template.html']:
 s=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','mexico-v1').replace('japan.glb','mexico.glb').replace('japan.blend','mexico.blend').replace('Japan / Cedar & Moss','Mexico / Talavera & Agave').replace('Japan Cedar and Moss','Mexico Talavera and Agave').replace('Japan geometry','Mexico geometry').replace('Yakushima cedar. Mossed granite. Quiet brass.','Cobalt ceramic. Blue agave. Warm terracotta.').replace('inspired by the original Japan concept','inspired by Mexican ceramic craft and agave landscapes').replace('JAPAN ·','MEXICO ·')
 if name=='verify_browser.py':
  s=s.replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1',timeout=3000)").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0',timeout=3000)")
 (R/name).write_text(s,encoding='utf8')
(R/'.gitattributes').write_text('* -text whitespace=cr-at-eol\nviewer.bundle.js -diff\nmexico-v1.html -diff\n')
# Reuse helpers, not the previous country's visible shapes.
a=(S/'author.py').read_text()
helpers=a[a.index('def select('):a.index("wood=mat(")]
cube=a[a.index('def cube('):a.index('for o in bpy.data.objects:')]
stone=a[a.index('def stone('):a.index('for sx in [-1,1]:',a.index('def stone('))]
(R/'helpers.py').write_text('import bpy,math,random\nfrom mathutils import Vector\nfrom pathlib import Path\nR=Path(__file__).resolve().parent\nlid=bpy.data.objects["Lid_Hinge"]\n'+helpers+'''def uv(o,axis='X'):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Face projection')
 for p in o.data.polygons:
  axis=max(range(3),key=lambda j:abs(p.normal[j]))
  ij=[j for j in range(3) if j!=axis]
  coords=[v.co for v in o.data.vertices]
  lo=[min(v[j] for v in coords) for j in ij];hi=[max(v[j] for v in coords) for j in ij]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=tuple((co[j]-lo[k])/max(hi[k]-lo[k],1e-6) for k,j in enumerate(ij))
'''+cube+stone.replace('material=granite','material=None'),encoding='utf8')
print('Scaffold copied; no old geometry or acceptance results copied.')
