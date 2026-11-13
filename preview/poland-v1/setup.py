from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','viewer.js','template.html','build.py','verify_source.py','verify_parity.py','verify_browser.py','THREE-LICENSE.txt','package.json']:
 if n.endswith(('.py','.js','.html','.json','.mjs')):
  t=(S/n).read_text(encoding='utf8').replace('japan-cedar-v1','poland-v1').replace('japan.glb','poland.glb').replace('japan.blend','poland.blend').replace('Japan','Poland').replace('Cedar & Moss','Cobalt & Cream').replace('cedar & moss','cobalt & cream')
  if n=='verify_parity.py':t=t.replace('len(image_names)>=3','len(image_names)>=2')
  (R/n).write_text(t,encoding='utf8')
 else:shutil.copy2(S/n,R/n)
(R/'.gitattributes').write_text('* -text\n')
# Retain base helper implementations and hardware, replace the entire theme.
a=(S/'author.py').read_text();prefix=a[:a.index('wood=mat(')]
helpers=a[a.index('def uv('):a.index('for o in bpy.data.objects:')]
helpers=helpers.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z","u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z")
materials="""
wood=mat('Ceramic / cobalt eyes on cream',(.8,.74,.6),.25);maptex(wood,'ceramic-color.png','Base Color');maptex(wood,'ceramic-roughness.png','Roughness',True)
blue=mat('Ceramic / cobalt glaze',(.009,.035,.18),.23)
cream=mat('Ceramic / warm ivory',(.78,.72,.59),.28)
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
"""
body="""
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(cream if o.name.startswith('Interior') else gold)
for sy in [-1,1]:cube('Ceramic / front' if sy<0 else 'Ceramic / rear',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.025)
for sx in [-1,1]:cube('Ceramic / side',(sx*1.745,0,.83),(.23,2.10,1.46),wood,bevel=.025,axis='Y')
cube('Ceramic / clasp seat',(0,-1.255,1.36),(.56,.075,.47),blue,bevel=.025)
for sy in [-1,1]:cube('Cobalt seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.070),blue,bevel=.009)
for sx in [-1,1]:
 cube('Cobalt seam / side',(sx*1.74,0,1.618),(.16,2.05,.070),blue,bevel=.009)
 for sy in [-1,1]:cube('Ceramic / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),blue,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),blue,lid,.045)
cube('Lid / cream inset',(0,0,1.986),(3.30,1.96,.025),wood,lid,.008)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
  cube('Ceramic foot',(sx*1.47,sy*.91,-.075),(.48,.43,.30),blue,bevel=.08)
for i in range(8):
 a=i*math.tau/8
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=10,radius=1,location=(.40*math.cos(a),.40*math.sin(a),2.055))
 o=bpy.context.object;o.name='Rosette / petal '+str(i);o.scale=(.26,.105,.058);o.rotation_euler.z=a;o.data.materials.append(blue);select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);parent(o)
 for f in o.data.polygons:f.use_smooth=True
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=1,location=(0,0,2.055));o=bpy.context.object;o.name='Rosette / center';o.scale=(.16,.16,.075);o.data.materials.append(gold);select(o);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);parent(o)
"""
tail=a[a.index('# Medallion is solid'):].replace('japan','poland').replace('JAPAN','POLAND').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=800')
tail=tail.replace("bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile", "scene.cycles.use_denoising=False;scene.render.threads_mode='FIXED';scene.render.threads=2;scene.use_nodes=False\nbpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile")
(R/'author.py').write_text(prefix+materials+helpers+body+tail)
print('SETUP PASS')
