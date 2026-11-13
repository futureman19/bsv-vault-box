"""One-time scoped adaptation of the repository's mechanical pilot."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for name in ['mechanism.blend','THREE-LICENSE.txt','motion.mjs']:
 shutil.copyfile(S/name,R/name)
for name in ['build.py','viewer.js','template.html','verify_source.py','verify_parity.py','verify_browser.py','package.json']:
 s=(S/name).read_text(encoding='utf8').replace('japan-cedar-v1','bosnia-and-herzegovina-v1').replace('japan.blend','bosnia-and-herzegovina.blend').replace('japan.glb','bosnia-and-herzegovina.glb')
 s=s.replace('Japan / Cedar & Moss','Bosnia and Herzegovina / Sarajevo Copper').replace('Yakushima cedar. Mossed granite. Quiet brass.','Hammered copper. Floral relief. Warm brass.').replace('Interactive Japan Cedar and Moss model','Interactive Bosnia and Herzegovina Sarajevo Copper model').replace('inspired by the original Japan concept','inspired by Sarajevo copperwork; an original geometric floral interpretation').replace('JAPAN · 3D / 001','BOSNIA AND HERZEGOVINA · 001')
 if name=='template.html':
  s=s.replace('h1{font-siz... [truncated]','h1{font-size:30px}.foot{flex-direction:column}.folio{white-space:normal}}')
 if name=='viewer.js':s=s.replace('camera.position.set(-5,3.7,7)','camera.position.set(-5,5.5,7)')
 if name=='verify_browser.py':
  s=s.replace("page.wait_for_timeout(70);assert page.evaluate('pilot.progress')==1","page.wait_for_function('pilot.progress===1',timeout=3000);assert page.evaluate('pilot.progress')==1")
  s=s.replace("page.wait_for_timeout(60);assert page.evaluate('pilot.progress')==0","page.wait_for_function('pilot.progress===0',timeout=3000);assert page.evaluate('pilot.progress')==0")
 (R/name).write_text(s,encoding='utf8')
s=(S/'author.py').read_text()
# Retain functions and mechanical source only, replace all Japan visual construction.
head=s[:s.index('wood=mat(')]
func=s[s.index('def uv('):s.index('for o in bpy.data.objects:')]
func=func.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z", "u=co.y if abs(p.normal.x)>.7 else co.x;v=co.y if abs(p.normal.z)>.7 else co.z")
tube=s[s.index('def tube('):s.index('trunk=[')]
footer=s[s.index('# Clean obsolete'):].replace('japan.blend','bosnia-and-herzegovina.blend').replace('japan.glb','bosnia-and-herzegovina.glb').replace('JAPAN AUTHORED','BOSNIA AND HERZEGOVINA AUTHORED').replace('scene.cycles.samples=32','scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4').replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
custom='''copper=mat('Copper / hammered satin',(.40,.16,.07),.42,.78)
maptex(copper,'copper-color.png','Base Color');maptex(copper,'copper-roughness.png','Roughness',True)
t=copper.node_tree.nodes.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(R/'maps/copper-normal.png'));t.image.colorspace_settings.name='Non-Color';t.image.pack()
n=copper.node_tree.nodes.new('ShaderNodeNormalMap');n.inputs['Strength'].default_value=.32;copper.node_tree.links.new(t.outputs['Color'],n.inputs['Color']);copper.node_tree.links.new(n.outputs['Normal'],copper.node_tree.nodes.get('Principled BSDF').inputs['Normal'])
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
bronze=mat('Bronze / dark interior',(.065,.032,.018),.58,.6)
seam=mat('Patina / dark teal seam',(.018,.065,.055),.8,.2)
for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(bronze if o.name.startswith('Interior') else gold)
for sy in [-1,1]:cube('Copper / front rear skin',(0,sy*1.145,.83),(3.26,.19,1.46),copper,bevel=.008)
for sx in [-1,1]:cube('Copper / side skin',(sx*1.745,0,.83),(.23,2.48,1.46),copper,bevel=.008,axis='Y')
cube('Copper / clasp seat',(0,-1.255,1.36),(.56,.075,.47),copper,bevel=.025)
for sy in [-1,1]:cube('Patina seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Patina seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:
  cube('Copper / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),copper,bevel=.004)
  cube('Bronze / foot',(sx*1.47,sy*.91,-.08),(.48,.42,.34),bronze,bevel=.06)
slab=cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),copper,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
def disc(name,r,z,depth,material):
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=depth,location=(0,0,z));o=bpy.context.object;o.name=name;o.data.materials.append(material);uv(o);parent(o);return o
disc('Ornament / copper tray',.78,1.991,.032,copper)
disc('Ornament / central boss',.115,2.025,.06,gold)
'''
ornament='''for radius in [.76,.24]:
 pts=[(radius*math.cos(j*math.tau/96),radius*math.sin(j*math.tau/96),2.014) for j in range(97)]
 tube('Ornament / ring',pts,[.012]*len(pts),gold,sides=8)
for k in range(8):
 a=k*math.tau/8;pts=[]
 for j in range(49):
  t=j*math.tau/48;rad=.46+.20*math.cos(t);side=.10*math.sin(t)
  pts.append((rad*math.cos(a)-side*math.sin(a),rad*math.sin(a)+side*math.cos(a),2.022))
 tube('Ornament / petal '+str(k),pts,[.014]*len(pts),gold,sides=8)
for sy in [-1,1]:
 for k in range(25):
  x=-1.5+k*.125
  bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=4,radius=.022,location=(x,sy*.97,1.985));o=bpy.context.object;o.name='Border / punched bead';o.data.materials.append(gold);parent(o)
for sx in [-1,1]:
 for k in range(13):
  bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=4,radius=.022,location=(sx*1.57,-.78+k*.13,1.985));o=bpy.context.object;o.name='Border / punched bead';o.data.materials.append(gold);parent(o)
'''
(R/'author.py').write_text(head.replace('Reference-led Japan pilot','Sarajevo copper craft-inspired pilot')+func+custom+tube+ornament+footer)
(R/'.gitattributes').write_text('* -text\n')
(R/'.gitignore').write_text('node_modules/\n__pycache__/\n*.blend1\n')
print('Scoped author and inherited mechanics/browser harness prepared')
