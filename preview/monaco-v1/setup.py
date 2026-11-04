from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','package.json','motion.mjs']:
 shutil.copy2(S/name,R/name)
for name in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html']:
 text=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','monaco-v1').replace('japan.glb','monaco.glb').replace('japan.blend','monaco.blend').replace('Japan / Cedar & Moss','Monaco / The Rock & Riviera').replace('Japan Cedar and Moss','Monaco Rock and Riviera').replace('Yakushima cedar. Mossed granite. Quiet brass.','Pale stone. Terracotta rooftops. Mediterranean blue.').replace('inspired by the original Japan concept','inspired by Monaco’s Rock and Mediterranean setting').replace('JAPAN ·','MONACO ·')
 if name=='verify_browser.py':
  text=text.replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1');assert page.evaluate('pilot.progress')==1").replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0');assert page.evaluate('pilot.progress')==0")
 (R/name).write_text(text,encoding='utf8')
(R/'.gitattributes').write_text('* -text\n')
# Reuse small mechanical author helpers, not Japan's visible artwork.
s=(S/'author.py').read_text(); helpers=s[s.index('def select'):s.index('wood=mat')]
helpers+=s[s.index('def uv'):s.index('for o in bpy.data.objects:')]
helpers+=s[s.index('def stone'):s.index('for sx in [-1,1]:\n for sy in [-1,1]:stone')].replace('material=granite','material=None').replace('o.data.materials.append(material);uv(o)','o.data.materials.append(material or stone_mat);uv(o)')
# Replace wood UV convention with physically isotropic dominant-face mapping.
a=helpers.index('def uv');b=helpers.index('def cube')
helpers=helpers[:a]+'''def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Stone planar projection')
 for p in o.data.polygons:
  n=p.normal; dominant=max(range(3),key=lambda i:abs(n[i]));axes=[i for i in range(3) if i!=dominant]
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   layer.data[li].uv=(co[axes[0]]*.6+.5,co[axes[1]]*.6+.5)
'''+helpers[b:]
(R/'helpers.py').write_text(helpers)
print('SETUP_PASS')
