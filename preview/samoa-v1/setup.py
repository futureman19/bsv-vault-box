"""Bootstrap local scripts from the read-only Japan mechanism lineage."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
S=R.parent/'japan-cedar-v1'
for n in ['mechanism.blend','motion.mjs','THREE-LICENSE.txt','package.json']:
 shutil.copyfile(S/n,R/n)
for n in ['build.py','verify_browser.py','verify_parity.py','verify_source.py','viewer.js','template.html']:
 t=(S/n).read_text(encoding='utf8').replace('japan-cedar-v1','samoa-v1').replace('japan.glb','samoa.glb').replace('japan.blend','samoa.blend').replace('Japan / Cedar & Moss','Samoa / Siapo & Lava').replace('Japan Cedar and Moss','Samoa Siapo and Lava').replace('Yakushima cedar. Mossed granite. Quiet brass.','Barkcloth-inspired geometry. Charcoal lava. Warm brass.').replace('inspired by the original Japan concept','inspired by Samoan barkcloth and volcanic landscapes; invented motifs, not a traditional-pattern replica').replace('JAPAN ·','SAMOA ·')
 if n=='viewer.js':
  t=t.replace("bindAction(open,()=>{target=target?0:1;", "function snap(){progress=target;const p=pose(progress);lid.rotation.x=p.lid;latch.rotation.x=p.latch;window.pilot.progress=progress;window.pilot.lid=p.lid;window.pilot.latch=p.latch;}\n bindAction(open,()=>{target=target?0:1;if(reduced.matches)snap();")
  t=t.replace('lastScale=1;controls.reset();','lastScale=1;controls.reset();if(ready)snap();')
 (R/n).write_text(t,encoding='utf8')
# Keep author helpers and original mechanism layout, replacing all theme geometry.
t=(S/'author.py').read_text(encoding='utf8')
head=t[:t.index('wood=mat(')]
helpers=t[t.index('def uv('):t.index('for o in bpy.data.objects:')]
helpers=helpers.replace("u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z", "u=co.y if axis=='Y' else co.x;v=co.y if abs(p.normal.z)>.7 else co.z")
stone=t[t.index('def stone('):t.index("for sx in [-1,1]:\n for sy in [-1,1]:stone")]
disk=t[t.index('def disk('):t.index('# Clean obsolete')]
end=t[t.index('# Clean obsolete'):].replace('japan','samoa').replace('JAPAN','SAMOA')
end=end.replace('scene.cycles.samples=32;', 'scene.cycles.samples=24;scene.cycles.use_denoising=False;scene.render.threads_mode="FIXED";scene.render.threads=4;scene.use_nodes=False;')
end=end.replace('resolution_x=1100','resolution_x=900').replace('resolution_y=1000','resolution_y=820')
materials='''wood=mat('Lava / charcoal porous stone',(.06,.07,.065),.88);maptex(wood,'lava-color.png','Base Color');maptex(wood,'lava-roughness.png','Roughness',True)
cloth=mat('Siapo / invented leaf and lozenge repeats',(.65,.45,.25),.84);maptex(cloth,'siapo-color.png','Base Color');maptex(cloth,'siapo-roughness.png','Roughness',True)
granite=wood
gold=mat('Brass / warm satin',(.48,.30,.10),.28,.8)
seam=mat('Seam / dark brown',(.04,.018,.009),.9)
liner=mat('Interior / warm dark timber',(.14,.065,.025),.7)
'''
geometry='''for o in bpy.data.objects:
 if o.type=='MESH' and not o.name.startswith('Studio'):
  o.data.materials.clear();o.data.materials.append(liner if o.name.startswith('Interior') else gold)
for sy in [-1,1]:
 cube('Lava / wall',(0,sy*1.145,.83),(3.72,.19,1.46),wood,bevel=.025)
 cube('Siapo / body panel',(0,sy*1.247,.84),(3.18,.018,1.08),cloth,bevel=.004)
for sx in [-1,1]:
 cube('Lava / side',(sx*1.745,0,.83),(.23,2.48,1.46),wood,bevel=.025,axis='Y')
 cube('Siapo / side panel',(sx*1.869,0,.84),(.018,1.94,1.08),cloth,bevel=.004,axis='Y')
cube('Lava / clasp seat',(0,-1.255,1.36),(.56,.075,.47),wood,bevel=.025)
for sy in [-1,1]:
 cube('Mineral seam / long',(0,sy*(1.14 if sy<0 else 1.10),1.618),(3.28,.16 if sy<0 else .08,.108),seam,bevel=.009)
for sx in [-1,1]:
 cube('Mineral seam / side',(sx*1.74,0,1.618),(.16,2.05,.108),seam,bevel=.009)
 for sy in [-1,1]:cube('Lava / rim corner',(sx*1.745,sy*1.145,1.616),(.23,.19,.112),wood,bevel=.004)
cube('Lid / polished slab',(0,0,1.828),(3.72,2.38,.30),wood,lid,.045)
for sx in [-1,1]:
 for sy in [-1,1]:
  cube('Corner hardware / top',(sx*1.73,sy*1.07,1.989),(.23,.23,.023),gold,lid,.008)
  cube('Corner hardware / edge',(sx*1.73,sy*1.197,1.93),(.23,.018,.12),gold,lid,.005)
# A genuine waved textile surface with closed edge skirt and bottom.
verts=[];faces=[];nx=32;ny=20
for j in range(ny+1):
 for i in range(nx+1):
  x=-1.58+i*3.16/nx;y=-.94+j*1.88/ny
  z=2.025+.012*math.sin(x*6+y*2)+.009*math.sin(y*8-x*2)
  verts.append((x,y,z))
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
boundary=list(range(nx+1))+[j*(nx+1)+nx for j in range(1,ny+1)]+[ny*(nx+1)+i for i in range(nx-1,-1,-1)]+[j*(nx+1) for j in range(ny-1,0,-1)]
bottom=[]
for a in boundary:
 bottom.append(len(verts));x,y,z=verts[a];verts.append((x,y,1.975))
for k,a in enumerate(boundary):
 n=(k+1)%len(boundary);faces.append((a,bottom[k],bottom[n],boundary[n]))
faces.append(tuple(reversed(bottom)))
me=bpy.data.meshes.new('Waved cloth geometry');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('Siapo / lid cloth',me);bpy.context.collection.objects.link(o);me.materials.append(cloth);uv(o);parent(o)
'''
rocks='''for sx in [-1,1]:
 for sy in [-1,1]:stone('Lava foot',(sx*1.47,sy*.91,-.10),(.32,.27,.19),sub=2)
for i,(x,y,z,s) in enumerate([(-1.18,.61,2.11,(.24,.20,.17)),(-.88,.65,2.16,(.29,.22,.21)),(-.55,.66,2.10,(.22,.18,.13))]):
 stone('Lava / lid mound '+str(i),(x,y,z),s,lid,sub=2)
'''
(R/'author.py').write_text(head+materials+helpers+geometry+stone+rocks+disk+end,encoding='utf8')
(R/'.gitattributes').write_text('* -text whitespace=cr-at-eol\n',encoding='utf8')
print('SAMOA_LOCAL_BOOTSTRAP_OK')
