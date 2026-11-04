from pathlib import Path
import shutil
R=Path(__file__).resolve().parent;S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','THREE-LICENSE.txt','motion.mjs','package.json','build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html']:
 if n.endswith(('.blend','.txt')):shutil.copy2(S/n,R/n)
 else:
  t=(S/n).read_text().replace('japan-cedar-v1','pakistan-v1').replace('japan.glb','pakistan.glb').replace('japan.blend','pakistan.blend').replace('Japan / Cedar & Moss','Pakistan / Multan Blue').replace('Interactive Japan Cedar and Moss','Interactive Pakistan Multan Blue').replace('Yakushima cedar. Mossed granite. Quiet brass.','Ivory glaze. Cobalt flowers. Multan-inspired craft.').replace('inspired by the original Japan concept','inspired by the blue pottery tradition of Multan').replace('JAPAN ·','PAKISTAN ·')
  if n=='verify_browser.py':t=t.replace("page.wait_for_timeout(70)","page.wait_for_function('pilot.progress===1')").replace("page.wait_for_timeout(60)","page.wait_for_function('pilot.progress===0')")
  (R/n).write_text(t)
a=(S/'author.py').read_text();a=a[:a.index('wood=mat')]+a[a.index('def uv'):]
a=a[:a.index('# Exterior skins')]+a[a.index('# Small collar'):]
a=a[:a.index('# A thin satin')]+a[a.index('# Restrained brass'):]
a=a[:a.index("stone('Terrain / granite'")]+a[a.index('# Medallion'):]
a=a.replace('japan.blend','pakistan.blend').replace('japan.glb','pakistan.glb').replace('JAPAN AUTHORED','PAKISTAN AUTHORED').replace('Reference-led Japan pilot','Multan blue pottery inspired Pakistan pilot')
a=a.replace("for o in bpy.data.objects:\n if o.type",'''ivory=mat('Ceramic / ivory floral glaze',(.8,.78,.66),.3);maptex(ivory,'floral-color.png','Base Color');maptex(ivory,'glaze-roughness.png','Roughness',True)
wood=mat('Ceramic / cobalt glaze',(.012,.047,.19),.26);maptex(wood,'cobalt-color.png','Base Color')
granite=mat('Stone / speckled feet',(.25,.25,.27),.8);maptex(granite,'stone.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / deep blue',(.008,.019,.045),.9)
turquoise=mat('Relief / turquoise',(.025,.35,.42),.28)
cream=mat('Relief / ivory',(.82,.78,.64),.3)
for sy in [-1,1]:cube('Ceramic / front rear skin',(0,sy*1.145,.83),(3.26,.19,1.46),ivory,bevel=.006)
for sx in [-1,1]:cube('Ceramic / side skin',(sx*1.745,0,.83),(.23,2.48,1.46),ivory,bevel=.006,axis='Y')
for o in bpy.data.objects:
 if o.type''')
# Existing re-material loop must not overwrite newly created floral panels.
a=a.replace("if o.type=='MESH' and not o.name.startswith('Studio'):","if o.type=='MESH' and not o.name.startswith(('Studio','Ceramic')):")
insert='''# Three shallow eight-petal rosettes, with flattened ellipsoid reliefs.
for flower,x in enumerate([-1.05,0,1.05]):
 for j in range(8):
  angle=j*math.tau/8
  bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=1,location=(x+.22*math.cos(angle),.22*math.sin(angle),2.018))
  o=bpy.context.object;o.name=f'Rosette / {flower} petal {j}';o.scale=(.20,.075,.035);o.rotation_euler.z=angle;o.data.materials.append(turquoise if j%2==0 else cream)
  for f in o.data.polygons:f.use_smooth=True
  parent(o)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=10,radius=1,location=(x,0,2.035));o=bpy.context.object;o.name=f'Rosette / {flower} centre';o.scale=(.09,.09,.045);o.data.materials.append(gold)
 for f in o.data.polygons:f.use_smooth=True
 parent(o)
'''
a=a.replace('# Medallion',insert+'# Medallion').replace("scene.cycles.samples=32","scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=4;scene.use_nodes=False")
a=a.replace("location=(-5.6,-7.8,4.5)","location=(-5.6,-7.8,6.8)")
(R/'author.py').write_text(a)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
print('Scoped source templates prepared')
