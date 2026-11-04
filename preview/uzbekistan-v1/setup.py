"""One-time mechanical template adaptation; does not modify baseline files."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent; B=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','THREE-LICENSE.txt','motion.mjs']:
 shutil.copy2(B/n,R/n)
shutil.copy2(R.parent/'iceland-pilot/tests.mjs',R/'tests.mjs')
for n in ['build.py','verify_source.py','verify_parity.py','verify_browser.py','viewer.js','template.html','package.json']:
 s=(B/n).read_text(encoding='utf8').replace('japan-cedar-v1','uzbekistan-v1').replace('japan.glb','uzbekistan.glb').replace('japan.blend','uzbekistan.blend').replace('Japan / Cedar & Moss','Uzbekistan / Rishtan Blue').replace('Japan Cedar and Moss','Uzbekistan Rishtan Blue').replace('Yakushima cedar. Mossed granite. Quiet brass.','Ivory ceramic. Cobalt flowers. Turquoise relief.').replace('inspired by the original Japan concept','inspired by Rishtan ceramic palettes; the floral motif is an authored interpretation').replace('JAPAN ·','UZBEKISTAN ·')
 (R/n).write_text(s,encoding='utf8')
s=(B/'author.py').read_text(encoding='utf8')
s=s.replace('Reference-led Japan pilot','Brief-led Uzbekistan pilot').replace('japan.blend','uzbekistan.blend').replace('japan.glb','uzbekistan.glb').replace('JAPAN AUTHORED','UZBEKISTAN AUTHORED')
a=s.index("wood=mat(");b=s.index('\ndef uv(',a)
s=s[:a]+'''wood=mat('Ceramic / ivory cobalt floral',(.75,.73,.65),.24);maptex(wood,'ceramic-color.png','Base Color');maptex(wood,'ceramic-roughness.png','Roughness',True)
end=wood
granite=mat('Clay / terracotta',(.33,.105,.045),.8);maptex(granite,'clay.png','Base Color')
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / deep cobalt',(.012,.035,.085),.48)
turquoise=mat('Petal / turquoise glaze',(.035,.39,.44),.23)
cobalt=mat('Medallion / cobalt glaze',(.012,.065,.20),.21)
''' + s[b:]
a=s.index('   u=co.y');b=s.index('\ndef cube',a)
s=s[:a]+'''   if abs(p.normal.z)>.7:u,v=co.x,co.y
   elif abs(p.normal.x)>.7:u,v=co.y,co.z
   else:u,v=co.x,co.z
   layer.data[li].uv=(u/1.5+.5,v/1.5+.5)
''' + s[b:]
a=s.index('# Exterior skins');b=s.index('# Small collar',a)
s=s[:a]+'''# Continuous ceramic skins meet at butt joints, not interpenetrating corners.
for sy in [-1,1]:cube('Ceramic / front' if sy<0 else 'Ceramic / rear',(0,sy*1.145,.83),(3.26,.19,1.46),wood,bevel=.008)
for sx in [-1,1]:cube('Ceramic / side',(sx*1.745,0,.83),(.23,2.48,1.46),wood,bevel=.008,axis='Y')
''' +s[b:]
s=s.replace('Cedar / clasp seat','Ceramic / clasp seat').replace('Mineral seam /','Blue seam /').replace('Cedar / rim corner','Ceramic / rim corner')
a=s.index('# A thin satin');b=s.index('# Restrained brass',a);s=s[:a]+s[b:]
a=s.index("stone('Terrain / granite'");b=s.index('# Medallion is solid',a)
s=s[:a]+'''# Circular ceramic medallion and eight raised almond-shaped petals.
def ornament_disk(name,radius,depth,z,material):
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=radius,depth=depth,location=(0,0,z));o=bpy.context.object;o.name=name;o.data.materials.append(material);parent(o);return o
ornament_disk('Rishtan / medallion',.72,.035,1.992,cobalt)
ornament_disk('Rishtan / ivory inset',.66,.025,2.020,wood)
for j in range(8):
 a=j*math.tau/8; verts=[]
 # Closed low convex petal, leaf perimeter counter-clockwise.
 for k in range(16):
  t=k*math.tau/16; u=.36+.235*math.cos(t);v=.105*math.sin(t)
  verts.append((u*math.cos(a)-v*math.sin(a),u*math.sin(a)+v*math.cos(a),2.034))
 verts.extend([( .36*math.cos(a),.36*math.sin(a),2.098),(.36*math.cos(a),.36*math.sin(a),2.032)])
 faces=[]
 for k in range(16):faces.extend([(k,(k+1)%16,16),((k+1)%16,k,17)])
 me=bpy.data.meshes.new('Raised petal');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Rishtan / petal '+str(j),me);bpy.context.collection.objects.link(o);me.materials.append(turquoise);parent(o)
ornament_disk('Rishtan / central boss',.09,.045,2.055,cobalt)
bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=8,major_radius=.695,minor_radius=.012,location=(0,0,2.022));o=bpy.context.object;o.name='Rishtan / brass perimeter';o.data.materials.append(gold);parent(o)
''' +s[b:]
s=s.replace("'Granite foot'","'Clay foot'")
s=s.replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode=\'FIXED\';scene.render.threads=4').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
(R/'author.py').write_text(s,encoding='utf8')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n*-source.zip\n')
(R/'.gitattributes').write_text('* -text\n')
print('Adapted template, source mechanism and bounded checks')
