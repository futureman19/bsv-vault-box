from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; B=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','THREE-LICENSE.txt','package.json','motion.mjs']:
 shutil.copy2(B/n,R/n)
for n in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html']:
 s=(B/n).read_text(encoding='utf8').replace('japan-cedar-v1','iran-v1').replace('japan.glb','iran.glb').replace('japan.blend','iran.blend').replace('Japan / Cedar & Moss','Iran / Turquoise & Star').replace('Japan Cedar and Moss','Iran Turquoise and Star').replace('JAPAN ·','IRAN ·').replace('Yakushima cedar. Mossed granite. Quiet brass.','Glazed turquoise. Ivory stars. Warm brass.').replace('inspired by the original Japan concept','inspired by Iranian architectural ceramics; independently designed star motifs')
 if n=='verify_parity.py':s=s.replace('len(image_names)>=3','len(image_names)>=2')
 if n=='viewer.js':s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.5,7)')
 (R/n).write_text(s,encoding='utf8')
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
# Reuse vetted mechanisms and helper code, not the previous country's art.
a=(B/'author.py').read_text()
s=a[a.index('import bpy'):a.index("wood=mat")]
s+= '''ceramic=mat('Ceramic / turquoise star glaze',(.02,.33,.36),.27);maptex(ceramic,'ceramic-color.png','Base Color');maptex(ceramic,'ceramic-roughness.png','Roughness',True)
navy=mat('Ceramic / cobalt',(.012,.03,.105),.28)
ivory=mat('Ceramic / ivory',(.82,.72,.46),.32)
turquoise=mat('Ceramic / turquoise jewels',(.015,.38,.42),.23)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / deep blue',(.008,.016,.032),.8)
wood=ceramic
'''
s+=a[a.index('def uv('):a.index('for o in bpy.data.objects:')]
# isotropic face projection, no inherited wood grain UVs
start=s.index('def uv(');end=s.index('def cube(')
s=s[:start]+'''def uv(o,axis='X',endgrain=False):
 layer=o.data.uv_layers.active or o.data.uv_layers.new(name='Ceramic tiling')
 for p in o.data.polygons:
  for li in p.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co
   if abs(p.normal.z)>.7:u,v=co.x,co.y
   elif abs(p.normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u/1.2+.5,v/1.2+.5)
'''+s[end:]
s+='''for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(navy if o.name.startswith('Interior') else gold)
for sy in [-1,1]:cube('Ceramic body / front rear',(0,sy*1.145,.83),(3.72,.19,1.46),ceramic,bevel=.018)
for sx in [-1,1]:cube('Ceramic body / sides',(sx*1.745,0,.83),(.23,2.10,1.46),ceramic,bevel=.018)
'''
s+=a[a.index("# Small collar"):a.index('# A thin satin')].replace('Cedar','Ceramic').replace('wood,lid','navy,lid')
s+=a[a.index('# Restrained brass'):a.index('def stone')]
s+='''for sx in [-1,1]:
 for sy in [-1,1]:cube('Ceramic / foot',(sx*1.47,sy*.91,-.08),(.48,.42,.30),navy,bevel=.06)
def prism(n,xy,z,h,material):
 verts=[(x,y,z) for x,y in xy]+[(x,y,z+h) for x,y in xy];k=len(xy)
 faces=[tuple(reversed(range(k))),tuple(range(k,2*k))]+[(i,(i+1)%k,(i+1)%k+k,i+k) for i in range(k)]
 me=bpy.data.meshes.new(n);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(n,me);bpy.context.collection.objects.link(o);me.materials.append(material);parent(o);return o
for ix in range(5):
 for iy in range(3):
  x=(ix-2)*.62;y=(iy-1)*.60
  xy=[(x+(.24 if k%2==0 else .15)*math.cos(k*math.pi/8),y+(.24 if k%2==0 else .15)*math.sin(k*math.pi/8)) for k in range(16)]
  prism('Mosaic / eight point star',xy,1.978,.046,ivory)
  xy=[(x+.08*math.cos(k*math.pi/4),y+.08*math.sin(k*math.pi/4)) for k in range(8)]
  prism('Mosaic / turquoise jewel',xy,2.024,.024,turquoise)
for ix in range(4):
 for iy in range(2):
  x=(ix-1.5)*.62;y=(iy-.5)*.60
  prism('Mosaic / diamond',[(x,y-.17),(x+.17,y),(x,y+.17),(x-.17,y)],1.978,.034,navy)
'''
s+=a[a.index('# Medallion'):]
s=s.replace('japan.blend','iran.blend').replace('japan.glb','iran.glb').replace('JAPAN AUTHORED','IRAN AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=2;scene.use_nodes=False').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820').replace('(-5.6,-7.8,4.5)','(-5.6,-7.8,6.5)')
(R/'author.py').write_text(s)
print('Scaffold created; design brief predates model.')
